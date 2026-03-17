from fastapi import FastAPI
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import os

app = FastAPI()

# DynamoDB connection
dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name="ap-south-1"
)
electronics_table = dynamodb.Table("Electronics")
accessories_table = dynamodb.Table("Accessories")
furniture_table = dynamodb.Table("Furniture")


# 🔹 Helper to convert Decimal → float
def convert_decimal(item):
    for k, v in item.items():
        if isinstance(v, Decimal):
            item[k] = float(v)
    return item


# 🔹 Electronics API
@app.get("/electronics")
def get_electronics():
    response = electronics_table.scan()
    items = [convert_decimal(i) for i in response["Items"]]
    return {"Electronics": items}


# 🔹 Accessories API
@app.get("/accessories")
def get_accessories():
    response = accessories_table.scan()
    items = [convert_decimal(i) for i in response["Items"]]
    return {"Accessories": items}


# 🔹 Furniture API
@app.get("/furniture")
def get_furniture():
    response = furniture_table.scan()
    items = [convert_decimal(i) for i in response["Items"]]
    return {"Furniture": items}


# 🔹 Combined Top Products API
@app.get("/top-products")
def get_all_products():
    electronics = electronics_table.scan()["Items"]
    accessories = accessories_table.scan()["Items"]
    furniture = furniture_table.scan()["Items"]

    all_items = electronics + accessories + furniture
    all_items = [convert_decimal(i) for i in all_items]

    # Sort by total_amount descending
    sorted_items = sorted(all_items, key=lambda x: x["total_amount"], reverse=True)

    return {"top_products": sorted_items}