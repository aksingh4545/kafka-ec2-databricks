# Kafka EC2 Databricks Pipeline

This repository demonstrates an end-to-end data pipeline:

**Kafka (EC2) → Databricks (PySpark Streaming) → S3 (raw) + DynamoDB (aggregated) → FastAPI APIs**

## Repository Contents

- `ec2.ipynb` — step-by-step guide to set up Kafka on an AWS EC2 instance.
- `pyspark.ipynb` — Databricks PySpark streaming workflow that reads Kafka events, parses JSON, and writes outputs.
- `app.py` — FastAPI service that reads aggregated data from DynamoDB and exposes product APIs.
- `ss/` — screenshots of pipeline and API outputs.

## FastAPI Service

The API connects to three DynamoDB tables:

- `Electronics`
- `Accessories`
- `Furniture`

### Endpoints

- `GET /electronics` — returns all records from `Electronics`
- `GET /accessories` — returns all records from `Accessories`
- `GET /furniture` — returns all records from `Furniture`
- `GET /top-products` — merges all categories and sorts by `total_amount` descending

The API also converts DynamoDB `Decimal` values to JSON-friendly `float` values.

## Local Run Instructions

### 1) Install dependencies

```bash
pip install fastapi uvicorn boto3
```

### 2) Configure AWS credentials

In `app.py`, update the DynamoDB client configuration (or switch to environment/IAM-based credentials):

- `aws_access_key_id`
- `aws_secret_access_key`
- `region_name`

### 3) Start the API server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 4) Test endpoints

```bash
curl http://localhost:8000/electronics
curl http://localhost:8000/accessories
curl http://localhost:8000/furniture
curl http://localhost:8000/top-products
```

## Notes

- Ensure the DynamoDB tables exist in the configured AWS region.
- For production, avoid hardcoding AWS credentials; prefer IAM roles or environment variables.
- If your data model changes, update sorting/field assumptions in `/top-products`.
