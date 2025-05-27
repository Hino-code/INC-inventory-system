import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017"
DATABASE_NAME = os.getenv("DATABASE_NAME") or "inventorydb"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

async def delete_all_products():
    result = await db.products.delete_many({})
    print(f"Deleted {result.deleted_count} existing products.")

if __name__ == "__main__":
    asyncio.run(delete_all_products())
