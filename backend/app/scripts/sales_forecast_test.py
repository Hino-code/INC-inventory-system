import asyncio
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from app.database.connection import db
from bson import ObjectId

# Specify the product ID for forecasting (will loop through all products)
PRODUCT_ID = "682f25441b749bb1e7895575"  # Replace with an actual product ID

async def fetch_sales(product_id):
    """Fetch sales data from MongoDB for a given product."""
    cursor = db.sales.find({"product_id": product_id})
    sales = []
    async for doc in cursor:
        print(f"Fetched sale: {doc}")  # Print the fetched sales data for debugging
        sales.append({
            "ds": doc["date"],  # Ensure this is an ISO date string or datetime
            "y": doc["quantity_sold"]
        })
    return sales

def forecast_sales(sales_data, product_id):
    """Run sales forecasting using Prophet and plot the results."""
    df = pd.DataFrame(sales_data)
    df['ds'] = pd.to_datetime(df['ds'])  # Ensure 'ds' is in datetime format

    # Check if we have enough valid rows
    if df.shape[0] < 2:
        print(f"Not enough data for forecasting (less than 2 valid rows) for product {product_id}.")
        return

    # Create and fit the Prophet model
    model = Prophet()
    model.fit(df)

    # Make predictions for the next 30 days (using correct method)
    future = model.make_future_dataframe(df, periods=30)  # Prophet will handle the frequency automatically
    forecast = model.predict(future)

    # Plot the forecast
    model.plot(forecast)
    plt.title(f"Sales Forecast for Product {product_id}")
    plt.show()

async def main():
    """Main function to fetch data and run the forecasting for all products."""
    sales_data = await fetch_sales(PRODUCT_ID)

    if not sales_data:
        print(f"No sales data found for product ID {PRODUCT_ID}. Skipping forecast.")
        return

    print(f"Running sales forecast for product ID {PRODUCT_ID}...")
    forecast_sales(sales_data, PRODUCT_ID)

if __name__ == "__main__":
    asyncio.run(main())
