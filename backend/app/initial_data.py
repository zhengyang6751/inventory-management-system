import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CATEGORIES = [
    {
        "name": "Electronics",
        "description": "Electronic devices and accessories"
    },
    {
        "name": "Clothing",
        "description": "Apparel and fashion items"
    },
    {
        "name": "Books",
        "description": "Books and publications"
    },
    {
        "name": "Home & Garden",
        "description": "Home improvement and garden supplies"
    }
]

SUPPLIERS = [
    {
        "name": "Tech Supplies Co.",
        "contact_name": "John Smith",
        "email": "john@techsupplies.com",
        "phone": "123-456-7890",
        "address": "123 Tech Street"
    },
    {
        "name": "Fashion Wholesale Ltd.",
        "contact_name": "Jane Doe",
        "email": "jane@fashionwholesale.com",
        "phone": "098-765-4321",
        "address": "456 Fashion Avenue"
    },
    {
        "name": "Book Distributors Inc.",
        "contact_name": "Bob Johnson",
        "email": "bob@bookdist.com",
        "phone": "555-123-4567",
        "address": "789 Book Lane"
    }
]

def init_db(db: Session) -> None:
    # Create categories
    for category_data in CATEGORIES:
        category = crud.category.get_by_name(db, name=category_data["name"])
        if not category:
            category_in = schemas.CategoryCreate(**category_data)
            crud.category.create(db, obj_in=category_in)
            logger.info(f"Created category: {category_data['name']}")

    # Create suppliers
    for supplier_data in SUPPLIERS:
        supplier = crud.supplier.get_by_name(db, name=supplier_data["name"])
        if not supplier:
            supplier_in = schemas.SupplierCreate(**supplier_data)
            crud.supplier.create(db, obj_in=supplier_in)
            logger.info(f"Created supplier: {supplier_data['name']}")

def main() -> None:
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    db.close()

if __name__ == "__main__":
    main() 