from confluent_kafka import Consumer
import json

consumer = Consumer({
    "bootstrap.servers": "localhost:19092",
    "group.id": "monitoring",
    "auto.offset.reset": "earliest"
})

consumer.subscribe(["server_temps"])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Error:", msg.error())
        continue

    data = json.loads(msg.value().decode("utf-8"))

    temp = data["temperature"]
    server = data["server_id"]

    if temp <= 60:
        status = "OK"
    elif temp <= 75:
        status = "WARNING"
    else:
        status = "CRITICAL ALERT"

    print(f"Server {server} | {temp}°C | {status}")