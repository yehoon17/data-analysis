#!/bin/bash

# Create the directory for Airflow user
echo "Creating /user/airflow directory in HDFS..."
hdfs dfs -mkdir -p /user/airflow

# Set permissions for the directory
echo "Setting permissions for /user/airflow..."
hdfs dfs -chown airflow:supergroup /user/airflow
hdfs dfs -chmod 770 /user/airflow

# Verify directory creation and permissions
hdfs dfs -ls /user
