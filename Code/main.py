from fastapi import FASTAPI , HTTPExeption , Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel , EmailStr

from model import Supplier , Base
from database import engine , SessionLocal

Base.metadaa.creat_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()