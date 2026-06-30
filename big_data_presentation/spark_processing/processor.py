import os
import sys

# Ensure driver and workers use the same Python version
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, split, udf, window, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# Ensure current directory and subfolders are in PYTHONPATH for workers
# and to make local imports work reliably.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import utilities by name to avoid closure capture
try:
    from big_data_presentation.spark_processing.utils import get_sentiment
except ImportError:
    # Handle both run-as-script and run-as-module scenarios
    from big_data_presentation.spark_processing.utils import get_sentiment

def main():
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:19092,localhost:29092,localhost:39092,localhost:49092,localhost:59092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_tweets")

    spark = SparkSession.builder \
        .appName("HashtagAnalyzer") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .config("spark.sql.kafka.consumer.useUninterruptibleThread", "true") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")

    # Add utils.py to spark context so workers can find it
    spark.sparkContext.addPyFile(os.path.join(current_dir, "utils.py"))

    # Move UDF registration here using the named function
    sentiment_udf = udf(get_sentiment, FloatType())

    schema = StructType([
        StructField("id", StringType(), True),
        StructField("text", StringType(), True),
        StructField("created_at", StringType(), True),
        StructField("lang", StringType(), True)
    ])

    # Read from Kafka
    raw_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .option("kafka.consumer.useUninterruptibleThread", "true") \
        .load()

    # Parse JSON
    tweets = raw_stream.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Add timestamp with watermark
    tweets = tweets.withColumn("timestamp", current_timestamp()) #\
                   #.withWatermark("timestamp", "10 minutes")

    # If we wanted to use event time instead:
    # tweets = tweets.withColumn("event_time", col("created_at").cast("timestamp"))

    # Extract hashtags
    hashtags_df = tweets.withColumn("hashtag", explode(split(col("text"), " "))) \
        .filter(col("hashtag").startswith("#")) \
        .withColumn("hashtag", split(col("hashtag"), "[^a-zA-Z0-9#]").getItem(0))

    # Calculate sentiment
    processed_df = hashtags_df.withColumn("sentiment", sentiment_udf(col("text")))

    # Aggregations
    windowed_metrics = processed_df \
        .groupBy(
            window(col("timestamp"), "5 minutes", "1 minute"),
            col("hashtag")
        ) \
        .agg({
            "hashtag": "count",
            "sentiment": "avg"
        }) \
        .withColumnRenamed("count(hashtag)", "count") \
        .withColumnRenamed("avg(sentiment)", "avg_sentiment") \
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            "hashtag",
            "count",
            "avg_sentiment"
        )

    # Write to Console
    query_console = windowed_metrics.writeStream \
        .outputMode("update") \
        .format("console") \
        .start()

    query_console.awaitTermination()

if __name__ == "__main__":
    main()
