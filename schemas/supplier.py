
from pydantic import BaseModel, EmailStr
from typing import Optional

class SupplierCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    delivery_days: int = 0

class SupplierUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    delivery_days: Optional[int]
    is_active: Optional[bool]

class SupplierResponse(SupplierCreate):
    id: int
    is_active: bool
    rating: float
    rating_count: int
    class Config:
        orm_mode = True
