#add library
from fastapi import FastAPI , HTTPException , Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel , EmailStr
from pydantic import Field
from model import Supplier , Base
from databse import engine , SessionLocal
from typing import Optional
from schema import SupplierCreate , SupplierResponse , SupplierUpdate
from databse import get_db  
from Routes import Supplier

#make engine
Base.metadata.create_all(bind=engine)

#make app
app = FastAPI()
app.include_router(Supplier.router)


        










