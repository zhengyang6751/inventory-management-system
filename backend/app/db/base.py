# Import all the models, so that Base has them before being imported by Alembic
from app.db.base_class import Base
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.inventory import InventoryTransaction
from app.models.customer import Customer
from app.models.sale import Sale, Return 