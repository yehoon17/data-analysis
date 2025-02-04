from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook
from airflow.utils.dates import days_ago
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import io

def read_hdfs(**kwargs):
    directory = "/user/airflow/neo-bank/"
    
    # Instantiate the WebHDFS hook
    hdfs_hook = WebHDFSHook(
        webhdfs_conn_id="hdfs_default",
        proxy_user="airflow"
    )
    
    conn = hdfs_hook.get_conn()
    files = conn.list(directory)
    
    # Get today's date
    today = datetime.today()
    
    # Get the date that is 365 days before today
    date_365_days_ago = today - timedelta(days=365)
    
    # Extract the year from the date 365 days ago
    year_365_days_ago = date_365_days_ago.year
    
    # Find the file that corresponds to the year 365 days ago
    file = next((f for f in files if str(year_365_days_ago) in f), None)
    
    if file is None:
        raise ValueError(f"No file found for the year {year_365_days_ago}")
    
    file_path = f"{directory}/{file}" if not directory.endswith('/') else f"{directory}{file}"
    
    # Read the file content
    content = hdfs_hook.read_file(file_path)
    
    # Load the content into a pandas DataFrame
    df = pd.read_parquet(io.BytesIO(content))
    
    # Filter the DataFrame to get the customer_id where the date is 365 days before today
    df['date'] = pd.to_datetime(df['date'])
    target_date = date_365_days_ago.strftime('%Y-%m-%d')
    customer_ids = df[df['date'] == target_date]['customer_id'].tolist()
    
    # Push the customer_ids to XCom so they can be used by the next task
    kwargs['ti'].xcom_push(key='customer_ids', value=customer_ids)

def update_churn_table(**kwargs):
    # Pull the customer_ids from XCom
    customer_ids = kwargs['ti'].xcom_pull(key='customer_ids', task_ids='read_hdfs_parquet_files')
    
    if not customer_ids:
        raise ValueError("No customer IDs found to update the churn table.")
    
    # Instantiate the Postgres hook
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # Create a connection and cursor
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    
    # Update or insert into the churn table for each customer_id
    for customer_id in customer_ids:
        upsert_query = """
        INSERT INTO churn (customer_id, churn_status, churn_date)
        VALUES (%s, %s, %s)
        ON CONFLICT (customer_id)
        DO UPDATE SET
            churn_status = EXCLUDED.churn_status,
            churn_date = EXCLUDED.churn_date;
        """
        cursor.execute(upsert_query, (customer_id, False, datetime.today().strftime('%Y-%m-%d')))
    
    # Commit the transaction
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()

# Define the DAG
dag = DAG(
    'label_churn',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(1),
    },
    schedule_interval=None,
    catchup=False,
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

# Task to read HDFS files and extract customer_ids
read_hdfs_task = PythonOperator(
    task_id='read_hdfs_parquet_files',
    python_callable=read_hdfs,
    provide_context=True,
    dag=dag,
)

# Task to update the churn table with the found customer_ids
update_churn_task = PythonOperator(
    task_id='update_churn_table',
    python_callable=update_churn_table,
    provide_context=True,
    dag=dag,
)

# Set the task dependencies in the DAG
create_churn_table >> read_hdfs_task >> update_churn_task