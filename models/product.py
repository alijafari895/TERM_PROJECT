
from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    sku = Column(String, unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=True, index=True)  # Game, Console, Monitor, Headset etc.
    quantity = Column(Integer, default=0)
    min_threshold = Column(Integer, default=0)
    image_url = Column(Text, nullable=True)
