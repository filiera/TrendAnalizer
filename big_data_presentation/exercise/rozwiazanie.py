import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, current_timestamp, udf, avg, count
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from textblob import TextBlob

# Logika analizy sentymentu
def get_sentiment(text):
    if not text: return 0.0
    try:
        return TextBlob(text).sentiment.polarity
    except:
        return 0.0

sentiment_udf = udf(get_sentiment, FloatType())

def main():
    # Inicjalizacja Sparka z konektorem Kafka
    spark = SparkSession.builder \
        .appName("RozwiazanieSentymentJezykowy") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")

    # Definicja schematu danych
    schema = StructType([
        StructField("text", StringType(), True),
        StructField("lang", StringType(), True)
    ])

    # 1. Odczyt strumienia z Kafki
    raw_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:19092") \
        .option("subscribe", "raw_tweets") \
        .option("startingOffsets", "latest") \
        .load()

    # 2. Parsowanie JSON i dodanie czasu przetwarzania
    tweets = raw_stream.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*") \
        .withColumn("timestamp", current_timestamp())

    # 3. Obliczenie sentymentu dla każdego tweeta
    processed_tweets = tweets.withColumn("sentiment", sentiment_udf(col("text")))

    # 4. Agregacja w oknie czasowym według języka
    lang_trends = processed_tweets \
        .groupBy(
            window(col("timestamp"), "2 minutes", "1 minute"),
            col("lang")
        ) \
        .agg(
            avg("sentiment").alias("sredni_sentyment"),
            count("lang").alias("liczba_tweetow")
        ) \
        .filter(col("liczba_tweetow") > 2) \
        .select(
            col("window.start").alias("poczatek_okna"),
            col("window.end").alias("koniec_okna"),
            "lang",
            "liczba_tweetow",
            "sredni_sentyment"
        )

    # 5. Wyświetlenie wyników w konsoli
    print("Uruchamianie strumienia rozwiązania...")
    query = lang_trends.writeStream \
        .outputMode("update") \
        .format("console") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
