from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class SupplierCreate(BaseModel):
    name: str
    email: EmailStr
    contact: Optional[str] = None
    delivery_days: int

class SupplierResponse(SupplierCreate):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    contact: Optional[str] = None
    delivery_days: Optional[int] = None

class orderStatus(str, Enum):
    draft = "draft"
    sent = "sent"
    received = "received"
    closed = "closed"

class order(BaseModel):
    id: int
    product_name: str
    quantity: int
    supplier_id: int
    order_status: orderStatus

class orderCreate(BaseModel):
    product_name: str
    quantity: int
    supplier_id: int
    order_status: orderStatus = orderStatus.draft

class orderResponse(order):
    class Config:
        orm_mode = True
