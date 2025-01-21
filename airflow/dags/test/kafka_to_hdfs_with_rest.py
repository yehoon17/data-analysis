from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.hooks.base import BaseHook
from kafka import KafkaConsumer
import requests

def consume_kafka_messages():
    # Get the Kafka connection details from Airflow
    kafka_conn = BaseHook.get_connection('kafka_default')  # This will use the connection defined in docker-compose
    print(f"Kafka connection details: {kafka_conn}")
    bootstrap_servers = kafka_conn.host + ':' + str(kafka_conn.port)  # Retrieve the host and port

    consumer = KafkaConsumer(
        'hdfs_pipeline',
        bootstrap_servers=bootstrap_servers,  # Use the connection URL dynamically
        auto_offset_reset='earliest',
        enable_auto_commit=True,
    )
    for message in consumer:
        data = message.value.decode('utf-8')
        store_to_hdfs(data)
        print(f"Consumed and stored message: {data}")

def store_to_hdfs(data):
    hdfs_url = "http://namenode:9870/webhdfs/v1/data/output.txt?op=CREATE&overwrite=true"
    response = requests.put(hdfs_url, data=data)
    if response.status_code == 201:
        print("Data successfully stored in HDFS.")
    else:
        print(f"Failed to store data in HDFS: {response.text}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='kafka_to_hdfs',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@once',
) as dag:

    kafka_to_hdfs_task = PythonOperator(
        task_id='consume_kafka_and_store_to_hdfs',
        python_callable=consume_kafka_messages,
    )

    kafka_to_hdfs_task
