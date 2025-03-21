import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.core.config import settings

logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    from app.db.base_class import Base
    from app.db.session import engine
    Base.metadata.create_all(bind=engine)
    
    user = crud.user.get_by_email(db, email="admin@example.com")
    if not user:
        user_in = schemas.UserCreate(
            email="admin@example.com",
            password="admin",
            is_superuser=True,
            full_name="Initial Admin"
        )
        user = crud.user.create(db, obj_in=user_in)
        logger.info("Created initial admin user") 