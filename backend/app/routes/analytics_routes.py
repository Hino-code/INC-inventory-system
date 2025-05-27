from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.auth import get_current_user
from app.database.connection import db
from bson import ObjectId

router = APIRouter()

def convert_objectid_to_str(doc):
    if isinstance(doc, list):
        return [convert_objectid_to_str(d) for d in doc]
    if isinstance(doc, dict):
        new_doc = {}
        for k, v in doc.items():
            if isinstance(v, ObjectId):
                new_doc[k] = str(v)
            elif isinstance(v, (dict, list)):
                new_doc[k] = convert_objectid_to_str(v)
            else:
                new_doc[k] = v
        return new_doc
    return doc

@router.get("/analytics/best-sellers")
async def best_sellers_report(limit: int = 10, user=Depends(get_current_user)):
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

    results = convert_objectid_to_str(results)

    return results
