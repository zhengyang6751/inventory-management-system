from typing import Optional

from pydantic import BaseModel

# Shared properties
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

# Properties to receive on category creation
class CategoryCreate(CategoryBase):
    pass

# Properties to receive on category update
class CategoryUpdate(CategoryBase):
    pass

# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Properties to return to client
class Category(CategoryInDBBase):
    pass

# Properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass 