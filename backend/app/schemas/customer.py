from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class CustomerBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    full_name: Optional[str] = None

class CustomerInDBBase(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Customer(CustomerInDBBase):
    pass

class CustomerInDB(CustomerInDBBase):
    pass 