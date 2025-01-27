"""Test script for checking out spark job

In `spark-master` container:
 `spark-submit /opt/spark/jobs/test_simple_job.py`
In `airflow-webserver` container:
 `spark-submit --master spark://spark-master:7077 /opt/spark/jobs/test_simple_job.py`

Result:
 +-----+-----+
 | name|value|
 +-----+-----+
 |Alice|    1|
 |  Bob|    2|
 |Cathy|    3|
 +-----+-----+
"""

from pyspark.sql import SparkSession

def main():
    # Initialize a Spark session
    spark = SparkSession.builder \
        .appName("SimplePySparkJob") \
        .getOrCreate()

    # Create a DataFrame
    data = [("Alice", 1), ("Bob", 2), ("Cathy", 3)]
    df = spark.createDataFrame(data, ["name", "value"])

    # Show the DataFrame
    df.show()

    # Perform some transformations and actions
    result = df.groupBy("value").count()
    result.show()

    # Stop the Spark session
    spark.stop()

if __name__ == "__main__":
    main()
