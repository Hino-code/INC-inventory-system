import random
import datetime
import asyncio
from app.database.connection import db
from bson import ObjectId

# Random Sales Data Generator for All Products
def generate_random_sales(product_id):
    # Generate random date within the last 3 months
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=90)  # Last 3 months
    random_date = start_date + datetime.timedelta(days=random.randint(0, 90))

    # Generate random quantity sold (between 1 and 100)
    random_quantity_sold = random.randint(1, 100)

    # Create a sale document to insert into MongoDB
    sale = {
        "product_id": product_id,
        "date": random_date,
        "quantity_sold": random_quantity_sold
    }

    return sale

async def insert_random_sales():
    # Fetch all product IDs from the products collection
    products = await db.products.find({}, {"_id": 1}).to_list(length=None)

    # For each product, generate random sales data and insert into MongoDB
    for product in products:
        product_id = str(product["_id"])  # Get the product ID
        random_sales = generate_random_sales(product_id)

        # Insert the random sales data into MongoDB
        result = await db.sales.insert_one(random_sales)
        print(f"Inserted random sale for product {product_id} with sale ID: {result.inserted_id}")

async def main():
    print("Generating and inserting random sales data for all products...")
    await insert_random_sales()
    print("Random sales data insertion complete!")

if __name__ == "__main__":
    asyncio.run(main())
