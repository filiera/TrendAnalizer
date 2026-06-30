from confluent_kafka import Consumer
import json

consumer_config = {
    "bootstrap.servers": "localhost:19092,localhost:29092,localhost:39092,localhost:49092,localhost:59092",
    "group.id": "raw_tweets_group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)

consumer.subscribe(["raw_tweets1"])

print("Consumer is running and subscribed to raw_tweets1")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        value = msg.value().decode("utf-8")
        tweet = json.loads(value)
        print(f"Received tweet - tweet id: {tweet['id']}, tweet text: {tweet['text']}, tweet created_at: {tweet['created_at']}, tweet lang {tweet['lang']}")
except KeyboardInterrupt:
    print("\n Stopping consumer")
finally:
    consumer.close()
