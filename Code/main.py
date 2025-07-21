#add library
from fastapi import FastAPI , HTTPException , Depends
from sqlalchemy.orm import Session
from databse import engine , SessionLocal
from databse import get_db  
from Routes import Supplier
from model import Supplier , Base

#make engine
Base.metadata.create_all(bind=engine)

#make app
app = FastAPI()
app.include_router(Supplier.router)


        










