from fastapi import HTTPException
from app.database.connection import db
from app.models.product_model import Product
from app.models.product_model import UpdateProduct
from bson import ObjectId

# 🔹 Create a new product
async def create_product(product: Product):
    product_dict = product.dict()
    result = await db.products.insert_one(product_dict)
    new_product = await db.products.find_one({"_id": result.inserted_id})
    if new_product:
        new_product["_id"] = str(new_product["_id"])  # Convert ObjectId to string
        return new_product
    else:
        raise HTTPException(status_code=500, detail="Product creation failed")

# 🔹 Fetch all products
async def get_all_products():
    products = []
    async for product in db.products.find():
        product["_id"] = str(product["_id"])
        products.append(product)
    return products

# 🔹 Delete a product by ID
async def delete_product(product_id: str):
    try:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID")

        result = await db.products.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 1:
            return {"message": "Product deleted successfully"}

        raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 Update product by ID
async def update_product(product_id: str, update_data: UpdateProduct):
    try:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID")

        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}

        if not update_dict:
            raise HTTPException(status_code=400, detail="No update fields provided")

        result = await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_dict}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"message": "Product updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")