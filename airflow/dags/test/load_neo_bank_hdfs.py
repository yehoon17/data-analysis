from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook

def upload_to_hdfs(**kwargs):
    """
    Upload a Parquet file to HDFS.
    """
    source_path = "/opt/airflow/raw_data/neo-bank-non-sub-churn-prediction/train_2008.parquet"
    destination_path = "/user/hdfs/train_2008.parquet"
    
    # Instantiate the WebHDFS hook
    hdfs_hook = WebHDFSHook(webhdfs_conn_id="hdfs_default")
    
    # Upload file to HDFS
    hdfs_hook.load_file(
        source=source_path,
        destination=destination_path,
        overwrite=True
    )
    print(f"Uploaded {source_path} to HDFS at {destination_path}")

# Define the DAG
with DAG(
    dag_id="upload_parquet_to_hdfs",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["hdfs", "parquet"],
) as dag:
    
    upload_file = PythonOperator(
        task_id="upload_parquet_file",
        python_callable=upload_to_hdfs,
    )

upload_file
