from typing import List, Optional, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(self.model)
            .options(joinedload(Product.category), joinedload(Product.supplier))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get(self, db: Session, id: Any) -> Optional[Product]:
        return (
            db.query(self.model)
            .options(joinedload(Product.category), joinedload(Product.supplier))
            .filter(self.model.id == id)
            .first()
        )

    def create(self, db: Session, *, obj_in: ProductCreate) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_sku(self, db: Session, *, sku: str) -> Optional[Product]:
        return (
            db.query(self.model)
            .options(joinedload(Product.category), joinedload(Product.supplier))
            .filter(Product.sku == sku)
            .first()
        )

    def get_by_barcode(self, db: Session, *, barcode: str) -> Optional[Product]:
        return (
            db.query(self.model)
            .options(joinedload(Product.category), joinedload(Product.supplier))
            .filter(Product.barcode == barcode)
            .first()
        )

    def get_by_category(self, db: Session, *, category_id: int) -> List[Product]:
        return (
            db.query(self.model)
            .options(joinedload(Product.category), joinedload(Product.supplier))
            .filter(Product.category_id == category_id)
            .all()
        )

    def get_by_supplier(self, db: Session, *, supplier_id: int) -> List[Product]:
        return (
            db.query(self.model)
            .options(joinedload(Product.category), joinedload(Product.supplier))
            .filter(Product.supplier_id == supplier_id)
            .all()
        )

    def get_low_stock(self, db: Session) -> List[Product]:
        return (
            db.query(self.model)
            .options(joinedload(Product.category), joinedload(Product.supplier))
            .filter(Product.stock <= Product.min_quantity)
            .all()
        )

product = CRUDProduct(Product) 