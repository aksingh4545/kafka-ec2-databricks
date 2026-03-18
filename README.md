# Kafka EC2 Databricks Pipeline

This repository demonstrates an **end-to-end real-time data pipeline** that processes streaming events from Kafka, transforms them using Databricks PySpark, stores raw and aggregated data in AWS services, and exposes the results via a FastAPI service.

## Architecture Overview

```
┌─────────────┐     ┌──────────────────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────┐
│  Kafka on   │────▶│  Databricks PySpark  │────▶│  Amazon  │────▶│  DynamoDB   │────▶│ FastAPI  │
│  EC2 Instance│     │  (Structured Stream)│     │   S3     │     │ (Aggregated)│     │   API    │
└─────────────┘     └──────────────────────┘     └──────────┘     └─────────────┘     └──────────┘
     (Producer)            (Processing)          (Raw Data)        (Query Layer)       (Consumption)
```

### Data Flow

1. **Kafka (EC2)**: Produces streaming events (e.g., product transactions)
2. **Databricks PySpark**: Consumes Kafka events, parses JSON, performs transformations
3. **Amazon S3**: Stores raw event data for archival and batch processing
4. **DynamoDB**: Stores aggregated product data for low-latency queries
5. **FastAPI**: Exposes REST endpoints to query aggregated data

## Repository Contents

| File/Directory | Description |
|----------------|-------------|
| `ec2.ipynb` | Step-by-step Jupyter notebook to set up and configure Kafka on an AWS EC2 instance |
| `pyspark.ipynb` | Databricks PySpark streaming workflow that reads Kafka events, parses JSON, and writes to S3 + DynamoDB |
| `app.py` | FastAPI service that reads aggregated data from DynamoDB and exposes product APIs |
| `ss/` | Screenshots documenting the pipeline setup and API outputs |

## Pipeline Components

### 1. Kafka on EC2

The Kafka broker runs on an AWS EC2 instance and acts as the event producer. Messages are published to Kafka topics in JSON format.

**Setup**: See `ec2.ipynb` for detailed EC2 instance configuration, Kafka installation, and topic creation.

### 2. Databricks PySpark Streaming

Databricks consumes Kafka messages using **Structured Streaming**. The notebook demonstrates:

- Kafka connection configuration
- JSON message parsing
- Data transformations and aggregations
- Writing to S3 (raw data lake)
- Writing to DynamoDB (aggregated results)

**Key Features**:
- Real-time stream processing
- Schema enforcement on JSON payloads
- Checkpointing for fault tolerance

### 3. Amazon S3 (Raw Data Lake)

All raw Kafka events are archived to S3 for:
- Historical analysis
- Reprocessing capabilities
- Compliance and auditing

### 4. DynamoDB (Aggregated Data)

Aggregated product data is stored in three DynamoDB tables:

| Table | Description |
|-------|-------------|
| `Electronics` | Electronic product transactions |
| `Accessories` | Accessory product transactions |
| `Furniture` | Furniture product transactions |

Each record contains product details and computed metrics (e.g., `total_amount`).

### 5. FastAPI Service

The API layer provides RESTful endpoints to query aggregated data from DynamoDB.

#### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/electronics` | GET | Returns all records from the `Electronics` table |
| `/accessories` | GET | Returns all records from the `Accessories` table |
| `/furniture` | GET | Returns all records from the `Furniture` table |
| `/top-products` | GET | Merges all categories and returns products sorted by `total_amount` (descending) |

#### Features

- Automatic conversion of DynamoDB `Decimal` types to JSON-compatible `float` values
- Cross-category aggregation in `/top-products`
- Error handling for missing tables or items

## Local Run Instructions

### Prerequisites

- Python 3.8+
- AWS account with configured credentials
- DynamoDB tables created (`Electronics`, `Accessories`, `Furniture`)

### 1. Install Dependencies

```bash
pip install fastapi uvicorn boto3
```

### 2. Configure AWS Credentials

**Option A: Update `app.py` directly** (for development only)
```python
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='YOUR_REGION'
)
```

**Option B: Environment Variables** (recommended)
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region
```

**Option C: IAM Role** (for production on EC2/ECS/Lambda)

### 3. Start the API Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### 4. Test Endpoints

Using `curl`:
```bash
curl http://localhost:8000/electronics
curl http://localhost:8000/accessories
curl http://localhost:8000/furniture
curl http://localhost:8000/top-products
```

Using a browser or API client (e.g., Postman):
- Navigate to `http://localhost:8000/docs` for interactive Swagger UI
- Navigate to `http://localhost:8000/redoc` for ReDoc documentation

## Screenshots

See the `ss/` directory for visual documentation:

- `kafka-consumer.png` — Kafka consumer output
- `databricks.png` — Databricks notebook execution
- `s3.png` — S3 bucket with raw data
- `dynamoDB.png` — DynamoDB table contents
- `api-working.png` — API endpoint responses

## Security Best Practices

- **Never commit AWS credentials** to version control
- Use **IAM roles** for EC2, Lambda, or ECS deployments
- Enable **encryption at rest** for DynamoDB and S3
- Use **VPC endpoints** for private AWS service access
- Implement **API authentication** for production deployments

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ResourceNotFoundException` | Ensure DynamoDB tables exist in the configured region |
| `CredentialsError` | Verify AWS credentials are properly configured |
| `Connection refused` (Kafka) | Check EC2 security group allows Kafka port (9092) |
| Decimal serialization error | The API already handles this; ensure you're using the latest `app.py` |

## Future Enhancements

- [ ] Add authentication (JWT/OAuth2) to FastAPI endpoints
- [ ] Implement Kafka schema registry (Avro/Protobuf)
- [ ] Add monitoring with CloudWatch or Prometheus
- [ ] Containerize services with Docker
- [ ] Add CI/CD pipeline for automated deployments

## License

MIT License
