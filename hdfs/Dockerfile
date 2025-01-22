# Start from the original HDFS image
FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8

# Create the directory in HDFS and set permissions
COPY setup_hdfs.sh /setup_hdfs.sh
RUN chmod +x /setup_hdfs.sh && /setup_hdfs.sh
