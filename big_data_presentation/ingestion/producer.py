import os
import json
import tweepy
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_tweets")

class TweetProducer(tweepy.StreamingClient):
    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def on_tweet(self, tweet):
        data = {
            "id": tweet.id,
            "text": tweet.text,
            "created_at": str(tweet.created_at),
            "lang": tweet.lang if hasattr(tweet, 'lang') else 'unknown'
        }
        print(f"Sending tweet: {data['id']}")
        self.producer.send(KAFKA_TOPIC, data)
        self.producer.flush()

    def on_errors(self, status):
        print(f"Error: {status}")

if __name__ == "__main__":
    if not BEARER_TOKEN:
        print("Error: X_BEARER_TOKEN not found in .env")
        exit(1)

    streaming_client = TweetProducer(BEARER_TOKEN)
    
    # Example: Add rules for hashtags
    # streaming_client.add_rules(tweepy.StreamRule("#spark #bigdata"))
    
    print(f"Starting stream for topic: {KAFKA_TOPIC}")
    streaming_client.filter(tweet_fields=["created_at", "lang", "entities"])
