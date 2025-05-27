from app.database.connection import db
from app.models.sales_model import SaleRecord
from fastapi import HTTPException, status
from bson import ObjectId
from datetime import datetime

async def record_sale(sale: SaleRecord, user):
    if user.get("role") not in ["employee", "owner"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if not ObjectId.is_valid(sale.product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = await db.products.find_one({"_id": ObjectId(sale.product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.get("quantity", 0) < sale.quantity_sold:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    sale_doc = {
        "product_id": ObjectId(sale.product_id),
        "quantity_sold": sale.quantity_sold,
        "sale_price": sale.sale_price,
        "sale_date": sale.sale_date or datetime.utcnow(),
        "sold_by_user_id": ObjectId(user.get("user_id"))
    }

    result = await db.sales.insert_one(sale_doc)

    await db.products.update_one(
        {"_id": ObjectId(sale.product_id)},
        {"$inc": {"quantity": -sale.quantity_sold}}
    )

    return {"message": "Sale recorded successfully", "sale_id": str(result.inserted_id)}
