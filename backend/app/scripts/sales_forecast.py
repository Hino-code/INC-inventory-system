import asyncio
from http.client import HTTPException
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from app.database.connection import db
from bson import ObjectId
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Specify the product ID for forecasting (change it to the actual product ID)
PRODUCT_ID = "6823f93bf389331cde211425"  # Replace with actual product ID from your DB

async def fetch_sales(product_id):
    """Fetch sales data from MongoDB for a given product."""
    cursor = db.sales.find({"product_id": product_id})
    sales = []
    async for doc in cursor:
        logger.debug(f"Fetched sale: {doc}")  # Log the fetched sales data for debugging
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
        logger.error(f"Not enough data for forecasting (less than 2 valid rows) for product {product_id}.")
        return {"message": f"Not enough data for forecasting (less than 2 valid rows) for product {product_id}."}

    try:
        # Create and fit the Prophet model
        model = Prophet()
        model.fit(df)

        # Make predictions for the next 30 days (using correct method)
        future = model.make_future_dataframe(df, periods=30)  # Only `periods` passed, no freq
        forecast = model.predict(future)

        # Extract the forecasted values
        forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30).to_dict(orient='records')
        return {"forecast": forecast_data}

    except Exception as e:
        logger.error(f"Error during forecasting for product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during forecasting: {str(e)}")

async def main():
    """Main function to fetch data and run the forecasting for all products."""
    sales_data = await fetch_sales(PRODUCT_ID)

    if not sales_data:
        logger.error(f"No sales data found for product ID {PRODUCT_ID}.")
        return {"message": f"No sales data found for product ID {PRODUCT_ID}."}

    logger.info(f"Running sales forecast for product ID {PRODUCT_ID}...")
    return forecast_sales(sales_data, PRODUCT_ID)

if __name__ == "__main__":
    asyncio.run(main())
