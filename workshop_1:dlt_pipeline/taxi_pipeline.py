import dlt
import requests

BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

@dlt.resource(name="taxi_trips")
def taxi_trips():

    page = 1

    while True:
        response = requests.get(f"{BASE_URL}?page={page}")
        data = response.json()

        if not data:
            break

        yield data
        page += 1


def load_taxi_data():
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="taxi_data",
    )

    load_info = pipeline.run(taxi_trips())
    print(load_info)


if __name__ == "__main__":
    load_taxi_data()