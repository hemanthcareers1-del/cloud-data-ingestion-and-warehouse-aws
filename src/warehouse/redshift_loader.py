import os
import logging
import psycopg2
import boto3

from config.aws.config import (
    AWS_REGION,
    REDSHIFT_DB,
    REDSHIFT_USER,
    REDSHIFT_PORT,
    SECRETS_MANAGER_REDSHIFT_SECRET,
)

logging.basicConfig(level=logging.INFO)

def get_redshift_credentials():
    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    secret = client.get_secret_value(SecretId=SECRETS_MANAGER_REDSHIFT_SECRET)
    return eval(secret["SecretString"])


def get_redshift_connection(host: str):
    creds = get_redshift_credentials()
    return psycopg2.connect(
        dbname=REDSHIFT_DB,
        user=REDSHIFT_USER,
        password=creds["password"],
        host=host,
        port=REDSHIFT_PORT,
    )


def create_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS weather_data (
        city VARCHAR(50),
        temperature FLOAT,
        weather VARCHAR(50),
        humidity INT,
        timestamp TIMESTAMP
    );
    """
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()


def load_from_s3(conn, bucket: str, key: str, iam_role_arn: str):
    copy_query = f"""
    COPY weather_data
    FROM 's3://{bucket}/{key}'
    IAM_ROLE '{iam_role_arn}'
    CSV
    IGNOREHEADER 1;
    """
    with conn.cursor() as cur:
        cur.execute(copy_query)
        conn.commit()


def validate_data(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM weather_data;")
        count = cur.fetchone()[0]
        logging.info(f"Rows loaded into Redshift: {count}")
