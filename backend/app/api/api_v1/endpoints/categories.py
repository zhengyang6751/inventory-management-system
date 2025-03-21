from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter()

@router.get("", response_model=List[Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[models.Category]:
    """
    Retrieve categories.
    """
    categories = crud.category.get_multi(db, skip=skip, limit=limit)
    return categories

@router.post("", response_model=Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate,
) -> models.Category:
    """
    Create new category.
    """
    category = crud.category.create(db=db, obj_in=category_in)
    return category

@router.put("/{id}", response_model=Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    category_in: CategoryUpdate,
) -> models.Category:
    """
    Update a category.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.update(db=db, db_obj=category, obj_in=category_in)
    return category

@router.get("/{id}", response_model=Category)
def read_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> models.Category:
    """
    Get category by ID.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{id}", response_model=Category)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> models.Category:
    """
    Delete a category.
    """
    category = crud.category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.remove(db=db, id=id)
    return category 