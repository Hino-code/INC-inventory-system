from fastapi import APIRouter, HTTPException
from app.database.connection import db
from prophet import Prophet
import pandas as pd
from bson import ObjectId
from typing import List
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

async def fetch_sales(product_id: str):
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

def forecast_sales(sales_data: List[dict], product_id: str):
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

        # Make predictions for the next 30 days (Prophet will handle frequency automatically)
        future = model.make_future_dataframe(df, periods=30)  # Only `periods` passed, no freq
        forecast = model.predict(future)

        # Extract the forecasted values
        forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30).to_dict(orient='records')
        return {"forecast": forecast_data}

    except Exception as e:
        logger.error(f"Error during forecasting for product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during forecasting: {str(e)}")

@router.get("/forecast/{product_id}", response_model=dict)
async def get_sales_forecast(product_id: str):
    """Endpoint to get sales forecast for a given product."""
    
    # Validate if the product ID exists in the products collection
    if not await db.products.find_one({"_id": ObjectId(product_id)}):
        logger.error(f"Product ID {product_id} not found.")
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Fetch sales data for the product
    sales_data = await fetch_sales(product_id)
    
    if not sales_data:
        logger.error(f"No sales data found for product ID {product_id}.")
        raise HTTPException(status_code=404, detail="No sales data found for the product")

    # Forecast sales using Prophet
    forecast_result = forecast_sales(sales_data, product_id)

    if not forecast_result:
        logger.error(f"Forecasting failed for product {product_id}.")
        raise HTTPException(status_code=500, detail="Error during forecasting")

    return forecast_result
