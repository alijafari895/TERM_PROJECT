#add library
from fastapi import FastAPI , HTTPException , Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel , EmailStr

from model import Supplier , Base
from databse import engine , SessionLocal

#make engine
Base.metadaa.creat_all(bind=engine)

#make app
app = FastAPI()

#make db func and sesion maker
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#make acceptable value for supplier
class SupplierCreat(BaseModel):
    name: str
    email: EmailStr
    contact: str | None = None
    delivery_days = int

#make acceptable value for active or not
class Supplierresponse(SupplierCreat):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


