from airflow import DAG
from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import pyarrow.parquet as pq
import pandas as pd
from io import BytesIO

# Function to read the Parquet file and display a sample
def read_parquet_sample(**kwargs):
    # Define the file path on HDFS
    file_path = "/user/appuser/neo_bank_data/neo_bank_data/partition=0/neo_bank_data+0+0000001900+0000001999.parquet"
    
    # Initialize WebHDFSHook with the appropriate connection ID
    hdfs_hook = WebHDFSHook(webhdfs_conn_id="hdfs_default", proxy_user="appuser")
    
    # Read the Parquet file from HDFS using WebHDFSHook
    file_data = hdfs_hook.read_file(file_path)
    
    # Convert the file content to a Pandas DataFrame
    with BytesIO(file_data) as file_stream:
        # Use PyArrow to read the Parquet file
        table = pq.read_table(file_stream)
        df = table.to_pandas()
        
        # Display a sample (first 5 rows)
        print("Sample Data:")
        print(df.head(1).T)  # Display the first 5 rows

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'read_parquet_sample',
    default_args=default_args,
    description='A simple DAG to read and display a sample from a Parquet file in HDFS',
    schedule_interval=None,  # Manual trigger
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Task to read and display a sample from the Parquet file
    read_sample_task = PythonOperator(
        task_id='read_parquet_sample',
        python_callable=read_parquet_sample,
        provide_context=True
    )
