from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate

class CRUDSupplier(CRUDBase[Supplier, SupplierCreate, SupplierUpdate]):
    def create(self, db: Session, *, obj_in: SupplierCreate) -> Supplier:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name(self, db: Session, *, name: str) -> Optional[Supplier]:
        return db.query(self.model).filter(Supplier.name == name).first()

supplier = CRUDSupplier(Supplier) 