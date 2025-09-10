
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SaleItem(BaseModel):
    sku: str
    quantity: int
    price: float

class SaleCreate(BaseModel):
    items: List[SaleItem]

class SaleResponse(BaseModel):
    id: int
    customer_id: Optional[int]
    items: List[Dict[str, Any]]
    total: float
    class Config:
        orm_mode = True
