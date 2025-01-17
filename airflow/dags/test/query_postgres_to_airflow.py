from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

# Define a Python function to query data from PostgreSQL and process it
def query_and_process_data():
    # Connect to PostgreSQL
    hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Query the data (assuming the table `test_table` exists in PostgreSQL)
    cursor.execute("SELECT id, name, age FROM test_table;")
    rows = cursor.fetchall()

    # Process the data (print it in this case)
    print("Queried data from PostgreSQL:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

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
    'query_postgres_to_airflow',
    default_args=default_args,
    description='A simple DAG to query PostgreSQL and process data',
    schedule_interval=None,  # Set to None for manual triggering
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    # Step 1: Query and process data from PostgreSQL
    query_data = PythonOperator(
        task_id='query_and_process_data',
        python_callable=query_and_process_data
    )
