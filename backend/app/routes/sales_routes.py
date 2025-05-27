from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.models.sales_model import SaleRecord
from app.controllers.sales_controller import record_sale

router = APIRouter()

@router.post("/sales", status_code=201)
async def create_sale(sale: SaleRecord, user=Depends(get_current_user)):
    return await record_sale(sale, user)
