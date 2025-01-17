from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

# Define a Python function to query changed data (based on last_updated timestamp)
def query_changed_data():
    # Connect to PostgreSQL
    hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Get the last run date (this can be fetched from Airflow's XCom or another source)
    last_run_date = '{{ ts }}'  # Airflow templating to get the timestamp of the current task instance

    # Query for records that have been modified since the last run
    query = f"""
        SELECT id, name, age, last_updated
        FROM test_table
        WHERE last_updated > '{last_run_date}';
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # Process the changed data (e.g., print it)
    print("Changed data from PostgreSQL since last run:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Last Updated: {row[3]}")

    cursor.close()
    conn.close()

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'cdc_from_postgres_to_airflow',
    default_args=default_args,
    description='A simple DAG to capture changes from PostgreSQL',
    schedule_interval='@daily',  # Schedule this to run daily (or adjust as needed)
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    # Step 1: Query changed data from PostgreSQL
    query_changes = PythonOperator(
        task_id='query_changed_data',
        python_callable=query_changed_data
    )
