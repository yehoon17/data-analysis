from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

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
    dag_id='spark_job_dag',
    default_args=default_args,
    description='Run a Spark job using Airflow',
    schedule_interval=None,  
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # SparkSubmitOperator to run the Spark job
    run_spark_job = SparkSubmitOperator(
        task_id='spark_submit_task',
        application='/opt/spark/jobs/test_simple_job.py',  
        conn_id='spark_default',  
        name='example_spark_job',
        execution_timeout=timedelta(minutes=10),
        conf={
            'spark.cores.max': '2',
            'spark.executor.memory': '1G',
            'spark.executor.instances': '1',
        },
        executor_cores=1,
        executor_memory='1G',
        driver_memory='512M',
        verbose=True
    )

    run_spark_job
