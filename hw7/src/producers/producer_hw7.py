import json
import math
import pandas as pd
from kafka import KafkaProducer
from time import time

def json_serializer(data):
    return json.dumps(data, allow_nan=False).encode('utf-8')

def clean_record(record):
    """Replace NaN/inf with None for JSON serialization"""
    return {
        k: (None if isinstance(v, float) and (math.isnan(v) or math.isinf(v)) else v)
        for k, v in record.items()
    }

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=json_serializer
)

print("Downloading green_tripdata_2025-10.parquet...")
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet"

columns = [
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount',
    'total_amount'
]

df = pd.read_parquet(url, columns=columns)

# Convert datetime columns to strings
df['lpep_pickup_datetime'] = df['lpep_pickup_datetime'].astype(str)
df['lpep_dropoff_datetime'] = df['lpep_dropoff_datetime'].astype(str)

print(f"Loaded {len(df):,} rows")

topic_name = 'green-trips'

t0 = time()

records = df.to_dict('records')
for message in records:
    producer.send(topic_name, value=clean_record(message))

producer.flush()

t1 = time()
took = t1 - t0
print(f"Sent {len(df):,} messages in {took:.2f} seconds")