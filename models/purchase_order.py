
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum
from datetime import datetime

class OrderStatus(PyEnum):
    draft = "Draft"
    sent = "Sent"
    received = "Received"
    closed = "Closed"

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    items = Column(JSON, nullable=False)  # list of {"sku":.., "quantity":.., "name":..}
    status = Column(Enum(OrderStatus), default=OrderStatus.draft)
    created_at = Column(DateTime, default=datetime.utcnow)
    received_at = Column(DateTime, nullable=True)
    delivery_time_days = Column(Integer, nullable=True)

    supplier = relationship("Supplier")
