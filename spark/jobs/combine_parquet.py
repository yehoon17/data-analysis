from pyspark.sql import SparkSession

def combine_parquet(input_path, output_path):
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("Load Parquet to HDFS") \
        .master("spark://spark-master:7077") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
        .config("spark.sql.legacy.parquet.nanosAsLong", "true") \
        .config("spark.sql.debug.maxToStringFields", "1000") \
        .getOrCreate()

    # Read multiple Parquet files
    df = spark.read.parquet(input_path)
    print(f"DataFrame has {len(df.columns)} columns.")

    # Perform transformations if needed (e.g., filtering or deduplication)
    combined_df = df

    # Write the combined DataFrame to the output path
    combined_df.write.mode("overwrite").parquet(output_path)

    print(f"Combined Parquet files written to {output_path}")

    spark.stop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print('!!Wrong arg')
        print("Usage: combine_parquet.py <input_path> <output_path>")
        sys.exit(-1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    combine_parquet(input_path, output_path)
