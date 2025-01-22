FROM apache/airflow:2.10.4

# Switch to root user to install system-level dependencies
USER root

# Install required libraries and clean up in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    # g++ \
    heimdal-dev \
    # libsasl2-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
  && pip uninstall -y argparse
