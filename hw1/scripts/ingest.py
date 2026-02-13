import pandas as pd
from sqlalchemy import create_engine

#  
user = "postgres"
password = "postgres"
host = "db"
port = "5432"
db = "ny_taxi"

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

#  trip data
df_trips = pd.read_parquet("/data/green_tripdata_2025-11.parquet")

df_trips.to_sql(
    name="green_taxi_trips",
    con=engine,
    if_exists="replace",
    index=False
)

print("Trips loaded")

#  zones
df_zones = pd.read_csv("/data/taxi_zone_lookup.csv")

df_zones.to_sql(
    name="zones",
    con=engine,
    if_exists="replace",
    index=False
)

print("Zones loaded")

