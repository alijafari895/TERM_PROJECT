from pydantic import BaseModel
from typing import List, Optional

class SaleItem(BaseModel):
    sku: str
    quantity: int
    price: float

class SaleCreate(BaseModel):
    items: List[SaleItem]

class SaleResponse(BaseModel):
    id: int
    customer_id: Optional[int]
    items: List[SaleItem] 
    total: float

    class Config:
        orm_mode = True
