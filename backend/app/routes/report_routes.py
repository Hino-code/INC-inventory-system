# app/routes/report_routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from app.dependencies.auth import get_current_user
from app.database.connection import db

router = APIRouter()

def _stream_pdf(pdf: FPDF, filename: str):
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buf = BytesIO(pdf_bytes)
    buf.seek(0)
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(buf, media_type="application/pdf", headers=headers)

# JSON endpoints (unchanged)…
@router.get("/reports/expired-items")
async def expired_items_report(user=Depends(get_current_user)):
    if user.get("role") not in ("owner", "employee"):
        raise HTTPException(403, "Access denied")
    today = datetime.utcnow()
    cursor = db.products.find({
        "expiration_date": {"$lte": today},
        "is_active": True
    })
    expired = []
    async for p in cursor:
        expired.append({
            "name": p["name"],
            "expiration_date": p["expiration_date"],
            "quantity": p["quantity"],
            "category": p["category"]
        })
    return {"expired_items": expired}

@router.get("/reports/low-stock")
async def low_stock_report(user=Depends(get_current_user)):
    if user.get("role") not in ("owner", "employee"):
        raise HTTPException(403, "Access denied")
    cursor = db.products.aggregate([
        {"$match": {
            "$expr": {"$lte": ["$quantity", "$refill_threshold"]},
            "is_active": True
        }}
    ])
    items = []
    async for p in cursor:
        items.append({
            "name": p["name"],
            "quantity": p["quantity"],
            "refill_threshold": p["refill_threshold"],
            "category": p["category"]
        })
    return {"low_stock_items": items}

@router.get("/reports/summary")
async def summary_report(user=Depends(get_current_user)):
    if user.get("role") not in ("owner", "employee"):
        raise HTTPException(403, "Access denied")
    today = datetime.utcnow()
    total_products = await db.products.count_documents({})
    total_expired  = await db.products.count_documents({
        "expiration_date": {"$lte": today}, "is_active": True
    })
    total_low     = await db.products.count_documents({
        "$expr": {"$lte": ["$quantity", "$refill_threshold"]},
        "is_active": True
    })
    total_damaged = await db.products.count_documents({
        "damaged_quantity": {"$gt": 0}, "is_active": True
    })
    agg = db.products.aggregate([
        {"$match": {"is_active": True}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ])
    by_cat = {}
    async for c in agg:
        by_cat[c["_id"]] = c["count"]
    return {
        "total_products": total_products,
        "total_expired": total_expired,
        "total_low_stock": total_low,
        "total_damaged": total_damaged,
        "products_by_category": by_cat
    }


# — PDF endpoints (now allowing employees) —

@router.get("/reports/expired-items/pdf")
async def expired_items_pdf_report(user=Depends(get_current_user)):
    if user.get("role") not in ("owner", "employee"):
        raise HTTPException(403, "Access denied")
    today = datetime.utcnow()
    cursor = db.products.find({
        "expiration_date": {"$lte": today},
        "is_active": True
    })
    expired = []
    async for p in cursor:
        expired.append(p)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Expired Products Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for prod in expired:
        exp_str = prod.get("expiration_date", "").strftime("%Y-%m-%d")
        line = f"{prod.get('name')} | Expiry: {exp_str} | Quantity: {prod.get('quantity', 0)}"
        pdf.cell(0, 10, line, ln=True)

    return _stream_pdf(pdf, "expired_products_report.pdf")


@router.get("/reports/low-stock/pdf")
async def low_stock_pdf_report(user=Depends(get_current_user)):
    if user.get("role") not in ("owner", "employee"):
        raise HTTPException(403, "Access denied")
    cursor = db.products.aggregate([
        {"$match": {
            "$expr": {"$lte": ["$quantity", "$refill_threshold"]},
            "is_active": True
        }}
    ])
    low_stock = []
    async for p in cursor:
        low_stock.append(p)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Low Stock Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for prod in low_stock:
        line = (
            f"{prod.get('name')} | Quantity: {prod.get('quantity',0)}"
            f" | Threshold: {prod.get('refill_threshold',0)}"
        )
        pdf.cell(0, 10, line, ln=True)

    return _stream_pdf(pdf, "low_stock_report.pdf")


@router.get("/reports/summary/pdf")
async def summary_report_pdf(user=Depends(get_current_user)):
    if user.get("role") not in ("owner", "employee"):
        raise HTTPException(403, "Access denied")
    today = datetime.utcnow()
    total_products = await db.products.count_documents({})
    total_expired  = await db.products.count_documents({
        "expiration_date": {"$lte": today}, "is_active": True
    })
    total_low     = await db.products.count_documents({
        "$expr": {"$lte": ["$quantity", "$refill_threshold"]},
        "is_active": True
    })
    total_damaged = await db.products.count_documents({
        "damaged_quantity": {"$gt": 0}, "is_active": True
    })
    agg = db.products.aggregate([
        {"$match": {"is_active": True}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ])
    by_cat = {}
    async for c in agg:
        by_cat[c["_id"]] = c["count"]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Inventory Summary Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Total Products: {total_products}", ln=True)
    pdf.cell(0, 10, f"Total Expired Products: {total_expired}", ln=True)
    pdf.cell(0, 10, f"Total Low Stock Products: {total_low}", ln=True)
    pdf.cell(0, 10, f"Total Damaged Products: {total_damaged}", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, "Products by Category:", ln=True)
    for cat, cnt in by_cat.items():
        pdf.cell(0, 10, f"  - {cat}: {cnt}", ln=True)

    return _stream_pdf(pdf, "inventory_summary_report.pdf")
