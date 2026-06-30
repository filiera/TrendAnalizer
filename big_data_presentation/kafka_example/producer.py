import time
import json
import random
from confluent_kafka import Producer

KAFKA_BOOTSTRAP_SERVERS = "localhost:19092,localhost:29092,localhost:39092,localhost:49092,localhost:59092"
KAFKA_TOPIC = "raw_tweets1"

# Mock data configuration
LANGS = ["en", "es", "fr", "de"]
SENTIMENTS = [
    "I love using Spark for real-time processing! #spark #bigdata",
    "Kafka is a bit complex but very powerful. #kafka #streaming",
    "Python is the best language for data science. #python #ai",
    "I'm struggling with this data pipeline. #dataengineering #help",
    "The weather is great today! #sun #happy",
    "Spark Streaming is so fast! #spark #streaming",
    "Learning new things every day. #learning #python"
]

def generate_mock_tweet():
    text = random.choice(SENTIMENTS)
    return {
        "id": str(random.randint(1000000000, 9999999999)),
        "text": text,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lang": random.choice(LANGS)
    }

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered to {msg.topic()} "
            f"[{msg.partition()}] @ {msg.offset()}"
        )

def main():
    producer_config = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS
    }

    producer = Producer(producer_config)
    
    print(f"Starting mock producer, sending to topic: {KAFKA_TOPIC}")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            tweet = generate_mock_tweet()
            print(f"Sending mock tweet: {tweet['id']} - {tweet['text']}")
            producer.produce(
                topic=KAFKA_TOPIC,
                value=json.dumps(tweet).encode("utf-8"),
                callback=delivery_report
                )
            producer.poll(0)
            
            # Send a tweet every 1-3 seconds
            time.sleep(random.uniform(1.0, 3.0))
    except KeyboardInterrupt:
        print("\nStopping mock producer...")
    finally:
        print("Flushing remaining messages")
        producer.flush()
        producer.close()

if __name__ == "__main__":
    main()
