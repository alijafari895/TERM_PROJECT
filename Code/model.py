from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SqlEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum

Base = declarative_base()

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    Phone = Column(String, unique=True, nullable=True)
    delivery_days = Column(Integer)
    is_active = Column(Boolean, default=True)

class OrderStatus(str, Enum):
    draft = "draft"
    sent = "sent"
    received = "received"
    closed = "closed"

class place_order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.draft)

    Supplier = relationship("Supplier")
