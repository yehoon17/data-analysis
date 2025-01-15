from kafka import KafkaProducer, KafkaConsumer
import psycopg2
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../.env')

# Kafka producer
def produce_data_to_kafka():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    topic = "test_topic"

    # Example data
    data = [
        {"id": 1, "name": "Alice", "age": 25},
        {"id": 2, "name": "Bob", "age": 30},
        {"id": 3, "name": "Charlie", "age": 35},
    ]

    for record in data:
        producer.send(topic, value=record)
        print(f"Produced: {record}")
        time.sleep(1)

    producer.close()

# Kafka consumer and PostgreSQL writer
def consume_data_and_store_in_postgres():
    consumer = KafkaConsumer(
        'test_topic',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=10000  # Exit after 10 seconds of inactivity
    )

    # PostgreSQL connection using environment variables
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()

    # Create table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INTEGER
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    try:
        for message in consumer:
            record = message.value
            print(f"Consumed: {record}")

            # Insert data into PostgreSQL
            insert_query = """
            INSERT INTO users (id, name, age) VALUES (%s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            cursor.execute(insert_query, (record['id'], record['name'], record['age']))
            conn.commit()

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        print("Consumer timed out or finished processing.")
        # Clean up
        consumer.close()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Run producer
    produce_data_to_kafka()

    # Run consumer
    consume_data_and_store_in_postgres()
