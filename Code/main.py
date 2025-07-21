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


#make engine
Base.metadata.create_all(bind=engine)

#make app
app = FastAPI()

#add post
@app.post("/suppliers/", response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    if db.query(Supplier).filter(Supplier.email == supplier.email).first():
        raise HTTPException(status_code=400, detail="Duplicate email.")
    new_supplier = Supplier(**supplier.dict())
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier
#add get supplier
@app.get("/suppliers/", response_model=list[SupplierResponse])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).filter(Supplier.is_active == True).all()

#add put supplier
@app.put("/suppliers/{supplier_id}")
def deactivate_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).get(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")
    supplier.is_active = False
    db.commit()
    return {"message": "Supplier deactivated."}

#change info add put
@app.put("/suppliers/{supplier_id}/edit", response_model=SupplierResponse)
def update_supplier_info(supplier_id: int, update: SupplierUpdate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).get(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Not Found")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(supplier, field, value)
    db.commit()
    db.refresh(supplier)
    return supplier

#add delete supplier
@app.delete("/suppliers/{suppliers_id}")
def delete_supplier(supplier_id: int , db:Session = Depends(get_db)):
    supplier = db.query(Supplier).get(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")
    db.delete(supplier)
    db.commit
    return {"message" : "Supplier Deleted"}


        










