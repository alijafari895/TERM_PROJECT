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
class SupplierCreate(BaseModel):
    name: str
    email: EmailStr
    contact: str | None = None
    delivery_days = int

#make acceptable value for active or not
class SupplierResponse(SupplierCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# add post
@app.post("/suppliers/", response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    if db.query(Supplier).filter(Supplier.email == supplier.email).first():
    raise HTTPException(status_code=400, detail="Duplicate email.")
    new_supplier = Supplier(**supplier.dict())
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

@app.get("/suppliers/", response_model=list[SupplierResponse])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).filter(Supplier.is_active == True).all()

@app.put("/suppliers/{supplier_id}")
def deactivate_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).get(supplier_id)
if not supplier:
    raise HTTPException(status_code=404, detail="Supplier not found.")








