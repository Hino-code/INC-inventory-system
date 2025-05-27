from app.database.connection import db
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime

async def best_selling_products(limit=10, user=None):
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    pipeline = [
        {
            "$group": {
                "_id": "$product_id",
                "total_quantity": {"$sum": "$quantity_sold"},
                "total_revenue": {"$sum": {"$multiply": ["$quantity_sold", "$sale_price"]}}
            }
        },
        {"$sort": {"total_quantity": -1}},
        {"$limit": limit},
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "_id",
                "as": "product"
            }
        },
        {"$unwind": "$product"},
        {
            "$project": {
                "product_name": "$product.name",
                "total_quantity": 1,
                "total_revenue": 1
            }
        }
    ]

    cursor = db.sales.aggregate(pipeline)
    results = []
    async for doc in cursor:
        results.append(doc)

    return results
