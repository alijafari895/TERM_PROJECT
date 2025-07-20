from sqlalchemy import Column , Integer , String , Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Supplier(Base):
    __tablename__ = "suppliers"

    id =            Column( Integer , primary_key=True , index=True )
    name =          Column( String , nullable=False )
    email =         Column( String , unique=True , nullable=False ) 
    Phone =         Column( Integer , unique=True , nullable=False )
    delivery_days = Column( Integer )
    is_active =     Column( Boolean , default=True )

class order(Base):
    __tablename__ = "order"

    id = Column( Integer , primary_key=True , index=True )
    