from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas.supplier import Supplier, SupplierCreate, SupplierUpdate

router = APIRouter()

@router.get("", response_model=List[Supplier])
def read_suppliers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[models.Supplier]:
    """
    Retrieve suppliers.
    """
    suppliers = crud.supplier.get_multi(db, skip=skip, limit=limit)
    return suppliers

@router.post("", response_model=Supplier)
def create_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_in: SupplierCreate,
) -> models.Supplier:
    """
    Create new supplier.
    """
    supplier = crud.supplier.create(db=db, obj_in=supplier_in)
    return supplier

@router.put("/{id}", response_model=Supplier)
def update_supplier(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    supplier_in: SupplierUpdate,
) -> models.Supplier:
    """
    Update a supplier.
    """
    supplier = crud.supplier.get(db=db, id=id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier = crud.supplier.update(db=db, db_obj=supplier, obj_in=supplier_in)
    return supplier

@router.get("/{id}", response_model=Supplier)
def read_supplier(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> models.Supplier:
    """
    Get supplier by ID.
    """
    supplier = crud.supplier.get(db=db, id=id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.delete("/{id}", response_model=Supplier)
def delete_supplier(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> models.Supplier:
    """
    Delete a supplier.
    """
    supplier = crud.supplier.get(db=db, id=id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier = crud.supplier.remove(db=db, id=id)
    return supplier 