#!/bin/bash

# Define variables
KAFKA_CONTAINER_NAME="kafka"
TOPIC_NAME="hdfs_pipeline"
BROKER="kafka:9092"
PARTITIONS=1
REPLICATION_FACTOR=1

# Execute the Kafka topic creation command
docker exec -it $KAFKA_CONTAINER_NAME kafka-topics \
  --create \
  --topic $TOPIC_NAME \
  --bootstrap-server $BROKER \
  --partitions $PARTITIONS \
  --replication-factor $REPLICATION_FACTOR

# Print confirmation
echo "Kafka topic '$TOPIC_NAME' created successfully!"
