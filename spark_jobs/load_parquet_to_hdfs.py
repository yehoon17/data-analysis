from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Load Parquet to HDFS") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .config("spark.sql.legacy.parquet.nanosAsLong", "true") \
    .config("spark.sql.debug.maxToStringFields", "1000") \
    .getOrCreate()

# Define paths
local_path = "file:///opt/spark/raw_data/neo-bank-non-sub-churn-prediction/train_200*.parquet"  # Mounted path inside container
hdfs_path = "hdfs://namenode:9000/user/spark/test/"  # Target HDFS path

# Read Parquet files from the local directory
print("Reading Parquet files from:", local_path)
df = spark.read.parquet(local_path)
print(f"DataFrame has {len(df.columns)} columns.")

# Write DataFrame to HDFS
print("Writing DataFrame to HDFS at:", hdfs_path)
df.write.mode("overwrite").parquet(hdfs_path)

print("Data successfully written to HDFS.")

# Stop Spark session
spark.stop()
