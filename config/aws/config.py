import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-2")

S3_BUCKET_PREFIX = "cloud-data-ingestion"
S3_RAW_PREFIX = "raw/weather"

REDSHIFT_DB = os.getenv("REDSHIFT_DB", "dev")
REDSHIFT_USER = os.getenv("REDSHIFT_USER", "awsuser")
REDSHIFT_PORT = int(os.getenv("REDSHIFT_PORT", 5439))

SECRETS_MANAGER_REDSHIFT_SECRET = os.getenv(
    "REDSHIFT_SECRET_NAME",
    "redshift-cluster-password"
)
