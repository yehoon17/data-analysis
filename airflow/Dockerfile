FROM apache/airflow:2.10.4

# Switch to root user to install system-level dependencies
USER root

# Install required libraries and clean up in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    # g++ \
    heimdal-dev \
    # libsasl2-dev \
    openjdk-17-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable for Spark compatibility
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Switch back to airflow user
USER airflow

# Copy and install Python dependencies
COPY /airflow/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
  && pip uninstall -y argparse
