from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()

@router.get("", response_model=List[Customer])
def read_customers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[models.Customer]:
    """
    Retrieve customers.
    """
    customers = crud.customer.get_multi(db, skip=skip, limit=limit)
    return customers

@router.post("", response_model=Customer)
def create_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_in: CustomerCreate,
) -> models.Customer:
    """
    Create new customer.
    """
    customer = crud.customer.create(db=db, obj_in=customer_in)
    return customer

@router.put("/{id}", response_model=Customer)
def update_customer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    customer_in: CustomerUpdate,
) -> models.Customer:
    """
    Update a customer.
    """
    customer = crud.customer.get(db=db, id=id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer = crud.customer.update(db=db, db_obj=customer, obj_in=customer_in)
    return customer

@router.get("/{id}", response_model=Customer)
def read_customer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> models.Customer:
    """
    Get customer by ID.
    """
    customer = crud.customer.get(db=db, id=id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{id}", response_model=Customer)
def delete_customer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> models.Customer:
    """
    Delete a customer.
    """
    customer = crud.customer.get(db=db, id=id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer = crud.customer.remove(db=db, id=id)
    return customer 