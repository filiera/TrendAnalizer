import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, current_timestamp, udf, avg, count
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from textblob import TextBlob

"""
ĆWICZENIE: Monitor Sentymentu Językowego

Cel: Oblicz średni sentyment oraz liczbę tweetów dla każdego języka 
używając okna przesuwnego (sliding window).

ZADANIA:
1. Skonfiguruj połączenie z Kafką (readStream) na localhost:19092.
2. Użyj funkcji current_timestamp(), aby utworzyć kolumnę 'timestamp'.
3. Zastosuj 'sentiment_udf' do kolumny 'text'.
4. Pogrupuj dane według 2-minutowego okna (przesuwanego co 1 minutę) ORAZ kolumny 'lang'.
5. Oblicz średni sentyment i liczbę wystąpień dla każdej grupy.
6. Bonus: Przefiltruj wyniki, aby pokazać tylko języki z więcej niż 2 tweetami w oknie.
"""

# Logika sentymentu
def get_sentiment(text):
    if not text: return 0.0
    return TextBlob(text).sentiment.polarity

sentiment_udf = udf(get_sentiment, FloatType())

def main():
    spark = SparkSession.builder \
        .appName("ZadanieSentymentJezykowy") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("ERROR")

    schema = StructType([
        StructField("text", StringType(), True),
        StructField("lang", StringType(), True)
    ])

    # 1. TODO: Odczyt z Kafki
    # raw_stream = ...
    
    # 2. TODO: Parsowanie JSON, dodanie timestamp i obliczenie sentymentu
    # tweets = ...
    
    # 3. TODO: Agregacja po oknie i języku
    # lang_trends = ...

    # 4. TODO: Zapis do konsoli w trybie 'update'
    # query = ...
    
    print("Skrypt zadania uruchomiony. Uzupełnij TODO, aby zobaczyć wyniki!")
    # query.awaitTermination()

if __name__ == "__main__":
    main()
