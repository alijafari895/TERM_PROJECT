from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
from datetime import datetime

class OrderStatus(str, Enum):
    draft = "Draft"
    sent = "Sent"
    received = "Received"
    closed = "Closed"

class OrderItem(BaseModel):
    sku: str
    name: str
    quantity: int

class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    items: List[OrderItem]

class PurchaseOrderUpdate(BaseModel):
    status: Optional[OrderStatus]
    received_at: Optional[datetime]
    delivery_time_days: Optional[int]

class PurchaseOrderResponse(BaseModel):
    id: int
    supplier_id: int
    items: List[OrderItem]  # تغییر داده شد تا با جدول PurchaseOrderItem مطابقت داشته باشد
    status: OrderStatus
    created_at: datetime
    received_at: Optional[datetime]
    delivery_time_days: Optional[int]

    class Config:
        orm_mode = True
