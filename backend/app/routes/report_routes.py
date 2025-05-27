from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from app.dependencies.auth import get_current_user
from app.database.connection import db

router = APIRouter()

@router.get("/reports/expired-items")
async def expired_items_report(user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    today = datetime.utcnow()
    expired_products_cursor = db.products.find({
        "expiration_date": {"$lte": today},
        "is_active": True
    })

    expired_products = []
    async for product in expired_products_cursor:
        expired_products.append({
            "name": product.get("name"),
            "expiration_date": product.get("expiration_date"),
            "quantity": product.get("quantity"),
            "category": product.get("category")
        })

    return {"expired_items": expired_products}

@router.get("/reports/low-stock")
async def low_stock_report(user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    low_stock_cursor = db.products.aggregate([
        {
            "$match": {
                "$expr": {
                    "$lte": ["$quantity", "$refill_threshold"]
                },
                "is_active": True
            }
        },
        {
            "$project": {
                "name": 1,
                "quantity": 1,
                "refill_threshold": 1,
                "category": 1
            }
        }
    ])

    low_stock_items = []
    async for item in low_stock_cursor:
        low_stock_items.append(item)

    return {"low_stock_items": low_stock_items}

@router.get("/reports/expired-items/pdf")
async def expired_items_pdf_report(user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    today = datetime.utcnow()
    cursor = db.products.find({
        "expiration_date": {"$lte": today},
        "is_active": True
    })

    expired_products = []
    async for product in cursor:
        expired_products.append(product)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Expired Products Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for prod in expired_products:
        name = prod.get("name", "N/A")
        expiry = prod.get("expiration_date")
        expiry_str = expiry.strftime("%Y-%m-%d") if expiry else "N/A"
        quantity = prod.get("quantity", 0)
        line = f"{name} | Expiry: {expiry_str} | Quantity: {quantity}"
        pdf.cell(0, 10, line, ln=True)

    pdf_output_str = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_output_str)
    buffer.seek(0)

    headers = {
        "Content-Disposition": "attachment; filename=expired_products_report.pdf"
    }

    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)

@router.get("/reports/summary")
async def summary_report(user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    today = datetime.utcnow()

    total_products = await db.products.count_documents({})

    total_expired = await db.products.count_documents({
        "expiration_date": {"$lte": today},
        "is_active": True
    })

    total_low_stock = await db.products.count_documents({
        "$expr": {"$lte": ["$quantity", "$refill_threshold"]},
        "is_active": True
    })

    total_damaged = await db.products.count_documents({
        "damaged_quantity": {"$gt": 0},
        "is_active": True
    })

    categories_agg = db.products.aggregate([
        {"$match": {"is_active": True}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ])

    categories_count = {}
    async for cat in categories_agg:
        categories_count[cat["_id"]] = cat["count"]

    return {
        "total_products": total_products,
        "total_expired": total_expired,
        "total_low_stock": total_low_stock,
        "total_damaged": total_damaged,
        "products_by_category": categories_count
    }

@router.get("/reports/summary/pdf")
async def summary_report_pdf(user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Access denied")

    today = datetime.utcnow()

    total_products = await db.products.count_documents({})

    total_expired = await db.products.count_documents({
        "expiration_date": {"$lte": today},
        "is_active": True
    })

    total_low_stock = await db.products.count_documents({
        "$expr": {"$lte": ["$quantity", "$refill_threshold"]},
        "is_active": True
    })

    total_damaged = await db.products.count_documents({
        "damaged_quantity": {"$gt": 0},
        "is_active": True
    })

    categories_agg = db.products.aggregate([
        {"$match": {"is_active": True}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ])

    categories_count = {}
    async for cat in categories_agg:
        categories_count[cat["_id"]] = cat["count"]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Inventory Summary Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Total Products: {total_products}", ln=True)
    pdf.cell(0, 10, f"Total Expired Products: {total_expired}", ln=True)
    pdf.cell(0, 10, f"Total Low Stock Products: {total_low_stock}", ln=True)
    pdf.cell(0, 10, f"Total Damaged Products: {total_damaged}", ln=True)
    pdf.ln(10)

    pdf.cell(0, 10, "Products by Category:", ln=True)
    for category, count in categories_count.items():
        pdf.cell(0, 10, f"  - {category}: {count}", ln=True)

    pdf_output_str = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_output_str)
    buffer.seek(0)

    headers = {
        "Content-Disposition": "attachment; filename=inventory_summary_report.pdf"
    }

    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)
