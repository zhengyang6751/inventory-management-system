from fastapi import APIRouter
from app.api.api_v1.endpoints import login, users, products, categories, suppliers, inventory, sales, customers

api_router = APIRouter()

# Login routes
api_router.include_router(login.router, prefix="/login", tags=["login"])

# User routes
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Product routes
api_router.include_router(products.router, prefix="/products", tags=["products"])

# Category routes
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])

# Supplier routes
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])

# Inventory routes
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])

# Sales routes
api_router.include_router(sales.router, tags=["sales"])

# Customer routes
api_router.include_router(customers.router, prefix="/customers", tags=["customers"]) 