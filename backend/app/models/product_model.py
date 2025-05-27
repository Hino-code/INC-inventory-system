from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    price: float
    stock_quantity: int = Field(..., alias="quantity")  # for API compatibility
    category: str = "General"
    is_active: bool = True
    expiration_date: Optional[datetime] = None
    damaged_quantity: Optional[int] = 0
    refill_threshold: Optional[int] = 10

    class Config:
        allow_population_by_field_name = True

class Product(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str] = ""
    price: float
    stock_quantity: int = Field(..., alias="quantity")
    category: str = "General"
    is_active: bool = True
    created_at: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    damaged_quantity: Optional[int] = 0
    refill_threshold: Optional[int] = 10

    class Config:
        allow_population_by_field_name = True

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = Field(None, alias="quantity")
    category: Optional[str] = None
    is_active: Optional[bool] = None
    expiration_date: Optional[datetime] = None
    damaged_quantity: Optional[int] = None
    refill_threshold: Optional[int] = None

    class Config:
        allow_population_by_field_name = True
