from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from tasks.hdfs_user_operations import create_and_manage_user_hdfs_directory  

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
}

with DAG(
    'manage_hdfs_user_dir',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    create_user_hdfs_dir = PythonOperator(
        task_id='create_user_hdfs_dir',
        python_callable=create_and_manage_user_hdfs_directory,
        op_kwargs={'username': 'appuser', 'folder': 'neo_bank_data'},  
    )
