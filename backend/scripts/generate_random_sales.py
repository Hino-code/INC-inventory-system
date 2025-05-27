import asyncio
import random
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") or "mongodb://localhost:27017"
DATABASE_NAME = os.getenv("DATABASE_NAME") or "inventorydb"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

NUM_SALES_TO_GENERATE = 1000  # Adjust for how many random sales you want
MAX_QUANTITY_PER_SALE = 5

async def generate_random_sales():
    products = []
    async for product in db.products.find({"quantity": {"$gt": 0}}):
        products.append(product)

    if not products:
        print("No products found with positive stock to generate sales.")
        return

    sales = []
    now = datetime.utcnow()

    for _ in range(NUM_SALES_TO_GENERATE):
        product = random.choice(products)
        max_qty = min(product.get("quantity", 1), MAX_QUANTITY_PER_SALE)
        quantity_sold = random.randint(1, max_qty)

        # Random sale date within last 60 days
        sale_date = now - timedelta(days=random.randint(0, 60), hours=random.randint(0, 23), minutes=random.randint(0, 59))

        sale = {
            "product_id": product["_id"],
            "quantity_sold": quantity_sold,
            "sale_price": float(product.get("price", 0)),
            "sale_date": sale_date,
            # Optional: no user ID assigned for testing
        }
        sales.append(sale)

    result = await db.sales.insert_many(sales)
    print(f"Inserted {len(result.inserted_ids)} random sales documents.")

async def main():
    await generate_random_sales()

if __name__ == "__main__":
    asyncio.run(main())
