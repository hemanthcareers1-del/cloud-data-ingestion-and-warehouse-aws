from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.ingestion.weather_api_ingestion import run as ingest_weather
from src.warehouse.redshift_loader import (
    get_redshift_connection,
    load_from_s3,
    validate_data,
)

import os

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def load_to_redshift_task():
    redshift_host = os.getenv("REDSHIFT_HOST")
    iam_role_arn = os.getenv("REDSHIFT_IAM_ROLE_ARN")

    if not redshift_host or not iam_role_arn:
        raise EnvironmentError("Missing Redshift connection details")

    conn = get_redshift_connection(redshift_host)
    load_from_s3(
        conn=conn,
        bucket=os.getenv("S3_BUCKET"),
        key=os.getenv("S3_OBJECT_KEY"),
        iam_role_arn=iam_role_arn,
    )
    validate_data(conn)
    conn.close()


with DAG(
    dag_id="weather_api_to_redshift_pipeline",
    default_args=DEFAULT_ARGS,
    description="Daily API to Redshift data pipeline",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["aws", "data-engineering"],
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_weather_api_data",
        python_callable=ingest_weather,
        op_kwargs={"city": "London"},
    )

    load_task = PythonOperator(
        task_id="load_data_to_redshift",
        python_callable=load_to_redshift_task,
    )

    ingest_task >> load_task
