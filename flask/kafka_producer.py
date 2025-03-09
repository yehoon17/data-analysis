from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import json
import numpy as np
from datetime import date, datetime
from kafka.errors import NoBrokersAvailable

KAFKA_TOPIC = "neo_bank_data"
KAFKA_BROKER = "kafka:9093"

producer = None
SCHEMA_REGISTRY_URL = "http://schema-registry:8082"

# Avro 스키마 정의
value_schema_str = """
{
   "type":"record",
   "name":"Transaction",
   "fields":[
      {"name":"Id","type":"int"},
      {"name":"customer_id","type":"int"},
      {"name":"interest_rate","type":"float"},
      {"name":"name","type":"string"},
      {"name":"country","type":"string"},
      {"name":"date_of_birth","type":"string"},
      {"name":"address","type":"string"},
      {"name":"date","type":"string"},
      {"name":"atm_transfer_in","type":"int"},
      {"name":"atm_transfer_out","type":"int"},
      {"name":"bank_transfer_in","type":"int"},
      {"name":"bank_transfer_out","type":"int"},
      {"name":"crypto_in","type":"int"},
      {"name":"crypto_out","type":"int"},
      {"name":"bank_transfer_in_volume","type":"float"},
      {"name":"bank_transfer_out_volume","type":"float"},
      {"name":"crypto_in_volume","type":"float"},
      {"name":"crypto_out_volume","type":"float"},
      {"name":"complaints","type":"int"},
      {"name":"touchpoints","type":{"type":"array","items":"string"}},
      {"name":"csat_scores","type":"string"},
      {"name":"tenure","type":"int"},
      {"name":"from_competitor","type":"boolean"},
      {"name":"job","type":"string"},
      {"name":"churn_due_to_fraud","type":"boolean"},
      {"name":"Usage","type":"string"},
      {"name":"model_predicted_fraud","type":"boolean"}
   ]
}
"""

value_schema = avro.loads(value_schema_str)

def initialize_kafka_producer():
    global producer
    try:
        producer = AvroProducer(
            {'bootstrap.servers': KAFKA_BROKER,
             'schema.registry.url': SCHEMA_REGISTRY_URL},
            default_value_schema=value_schema
        )
        return True
    except NoBrokersAvailable:
        return False

def serialize_data(data):
    # Convert datetime and date to string
    for key, value in data.items():
        if isinstance(value, (datetime, date)):
            data[key] = value.isoformat()
        elif isinstance(value, np.ndarray):
            data[key] = value.tolist()  # Convert numpy arrays to lists
        elif isinstance(value, dict):
            data[key] = json.dumps(value)  # Convert dictionaries to JSON strings
    return data

def send_to_kafka(data, serialize=True):
    if producer is None:
        raise Exception("Kafka producer is not initialized")

    if serialize:
        data = serialize_data(data) 
    producer.produce(topic=KAFKA_TOPIC, value=data)
    producer.flush()
