"""Clothing product catalog API starter."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(title="Clothing Product Service", version="1.0.0")

class Product(BaseModel):
    id: str
    name: str = Field(min_length=1, max_length=120)
    description: str = ""
    category: str
    price: float = Field(gt=0)
    currency: str = "INR"
    in_stock: bool = True

PRODUCTS: dict[str, Product] = {
    "tee-001": Product(id="tee-001", name="Classic Cotton T-Shirt", description="Everyday cotton tee", category="tops", price=499.0),
    "hood-001": Product(id="hood-001", name="Essential Hoodie", description="Mid-weight fleece hoodie", category="outerwear", price=1499.0),
}

@app.get("/health")
def health(): return {"status": "ok", "service": "product"}
@app.get("/products", response_model=list[Product])
def list_products(category: str | None = None):
    items = list(PRODUCTS.values())
    return [p for p in items if not category or p.category == category]
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    if product_id not in PRODUCTS: raise HTTPException(404, "Product not found")
    return PRODUCTS[product_id]
@app.post("/products", response_model=Product, status_code=201)
def create_product(product: Product):
    if product.id in PRODUCTS: raise HTTPException(409, "Product ID already exists")
    PRODUCTS[product.id] = product
    return product
