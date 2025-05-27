# app/routes/employee_routes.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from app.dependencies.auth import get_current_user
from app.database.connection import db

router = APIRouter()

# Fetch employee profile data
@router.get("/employee/data")
async def get_employee_data(user=Depends(get_current_user)):
    if user.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    employee_data = {
        "name": user.get("name", "Employee Name"),
        "role": user.get("role", "employee"),
    }
    return employee_data

# View all active products
@router.get("/employee/products")
async def view_products(user=Depends(get_current_user)):
    if user.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    products = []
    async for product in db.products.find({"is_active": True}):
        product["_id"] = str(product["_id"])
        products.append(product)
    return {"products": products}

# Get expired items
@router.get("/employee/reports/expired")
async def expired_items(user=Depends(get_current_user)):
    if user.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    today = datetime.utcnow()
    items = []
    cursor = db.products.find({
        "expiration_date": {"$lte": today},
        "is_active": True
    })
    async for item in cursor:
        items.append(item)
    return {"expired_items": items}

# Get low stock items
@router.get("/employee/reports/low-stock")
async def low_stock(user=Depends(get_current_user)):
    if user.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    items = []
    cursor = db.products.aggregate([
        {
            "$match": {
                "$expr": {"$lte": ["$quantity", "$refill_threshold"]},
                "is_active": True
            }
        }
    ])
    async for item in cursor:
        items.append(item)
    return {"low_stock_items": items}

# Get damaged items
@router.get("/employee/reports/damaged")
async def damaged_items(user=Depends(get_current_user)):
    if user.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    items = []
    cursor = db.products.find({
        "damaged_quantity": {"$gt": 0},
        "is_active": True
    })
    async for item in cursor:
        items.append(item)
    return {"damaged_items": items}

# PDF report: most damaged items
@router.get("/employee/reports/damaged/pdf")
async def damaged_items_pdf(user=Depends(get_current_user)):
    if user.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    items = []
    cursor = db.products.find({
        "damaged_quantity": {"$gt": 0},
        "is_active": True
    }).sort("damaged_quantity", -1).limit(10)
    async for item in cursor:
        items.append(item)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Top Damaged Products", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for item in items:
        line = f"{item.get('name', 'N/A')} | Damaged: {item.get('damaged_quantity', 0)}"
        pdf.cell(0, 10, line, ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)

    headers = {"Content-Disposition": "attachment; filename=damaged_products_report.pdf"}
    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)

# PDF report: most unsold items
@router.get("/employee/reports/unsold/pdf")
async def unsold_items_pdf(user=Depends(get_current_user)):
    if user.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    items = []
    cursor = db.products.find({
        "sold_quantity": {"$lte": 0},
        "is_active": True
    })
    async for item in cursor:
        items.append(item)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Most Unsold Products", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for item in items:
        line = f"{item.get('name', 'N/A')} | Sold: {item.get('sold_quantity', 0)}"
        pdf.cell(0, 10, line, ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)

    headers = {"Content-Disposition": "attachment; filename=unsold_products_report.pdf"}
    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)

# Summary PDF Report
@router.get("/employee/reports/summary/pdf")
async def employee_summary_pdf(user=Depends(get_current_user)):
    if user.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    today = datetime.utcnow()

    expired = await db.products.count_documents({
        "expiration_date": {"$lte": today},
        "is_active": True
    })

    low_stock = await db.products.count_documents({
        "$expr": {"$lte": ["$quantity", "$refill_threshold"]},
        "is_active": True
    })

    damaged = await db.products.count_documents({
        "damaged_quantity": {"$gt": 0},
        "is_active": True
    })

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Employee Inventory Summary", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Expired Products: {expired}", ln=True)
    pdf.cell(0, 10, f"Low Stock Products: {low_stock}", ln=True)
    pdf.cell(0, 10, f"Damaged Products: {damaged}", ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)

    headers = {"Content-Disposition": "attachment; filename=employee_summary_report.pdf"}
    return StreamingResponse(buffer, media_type="application/pdf", headers=headers)
