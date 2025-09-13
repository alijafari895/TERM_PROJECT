from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Enum as SqlEnum

class OrderStatus(str, Enum):
    draft = "Draft"
    sent = "Sent"
    received = "Received"
    closed = "Closed"



class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.draft, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    received_at = Column(DateTime, nullable=True)
    delivery_time_days = Column(Integer, nullable=True)

    supplier = relationship("Supplier")
    items = relationship("PurchaseOrderItem", back_populates="order", cascade="all, delete-orphan")


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    sku = Column(String, nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("PurchaseOrder", back_populates="items")

    def __repr__(self):
        return f"<PurchaseOrderItem sku={self.sku} name={self.name} quantity={self.quantity}>"
