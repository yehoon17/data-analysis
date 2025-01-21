FROM apache/airflow:2.10.4

USER root

# Install Kerberos libraries for HDFS provider
RUN apt-get update && apt-get install -y \
    krb5-user \
    libkrb5-dev \
    && apt-get clean

# Switch to airflow user
USER airflow

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
