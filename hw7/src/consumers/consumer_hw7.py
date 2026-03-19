import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='green-trips-q3',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=10000
)

count = 0
count_over_5 = 0

for message in consumer:
    data = message.value
    distance = data.get('trip_distance', 0)
    if distance is not None and float(distance) > 5.0:
        count_over_5 += 1
    count += 1

consumer.close()
print(f"Total messages: {count:,}")
print(f"Trips with trip_distance > 5: {count_over_5:,}")