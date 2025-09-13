from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
from datetime import datetime
from models.purchase_order import OrderStatus


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
    items: List[OrderItem]  
    status: OrderStatus
    created_at: datetime
    received_at: Optional[datetime]
    delivery_time_days: Optional[int]

    class Config:
        orm_mode = True
