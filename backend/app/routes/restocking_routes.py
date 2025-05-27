from fastapi import APIRouter, HTTPException
from app.database.connection import db
from prophet import Prophet
import pandas as pd
from bson import ObjectId
import logging

router = APIRouter()

# Set up logging for detailed error reporting
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

def calculate_ideal_stock(forecast_data, buffer_percentage=0.2):
    """Calculate the ideal stock level based on forecasted sales and buffer stock."""
    forecasted_sales = sum([forecast['yhat'] for forecast in forecast_data])  # Sum up forecasted sales
    buffer_stock = forecasted_sales * buffer_percentage
    ideal_stock = forecasted_sales + buffer_stock
    return ideal_stock

@router.get("/restock/{product_id}")
async def get_restock_suggestion(product_id: str):
    """Endpoint to get restocking suggestion for a product."""
    
    # Validate if the product ID exists in the products collection
    try:
        product = await db.products.find_one({"_id": ObjectId(product_id)})
        if not product:
            logger.error(f"Product ID {product_id} not found.")
            raise HTTPException(status_code=404, detail="Product not found")

        logger.debug(f"Product found: {product}")

        # Fetch sales data for the product
        sales_data = await fetch_sales(product_id)
        if not sales_data:
            logger.error(f"No sales data found for product ID {product_id}.")
            raise HTTPException(status_code=404, detail="No sales data found for the product")

        logger.debug(f"Sales data fetched: {sales_data}")

        # Use Prophet to forecast sales for the next 30 days
        df = pd.DataFrame(sales_data)
        df['ds'] = pd.to_datetime(df['ds'])

        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(df, periods=30)  # Forecast for next 30 days
        forecast = model.predict(future)

        # Calculate the ideal stock level based on the forecast
        forecast_data = forecast[['ds', 'yhat']].tail(30).to_dict(orient='records')
        ideal_stock = calculate_ideal_stock(forecast_data)

        # Get current stock for the product
        current_stock = product.get("stock", 0)
        restock_amount = ideal_stock - current_stock if current_stock < ideal_stock else 0

        return {
            "product_id": product_id,
            "product_name": product.get("name", "Unknown Product"),
            "current_stock": current_stock,
            "ideal_stock": ideal_stock,
            "restock_amount": restock_amount
        }

    except Exception as e:
        logger.error(f"Error during restocking suggestion for product {product_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during restocking suggestion: {str(e)}")
