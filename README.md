# Cloud Data Ingestion and Warehouse on AWS

## Overview

This project implements a production-style, end-to-end data engineering pipeline on AWS.

The pipeline ingests data from an external REST API, performs validation and transformation, and loads analytics-ready data into Amazon Redshift on a daily schedule.

The design follows enterprise data engineering best practices such as modular code organization, secure credential handling, data quality validation, and workflow orchestration.

---

## Architecture

![Architecture Diagram](docs/architecture.png)

### Pipeline Flow
1. External REST API (Weather API)
2. Python-based ingestion and transformation
3. Amazon S3 (raw data storage)
4. Amazon Redshift (analytics warehouse)
5. Apache Airflow (orchestration & scheduling)

### Key AWS Services Used
- Amazon S3 for raw data storage
- Amazon Redshift for analytical data warehousing
- AWS IAM for secure access control
- AWS Secrets Manager for credential management
- Apache Airflow for workflow orchestration

---

## Project Structure

```text
cloud-data-ingestion-and-warehouse-aws/
├── src/
│   ├── ingestion/        # API ingestion and transformation logic
│   ├── warehouse/        # Redshift loading and validation
│   ├── orchestration/    # Airflow DAGs
│
├── config/
│   ├── aws/              # AWS configuration
│   └── .env.example      # Environment variable template
│
├── tests/                # Validation and testing (extensible)
├── requirements.txt
└── README.md

---

## Challenges & Solutions

### 1. Secure Credential Management
Challenge: 
Managing database credentials and API keys securely without hardcoding sensitive values in source code.

Solution:  
Integrated AWS Secrets Manager to securely generate, store, and retrieve Redshift credentials at runtime. Environment variables and configuration templates (`.env.example`) were used to separate secrets from application logic, following cloud security best practices.

---

### 2. Data Quality and Reliability
Challenge:
Ensuring that ingested API data is complete, schema-consistent, and analytics-ready before loading into the data warehouse.

Solution:
Implemented data validation checks at multiple stages, including schema validation, null checks, and row-count verification prior to Redshift ingestion. Post-load validation queries were executed in Redshift to confirm schema consistency and data integrity.

---

### 3. Orchestration and Fault Tolerance
Challenge: 
Coordinating multiple dependent steps (ingestion, validation, load) while handling failures gracefully.

Solution:  
Used Apache Airflow DAGs to orchestrate the pipeline with clearly defined task dependencies, retries, and scheduling. Centralized logging and exception handling improved observability and simplified debugging.

---

### 4. Cloud Resource Management
Challenge:
Avoiding manual AWS console setup and ensuring reproducibility of infrastructure.

Solution:  
Provisioned and managed AWS resources such as S3 buckets, IAM roles, Secrets Manager, and Redshift clusters programmatically using Boto3, enabling repeatable and automated infrastructure setup.


---

## Azure to AWS Service Mapping



| Azure Service | AWS Equivalent | Usage in This Project |
|---------------|---------------|-----------------------|
| Azure Data Factory | AWS Glue / Apache Airflow | Pipeline orchestration and scheduling |
| Azure Data Lake Storage (ADLS) | Amazon S3 | Raw data storage and staging |
| Azure Synapse Analytics | Amazon Redshift | Analytical data warehouse |
| Azure Key Vault | AWS Secrets Manager | Secure credential storage |
| Azure Monitor / Log Analytics | CloudWatch / Logging | Observability and debugging |
| Managed Identity | IAM Roles | Secure service-to-service access |


