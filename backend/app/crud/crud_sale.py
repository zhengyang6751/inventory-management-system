from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.sale import Sale, Return
from app.models.customer import Customer
from app.schemas.sale import SaleCreate, SaleUpdate, ReturnCreate, ReturnUpdate
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CRUDSale(CRUDBase[Sale, SaleCreate, SaleUpdate]):
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Sale]:
        return (
            db.query(Sale)
            .options(joinedload(Sale.product), joinedload(Sale.customer))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_total(self, db: Session, *, obj_in: SaleCreate, created_by: int) -> Sale:
        obj_in_data = jsonable_encoder(obj_in)
        total_amount = obj_in.quantity * obj_in.unit_price
        db_obj = Sale(**obj_in_data, total_amount=total_amount, created_by=created_by)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        # Reload the object with relationships
        return db.query(Sale).options(joinedload(Sale.product), joinedload(Sale.customer)).filter(Sale.id == db_obj.id).first()

    def get_by_customer(self, db: Session, *, customer_id: int) -> List[Sale]:
        return (
            db.query(Sale)
            .options(joinedload(Sale.product), joinedload(Sale.customer))
            .filter(Sale.customer_id == customer_id)
            .all()
        )

    def get_by_date_range(
        self, db: Session, *, start_date: datetime, end_date: datetime
    ) -> List[Sale]:
        return (
            db.query(Sale)
            .options(joinedload(Sale.product), joinedload(Sale.customer))
            .filter(Sale.created_at >= start_date)
            .filter(Sale.created_at <= end_date)
            .all()
        )

    def get_daily_sales(self, db: Session, *, date: datetime) -> List[Sale]:
        next_day = date + timedelta(days=1)
        return (
            db.query(Sale)
            .options(joinedload(Sale.product), joinedload(Sale.customer))
            .filter(Sale.created_at >= date)
            .filter(Sale.created_at < next_day)
            .all()
        )

    def get_sales_summary(
        self, db: Session, *, start_date: datetime, end_date: datetime
    ) -> dict:
        result = (
            db.query(
                func.count(Sale.id).label("total_sales"),
                func.sum(Sale.total_amount).label("total_revenue"),
            )
            .filter(Sale.created_at >= start_date)
            .filter(Sale.created_at <= end_date)
            .first()
        )
        return {
            "total_sales": result.total_sales or 0,
            "total_revenue": float(result.total_revenue or 0),
        }

class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.email == email).first()

    def get_by_phone(self, db: Session, *, phone: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.phone == phone).first()

class CRUDReturn(CRUDBase[Return, ReturnCreate, ReturnUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: ReturnCreate, created_by: int
    ) -> Return:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Return(**obj_in_data, created_by=created_by)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_sale(self, db: Session, *, sale_id: int) -> List[Return]:
        return db.query(Return).filter(Return.sale_id == sale_id).all()

    def get_by_product(self, db: Session, *, product_id: int) -> List[Return]:
        return db.query(Return).filter(Return.product_id == product_id).all()

sale = CRUDSale(Sale)
customer = CRUDCustomer(Customer)
return_ = CRUDReturn(Return) 