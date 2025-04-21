from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SupplierBase(BaseModel):
    name: str
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Shared properties
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None
    barcode: Optional[str] = None
    price: float = Field(gt=0)
    cost: float = Field(gt=0)
    stock: int = Field(ge=0)
    min_quantity: int = Field(ge=0)

# Properties to receive on product creation
class ProductCreate(ProductBase):
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None

# Properties to receive on product update
class ProductUpdate(ProductBase):
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None

# Properties shared by models stored in DB
class ProductInDBBase(ProductBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None

    class Config:
        from_attributes = True

# Properties to return to client
class Product(ProductInDBBase):
    category: Optional[Category] = None
    supplier: Optional[Supplier] = None

    class Config:
        from_attributes = True

# Properties stored in DB
class ProductInDB(ProductInDBBase):
    pass

class InventoryTransactionBase(BaseModel):
    product_id: int
    quantity: int
    type: str
    reference: Optional[str] = None
    notes: Optional[str] = None

class InventoryTransactionCreate(InventoryTransactionBase):
    pass

class InventoryTransaction(InventoryTransactionBase):
    id: int
    created_at: datetime
    created_by: int
    product: Product

    class Config:
        from_attributes = True 