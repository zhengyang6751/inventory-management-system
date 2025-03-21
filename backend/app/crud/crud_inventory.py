from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.inventory import InventoryTransaction
from app.schemas.inventory import InventoryTransactionCreate

class CRUDInventory(CRUDBase[InventoryTransaction, InventoryTransactionCreate, InventoryTransactionCreate]):
    def create(self, db: Session, *, obj_in: InventoryTransactionCreate) -> InventoryTransaction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_product(self, db: Session, *, product_id: int) -> List[InventoryTransaction]:
        return db.query(self.model).filter(InventoryTransaction.product_id == product_id).all()

inventory = CRUDInventory(InventoryTransaction) 