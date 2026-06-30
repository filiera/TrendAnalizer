from confluent_kafka import Producer
import json, random, time

producer = Producer({
    "bootstrap.servers": "localhost:19092"
})

def delivery_report(err, msg):
    if err:
        print("Error:", err)

while True:
    data = {
        "server_id": random.randint(1, 5),
        "temperature": round(random.uniform(20, 90), 2)
    }

    producer.produce(
        topic="server_temps",
        value=json.dumps(data).encode("utf-8"),
        callback=delivery_report
    )

    producer.poll(0)
    time.sleep(random.uniform(1, 2))