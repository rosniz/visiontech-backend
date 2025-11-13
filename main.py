from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime

app = FastAPI(
    title="VisionTech API",
    description="API Backend pour VisionTech",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez vos domaines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles de données
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    category: str
    stock: int
    created_at: Optional[datetime] = None

class ContactMessage(BaseModel):
    name: str
    email: str
    subject: str
    message: str

# Base de données simulée (remplacer par PostgreSQL/MongoDB en production)
products_db = [
    {
        "id": 1,
        "name": "Ordinateur Portable HP",
        "description": "Core i5, 8GB RAM, 256GB SSD",
        "price": 450000,
        "category": "laptops",
        "stock": 15,
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "name": "iPhone 13",
        "description": "128GB, Noir",
        "price": 550000,
        "category": "phones",
        "stock": 10,
        "created_at": datetime.now()
    }
]

messages_db = []

# Routes
@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API VisionTech",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now()
    }

# Products endpoints
@app.get("/api/products", response_model=List[Product])
async def get_products(category: Optional[str] = None):
    if category:
        return [p for p in products_db if p["category"] == category]
    return products_db

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

@app.post("/api/products", response_model=Product)
async def create_product(product: Product):
    product.id = len(products_db) + 1
    product.created_at = datetime.now()
    product_dict = product.dict()
    products_db.append(product_dict)
    return product_dict

@app.put("/api/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product):
    idx = next((i for i, p in enumerate(products_db) if p["id"] == product_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    product.id = product_id
    products_db[idx] = product.dict()
    return products_db[idx]

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int):
    idx = next((i for i, p in enumerate(products_db) if p["id"] == product_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    products_db.pop(idx)
    return {"message": "Produit supprimé avec succès"}

# Contact endpoint
@app.post("/api/contact")
async def send_contact_message(message: ContactMessage):
    message_dict = message.dict()
    message_dict["created_at"] = datetime.now()
    messages_db.append(message_dict)
    return {
        "message": "Message envoyé avec succès",
        "status": "success"
    }

# Categories endpoint
@app.get("/api/categories")
async def get_categories():
    categories = list(set(p["category"] for p in products_db))
    return {"categories": categories}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)