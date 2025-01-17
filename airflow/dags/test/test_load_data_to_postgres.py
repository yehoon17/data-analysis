from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

# Define a Python function to verify the data was inserted
def verify_data_inserted():
    # Connect to PostgreSQL
    hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Query the inserted data
    cursor.execute("SELECT * FROM test_table")
    rows = cursor.fetchall()

    # Log the rows
    for row in rows:
        print(f"Row: {row}")

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
    'load_data_to_postgres',
    default_args=default_args,
    description='A simple DAG to load data to PostgreSQL',
    schedule_interval=None,  # Set to None for manual triggering
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    # Step 1: Create a test table in PostgreSQL
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_default',  # Connection ID defined in Airflow
        sql="""
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT
        );
        """
    )

    # Step 2: Insert sample data into the test table
    insert_data = PostgresOperator(
        task_id='insert_data',
        postgres_conn_id='postgres_default',
        sql="""
        INSERT INTO test_table (name, age) VALUES
        ('Alice', 30),
        ('Bob', 25),
        ('Charlie', 35);
        """
    )

    # Step 3: Verify data insertion
    verify_insertion = PythonOperator(
        task_id='verify_insertion',
        python_callable=verify_data_inserted
    )

    # Set the task dependencies
    create_table >> insert_data >> verify_insertion
