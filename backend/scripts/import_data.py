# scripts/import_products_from_excel.py

import asyncio
from datetime import datetime
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017"
DATABASE_NAME = os.getenv("DATABASE_NAME") or "inventorydb"

# MongoDB client and database reference
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

# Excel file path - update as needed
EXCEL_FILE_PATH = r"C:\Users\bro\Downloads\sample_product.xlsx"

def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == 'true'
    return False

def parse_date(value):
    if pd.isna(value):
        return None
    if isinstance(value, datetime):
        return value
    try:
        return pd.to_datetime(value)
    except Exception:
        return None

async def delete_all_products():
    result = await db.products.delete_many({})
    print(f"Deleted {result.deleted_count} existing products.")

async def import_products_from_excel(file_path):
    print(f"Reading Excel file from {file_path}...")
    df = pd.read_excel(file_path, engine='openpyxl')

    products = []
    for _, row in df.iterrows():
        product = {
            "name": row.get("name"),
            "description": row.get("description", "") or "",
            "price": float(row.get("price")),
            "quantity": int(row.get("quantity")),
            "category": row.get("category", "General") or "General",
            "is_active": parse_bool(row.get("is_active")),
            "created_at": parse_date(row.get("created_at")),
            "expiration_date": parse_date(row.get("expiration_date")),
            "damaged_quantity": int(row.get("damaged_quantity") if not pd.isna(row.get("damaged_quantity")) else 0),
            "refill_threshold": int(row.get("refill_threshold") if not pd.isna(row.get("refill_threshold")) else 10),
        }
        products.append(product)

    if products:
        result = await db.products.insert_many(products)
        print(f"Inserted {len(result.inserted_ids)} products.")

async def main():
    await delete_all_products()
    await import_products_from_excel(EXCEL_FILE_PATH)

if __name__ == "__main__":
    asyncio.run(main())
