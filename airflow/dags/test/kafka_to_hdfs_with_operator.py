from airflow import DAG
from airflow.providers.apache.kafka.operators.consume import KafkaConsumeMessagesOperator
from airflow.providers.apache.hdfs.operators.hdfs import HDFSCreateFileOperator
from airflow.utils.dates import days_ago
import json

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

# Define the DAG
with DAG(
    "kafka_to_hdfs",
    default_args=default_args,
    description="Consume messages from Kafka and store them in HDFS",
    schedule_interval=None,
    start_date=days_ago(1),
    tags=["kafka", "hdfs"],
) as dag:

    # Step 1: Consume messages from Kafka
    consume_kafka = KafkaConsumeMessagesOperator(
        task_id="consume_from_kafka",
        kafka_conn_id="kafka_default",  # Airflow Kafka connection ID
        topics=["hdfs_pipeline"],  # Replace with your Kafka topic
        group_id="airflow-consumer-group",  # Consumer group ID
        max_messages=100,  # Number of messages to consume at once
    )

    # Step 2: Write messages to HDFS
    def transform_messages(**context):
        """
        Transform Kafka messages into a format suitable for HDFS.
        """
        messages = context["task_instance"].xcom_pull(task_ids="consume_from_kafka")
        return "\n".join([json.dumps(msg) for msg in messages]) if messages else ""

    write_to_hdfs = HDFSCreateFileOperator(
        task_id="write_to_hdfs",
        hdfs_conn_id="hdfs_default",  # Airflow HDFS connection ID
        file_path="/user/airflow/transactions.json",  # Path in HDFS
        data="{{ task_instance.xcom_pull(task_ids='consume_from_kafka', key='return_value') | tojson }}",
        overwrite=True,  # Overwrite the file if it exists
    )

    # Define task dependencies
    consume_kafka >> write_to_hdfs
