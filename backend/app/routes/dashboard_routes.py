from fastapi import APIRouter, Depends, HTTPException, Query
from app.dependencies.auth import get_current_user
from app.database.connection import db
from datetime import datetime, timedelta

router = APIRouter()

def parse_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None

@router.get("/dashboard/summary")
async def dashboard_summary(date: str = Query(None), user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    # Filter by date if provided, else total
    filter_query = {}
    if date:
        start = parse_date(date)
        if not start:
            raise HTTPException(status_code=400, detail="Invalid date format")
        end = start + timedelta(days=1)
        filter_query = {"sale_date": {"$gte": start, "$lt": end}}

    pipeline = [
        {"$match": filter_query} if filter_query else {"$match": {}},
        {
            "$group": {
                "_id": None,
                "net_sales": {"$sum": {"$multiply": ["$quantity_sold", "$sale_price"]}},
                "transactions": {"$sum": 1}
            }
        }
    ]

    result = await db.sales.aggregate(pipeline).to_list(length=1)
    if result:
        net_sales = result[0].get("net_sales", 0)
        transactions = result[0].get("transactions", 0)
        average_net_sale = net_sales / transactions if transactions > 0 else 0
    else:
        net_sales = 0
        transactions = 0
        average_net_sale = 0

    # Placeholder for future extension: customers and payment types
    customers = []
    payment_types = []

    return {
        "net_sales": net_sales,
        "transactions": transactions,
        "gross_sales": net_sales,
        "average_net_sale": average_net_sale,
        "customers": customers,
        "payment_types": payment_types,
    }

@router.get("/dashboard/sales-data")
async def get_sales_data(days: int = 7, user=Depends(get_current_user)):
    """
    Returns aggregated net sales grouped by day for the last `days` days.
    """
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    end_date = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
    start_date = end_date - timedelta(days=days - 1)
    pipeline = [
        {"$match": {"sale_date": {"$gte": start_date, "$lte": end_date}}},
        {
            "$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$sale_date"}},
                "net_sales": {"$sum": {"$multiply": ["$quantity_sold", "$sale_price"]}},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    cursor = db.sales.aggregate(pipeline)
    results = []
    async for doc in cursor:
        results.append({"date": doc["_id"], "net_sales": doc["net_sales"]})

    return results

@router.get("/dashboard/customers-summary")
async def get_customers_summary(user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    total_customers = await db.customers.count_documents({})
    returning_customers_list = await db.orders.distinct("customer_id")
    returning_customers = len(returning_customers_list)

    return {
        "total_customers": total_customers,
        "returning_customers": returning_customers,
    }

@router.get("/dashboard/payment-types-summary")
async def get_payment_types_summary(user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    pipeline = [
        {
            "$group": {
                "_id": "$payment_type",
                "total_amount": {"$sum": "$amount"},
            }
        }
    ]

    cursor = db.payments.aggregate(pipeline)
    results = []
    async for doc in cursor:
        results.append({"payment_type": doc["_id"], "total_amount": doc["total_amount"]})

    return results
