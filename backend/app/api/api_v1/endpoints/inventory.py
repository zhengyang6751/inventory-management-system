from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app import crud, models
from app.api import deps
from app.schemas.inventory import InventoryTransaction, InventoryTransactionCreate

router = APIRouter()

@router.get("/", response_model=List[InventoryTransaction])
def read_inventory_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> List[models.InventoryTransaction]:
    """
    Get inventory transactions for the current user.
    """
    return (
        db.query(models.InventoryTransaction)
        .filter(models.InventoryTransaction.created_by == current_user.id)
        .options(joinedload(models.InventoryTransaction.product))
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.post("/", response_model=InventoryTransaction)
def create_inventory_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: InventoryTransactionCreate,
) -> models.InventoryTransaction:
    """
    Create new inventory transaction.
    """
    # Get the product
    product = crud.product.get(db=db, id=transaction_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update product quantity based on transaction type
    if transaction_in.transaction_type == "IN":
        product.quantity += transaction_in.quantity
    elif transaction_in.transaction_type == "OUT":
        if product.quantity < transaction_in.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        product.quantity -= transaction_in.quantity
    elif transaction_in.transaction_type == "ADJUSTMENT":
        product.quantity = transaction_in.quantity

    # Create transaction
    transaction = crud.inventory.create(db=db, obj_in=transaction_in)
    
    # Commit changes
    db.commit()
    db.refresh(product)
    
    return transaction

@router.get("/product/{product_id}", response_model=List[InventoryTransaction])
def read_product_transactions(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> List[models.InventoryTransaction]:
    """
    Get inventory transactions for a specific product and current user.
    """
    return (
        db.query(models.InventoryTransaction)
        .filter(
            models.InventoryTransaction.product_id == product_id,
            models.InventoryTransaction.created_by == current_user.id
        )
        .options(joinedload(models.InventoryTransaction.product))
        .all()
    ) 