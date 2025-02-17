from kafka import KafkaProducer
import json
from datetime import date

KAFKA_TOPIC = "neo_bank_data"
KAFKA_BROKER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')  
)

def send_to_kafka(data):
    data = {k: (v.isoformat() if isinstance(v, date) else v) for k, v in data.items()}
    producer.send(KAFKA_TOPIC, data)
    producer.flush()
