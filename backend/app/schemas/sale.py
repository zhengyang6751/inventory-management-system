from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .product import Product
from .customer import Customer

# Sale schemas
class SaleBase(BaseModel):
    product_id: int
    customer_id: Optional[int] = None
    quantity: float = Field(gt=0)
    unit_price: float = Field(gt=0)
    notes: Optional[str] = None

class SaleCreate(SaleBase):
    pass

class SaleUpdate(SaleBase):
    product_id: Optional[int] = None
    quantity: Optional[float] = Field(None, gt=0)
    unit_price: Optional[float] = Field(None, gt=0)

class Sale(SaleBase):
    id: int
    total_amount: float
    created_by: int
    created_at: datetime
    product: Product
    customer: Customer

    class Config:
        from_attributes = True

# Return schemas
class ReturnBase(BaseModel):
    sale_id: int
    product_id: int
    quantity: float = Field(gt=0)
    reason: Optional[str] = None
    notes: Optional[str] = None

class ReturnCreate(ReturnBase):
    pass

class ReturnUpdate(ReturnBase):
    sale_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[float] = Field(None, gt=0)

class Return(ReturnBase):
    id: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True 