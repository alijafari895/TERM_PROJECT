
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    items = Column(JSON, nullable=False)  # [{"sku":..., "quantity":..., "price":...}, ...]
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User")
