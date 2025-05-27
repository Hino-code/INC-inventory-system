from fastapi import APIRouter, Depends, HTTPException, status, Body
from bson import ObjectId
from typing import List
from app.dependencies.auth import get_current_user
from app.database.connection import db
from app.models.product_model import Product, ProductCreate, UpdateProduct

router = APIRouter()

def product_serializer(product) -> dict:
    return {
        "id": str(product.get("_id")),
        "name": product.get("name"),
        "description": product.get("description", ""),
        "price": product.get("price"),
        "quantity": product.get("quantity"),
        "category": product.get("category", "General"),
        "is_active": product.get("is_active", True),
        "created_at": product.get("created_at"),
        "expiration_date": product.get("expiration_date"),
        "damaged_quantity": product.get("damaged_quantity", 0),
        "refill_threshold": product.get("refill_threshold", 10),
    }

@router.get("/products", response_model=List[Product])
async def get_products(user=Depends(get_current_user)):
    products_cursor = db.products.find()
    products = []
    async for product in products_cursor:
        products.append(product_serializer(product))
    return products

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str, user=Depends(get_current_user)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product_serializer(product)

@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners can create products")

    product_dict = product.dict(by_alias=True)
    result = await db.products.insert_one(product_dict)
    new_product = await db.products.find_one({"_id": result.inserted_id})
    return product_serializer(new_product)

@router.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: str,
    product_update: UpdateProduct = Body(...),
    user=Depends(get_current_user)
):
    if user.get("role") != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners can update products")

    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    update_data = {k: v for k, v in product_update.dict(exclude_unset=True, by_alias=True).items()}

    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields provided")

    result = await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
    return product_serializer(updated_product)

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, user=Depends(get_current_user)):
    if user.get("role") != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners can delete products")

    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    result = await db.products.delete_one({"_id": ObjectId(product_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return
