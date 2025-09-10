
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    sku: str
    price: float
    category: Optional[str] = None
    quantity: int = 0
    min_threshold: int = 0
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    category: Optional[str]
    quantity: Optional[int]
    min_threshold: Optional[int]
    image_url: Optional[str]

class ProductResponse(ProductBase):
    id: int
    class Config:
        orm_mode = True
