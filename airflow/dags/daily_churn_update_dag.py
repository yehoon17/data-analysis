from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

def update_churn_table(**kwargs):
    # Calculate the target date (366 days before today)
    target_date = (datetime.today() - timedelta(days=366)).strftime('%Y-%m-%d')
    
    # Instantiate the Postgres hook
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Create a connection and cursor
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    
    # Query to find customer_ids where churn_date is equal to the target date
    select_query = """
    SELECT customer_id
    FROM churn
    WHERE churn_date = %s;
    """
    cursor.execute(select_query, (target_date,))
    customer_ids = [row[0] for row in cursor.fetchall()]
    
    if not customer_ids:
        print(f"No customers found with churn_date = {target_date}.")
        return
    
    # Update the churn table for each customer_id
    for customer_id in customer_ids:
        update_query = """
        UPDATE churn
        SET churn_status = TRUE, churn_date = %s
        WHERE customer_id = %s;
        """
        cursor.execute(update_query, (datetime.today().strftime('%Y-%m-%d'), customer_id))
    
    # Commit the transaction
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    print(f"Updated {len(customer_ids)} customers with churn_date = {target_date}.")

# Define the DAG
dag = DAG(
    'daily_churn_update',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(1),  # Start date for the DAG
    },
    schedule_interval='@daily',  # Run the DAG daily
    catchup=False,  # Disable catchup to avoid backfilling
)

# Task to create the 'churn' table if it does not exist
create_churn_table = PostgresOperator(
    task_id='create_churn_table',
    postgres_conn_id='postgres_default',
    sql="""
    CREATE TABLE IF NOT EXISTS churn (
        customer_id INT PRIMARY KEY,
        churn_status BOOLEAN NOT NULL,
        churn_date DATE
    );
    """,
    dag=dag,
)

# Task to update the churn table for customers with churn_date = 366 days before today
update_churn_task = PythonOperator(
    task_id='update_churn_table',
    python_callable=update_churn_table,
    provide_context=True,
    dag=dag,
)

# Set the task dependencies in the DAG
create_churn_table >> update_churn_task
