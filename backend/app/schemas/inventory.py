from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.inventory import TransactionType

class InventoryTransactionBase(BaseModel):
    product_id: int
    quantity: int
    transaction_type: TransactionType
    reference: Optional[str] = None
    notes: Optional[str] = None

class InventoryTransactionCreate(InventoryTransactionBase):
    pass

class InventoryTransactionUpdate(InventoryTransactionBase):
    pass

class InventoryTransactionInDBBase(InventoryTransactionBase):
    id: int
    created_at: datetime
    created_by: Optional[int] = None

    class Config:
        from_attributes = True

class InventoryTransaction(InventoryTransactionInDBBase):
    pass

class InventoryTransactionInDB(InventoryTransactionInDBBase):
    pass 