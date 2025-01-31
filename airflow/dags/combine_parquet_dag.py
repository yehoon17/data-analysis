from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from tasks.hdfs_user_operations import create_and_manage_user_hdfs_directory


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'combine_parquet_dag',
    default_args=default_args,
    description='DAG to combine multiple Parquet files using Spark',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    create_user_hdfs_dir = PythonOperator(
        task_id='create_user_hdfs_dir',
        python_callable=create_and_manage_user_hdfs_directory,
        op_kwargs={'username': 'spark', 'folder':'neo-bank'},  
    )

    combine_parquet = SparkSubmitOperator(
        task_id='combine_parquet',
        conn_id='spark_default',  # Uses AIRFLOW_CONN_SPARK_DEFAULT
        application='/opt/spark/jobs/combine_parquet.py',  # Path to Spark job in the container
        name='combine_parquet_job',
        application_args=[
            'file:///opt/airflow/raw_data/neo-bank-non-sub-churn-prediction/train_200*.parquet', # Input files (wildcard)
            'hdfs://namenode:9000/user/spark/neo-bank/'
        ],
        # conf={
        #     'spark.cores.max': '2',
        #     'spark.executor.memory': '1G',
        #     'spark.executor.instances': '1',
        # },
        # executor_cores=1,
        # executor_memory='1G',
        # driver_memory='512M',
        # verbose=True,
    )

    create_user_hdfs_dir >> combine_parquet
    