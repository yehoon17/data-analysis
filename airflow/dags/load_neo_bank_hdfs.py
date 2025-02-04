from datetime import datetime
import glob
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook
from tasks.hdfs_user_operations import create_and_manage_user_hdfs_directory  


def upload_to_hdfs(**kwargs):
    """
    Upload multiple Parquet files to HDFS using a wildcard pattern.
    """
    source_pattern = "/opt/airflow/raw_data/neo-bank-non-sub-churn-prediction/train_*.parquet"
    destination_path = "/user/airflow/neo-bank"
    
    # Instantiate the WebHDFS hook
    hdfs_hook = WebHDFSHook(
        webhdfs_conn_id="hdfs_default",
        proxy_user="airflow"
    )
    
    # Find all files matching the wildcard pattern
    source_files = glob.glob(source_pattern)
    
    if not source_files:
        print(f"No files found matching the pattern: {source_pattern}")
        return
    
    # Upload each file to HDFS
    for source_file in source_files:
        # Construct the destination path in HDFS
        file_name = source_file.split("/")[-1]  # Extract the file name
        hdfs_file_path = f"{destination_path}/{file_name}"
        
        # Upload the file
        hdfs_hook.load_file(
            source=source_file,
            destination=hdfs_file_path,
            overwrite=True
        )
        print(f"Uploaded {source_file} to HDFS at {hdfs_file_path}")
        

# Define the DAG
with DAG(
    dag_id="upload_parquet_to_hdfs",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["hdfs", "parquet"],
) as dag:
    
    create_user_hdfs_dir = PythonOperator(
        task_id='create_neo_bank_hdfs_dir',
        python_callable=create_and_manage_user_hdfs_directory,
        op_kwargs={'username': 'airflow', 'folder': 'neo-bank'},  
    )

    upload_file = PythonOperator(
        task_id="upload_parquet_file",
        python_callable=upload_to_hdfs,
    )

create_user_hdfs_dir >> upload_file
