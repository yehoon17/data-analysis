from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Test") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

print('spark version:', spark.version)

hdfs_path = "hdfs://namenode:9000/user/spark"
try:
    files = spark._jvm.org.apache.hadoop.fs.FileSystem.get(
        spark._jsc.hadoopConfiguration()
    ).listStatus(spark._jvm.org.apache.hadoop.fs.Path(hdfs_path))
    print([f.getPath().toString() for f in files])
except Exception as e:
    print("Error accessing HDFS:", e)
