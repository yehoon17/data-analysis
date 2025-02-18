from kafka import KafkaProducer
import json
from datetime import date
from kafka.errors import NoBrokersAvailable

KAFKA_TOPIC = "neo_bank_data"
KAFKA_BROKER = "localhost:9092"

producer = None

def initialize_kafka_producer():
    global producer
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
        )
        return True
    except NoBrokersAvailable:
        return False

def send_to_kafka(data):
    if producer is None:
        raise Exception("Kafka producer is not initialized")
    data = {k: (v.isoformat() if isinstance(v, date) else v) for k, v in data.items()}
    producer.send(KAFKA_TOPIC, data)
    producer.flush()
