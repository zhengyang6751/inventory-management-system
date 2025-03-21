from typing import Optional
from pydantic import BaseModel, EmailStr

class SupplierBase(BaseModel):
    name: str
    contact_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    pass

class SupplierInDBBase(SupplierBase):
    id: int

    class Config:
        from_attributes = True

class Supplier(SupplierInDBBase):
    pass

class SupplierInDB(SupplierInDBBase):
    pass 