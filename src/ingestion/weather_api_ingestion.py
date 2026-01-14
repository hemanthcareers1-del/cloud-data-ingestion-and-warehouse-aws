import os
import uuid
import logging
import requests
import boto3
import pandas as pd
from io import StringIO

from config.aws.config import AWS_REGION, S3_BUCKET_PREFIX, S3_RAW_PREFIX

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_weather_data(city: str, api_key: str) -> dict:
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def transform_weather_data(payload: dict) -> pd.DataFrame:
    data = {
        "city": payload["name"],
        "temperature": payload["main"]["temp"],
        "weather": payload["weather"][0]["description"],
        "humidity": payload["main"]["humidity"],
        "timestamp": pd.to_datetime("now"),
    }
    return pd.DataFrame([data])


def upload_to_s3(df: pd.DataFrame, bucket: str, key: str) -> None:
    s3 = boto3.client("s3", region_name=AWS_REGION)
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())


def run(city: str) -> None:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise EnvironmentError("WEATHER_API_KEY is not set")

    bucket_name = f"{S3_BUCKET_PREFIX}-{uuid.uuid4().hex[:8]}"
    object_key = f"{S3_RAW_PREFIX}/weather_{uuid.uuid4().hex}.csv"

    s3 = boto3.client("s3", region_name=AWS_REGION)
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
    )

    logging.info("Fetching weather data from API")
    payload = fetch_weather_data(city, api_key)

    logging.info("Transforming API payload")
    df = transform_weather_data(payload)

    logging.info("Uploading data to S3")
    upload_to_s3(df, bucket_name, object_key)

    logging.info("Ingestion completed successfully")


if __name__ == "__main__":
    run(city="London")
