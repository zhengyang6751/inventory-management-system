from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app import crud, models
from app.api import deps
from app.schemas.sale import (
    Sale,
    SaleCreate,
    SaleUpdate,
    Return,
    ReturnCreate,
    ReturnUpdate,
)
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()

# Sales endpoints
@router.post("/sales", response_model=Sale)
def create_sale(
    *,
    db: Session = Depends(deps.get_db),
    sale_in: SaleCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> models.Sale:
    """
    Create new sale.
    """
    # Check if product exists and has enough stock
    product = crud.product.get(db, id=sale_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < sale_in.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    # Create sale
    sale = crud.sale.create_with_total(db, obj_in=sale_in, created_by=current_user.id)

    # Update product stock
    crud.product.update(
        db,
        db_obj=product,
        obj_in={"stock": product.stock - sale_in.quantity},
    )

    return sale

@router.get("/sales", response_model=List[Sale])
def read_sales(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    customer_id: Optional[int] = None,
    current_user: models.User = Depends(deps.get_current_user),
) -> List[models.Sale]:
    """
    Retrieve sales for the current user.
    """
    query = db.query(models.Sale).filter(models.Sale.created_by == current_user.id)
    
    if customer_id:
        query = query.filter(models.Sale.customer_id == customer_id)
    if start_date and end_date:
        query = query.filter(
            models.Sale.created_at >= datetime.combine(start_date, datetime.min.time()),
            models.Sale.created_at <= datetime.combine(end_date, datetime.max.time())
        )
    
    return query.options(joinedload(models.Sale.product), joinedload(models.Sale.customer)).offset(skip).limit(limit).all()

@router.get("/sales/summary")
def get_sales_summary(
    db: Session = Depends(deps.get_db),
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    """
    Get sales summary for date range.
    """
    return crud.sale.get_sales_summary(
        db,
        start_date=datetime.combine(start_date, datetime.min.time()),
        end_date=datetime.combine(end_date, datetime.max.time()),
    )

# Customer endpoints
@router.post("/customers/", response_model=Customer)
def create_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_in: CustomerCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> models.Customer:
    """
    Create new customer.
    """
    if customer_in.email:
        customer = crud.customer.get_by_email(db, email=customer_in.email)
        if customer:
            raise HTTPException(
                status_code=400,
                detail="A customer with this email already exists",
            )
    return crud.customer.create(db, obj_in=customer_in)

@router.get("/customers/", response_model=List[Customer])
def read_customers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> List[models.Customer]:
    """
    Retrieve customers.
    """
    return crud.customer.get_multi(db, skip=skip, limit=limit)

# Return endpoints
@router.post("/returns/", response_model=Return)
def create_return(
    *,
    db: Session = Depends(deps.get_db),
    return_in: ReturnCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> models.Return:
    """
    Create new return.
    """
    # Check if sale exists
    sale = crud.sale.get(db, id=return_in.sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    # Check if return quantity is valid
    if return_in.quantity > sale.quantity:
        raise HTTPException(
            status_code=400,
            detail="Return quantity cannot be greater than sale quantity",
        )

    # Create return
    return_ = crud.return_.create_with_user(
        db, obj_in=return_in, created_by=current_user.id
    )

    # Update product stock
    product = crud.product.get(db, id=return_in.product_id)
    crud.product.update(
        db,
        db_obj=product,
        obj_in={"stock": product.stock + return_in.quantity},
    )

    return return_

@router.get("/returns/", response_model=List[Return])
def read_returns(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    sale_id: Optional[int] = None,
    product_id: Optional[int] = None,
    current_user: models.User = Depends(deps.get_current_user),
) -> List[models.Return]:
    """
    Retrieve returns.
    """
    if sale_id:
        return crud.return_.get_by_sale(db, sale_id=sale_id)
    if product_id:
        return crud.return_.get_by_product(db, product_id=product_id)
    return crud.return_.get_multi(db, skip=skip, limit=limit) 