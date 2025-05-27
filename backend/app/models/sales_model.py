from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SaleRecord(BaseModel):
    product_id: str
    quantity_sold: int
    sale_price: float
    sale_date: Optional[datetime] = None  # Optional: filled automatically if missing
