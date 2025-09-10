
from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    delivery_days = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)  # computed average based on deliveries
    rating_count = Column(Integer, default=0)
