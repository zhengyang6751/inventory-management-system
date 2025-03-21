from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter()

@router.get("", response_model=List[Product])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[models.Product]:
    """
    Retrieve products.
    """
    products = crud.product.get_multi(db, skip=skip, limit=limit)
    return products

@router.post("", response_model=Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: ProductCreate,
) -> models.Product:
    """
    Create new product.
    """
    product = crud.product.create(db=db, obj_in=product_in)
    return product

@router.put("/{id}", response_model=Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    product_in: ProductUpdate,
) -> models.Product:
    """
    Update a product.
    """
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product

@router.get("/{id}", response_model=Product)
def read_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> models.Product:
    """
    Get product by ID.
    """
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{id}", response_model=Product)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> models.Product:
    """
    Delete a product.
    """
    product = crud.product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = crud.product.remove(db=db, id=id)
    return product

@router.get("/sku/{sku}", response_model=Product)
def read_product_by_sku(
    *,
    db: Session = Depends(deps.get_db),
    sku: str,
) -> models.Product:
    """
    Get product by SKU.
    """
    product = crud.product.get_by_sku(db=db, sku=sku)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/barcode/{barcode}", response_model=Product)
def read_product_by_barcode(
    *,
    db: Session = Depends(deps.get_db),
    barcode: str,
) -> models.Product:
    """
    Get product by barcode.
    """
    product = crud.product.get_by_barcode(db=db, barcode=barcode)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/category/{category_id}", response_model=List[Product])
def read_products_by_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
) -> List[models.Product]:
    """
    Get products by category.
    """
    products = crud.product.get_by_category(db=db, category_id=category_id)
    return products

@router.get("/supplier/{supplier_id}", response_model=List[Product])
def read_products_by_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_id: int,
) -> List[models.Product]:
    """
    Get products by supplier.
    """
    products = crud.product.get_by_supplier(db=db, supplier_id=supplier_id)
    return products

@router.get("/low-stock", response_model=List[Product])
def read_low_stock_products(
    db: Session = Depends(deps.get_db),
) -> List[models.Product]:
    """
    Get products with low stock (quantity <= min_quantity).
    """
    products = crud.product.get_low_stock(db=db)
    return products 