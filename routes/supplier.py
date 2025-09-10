
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.supplier import Supplier
from schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/", response_model=SupplierResponse)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    if db.query(Supplier).filter(Supplier.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    s = Supplier(name=payload.name, email=payload.email, phone=payload.phone, delivery_days=payload.delivery_days)
    db.add(s); db.commit(); db.refresh(s)
    return s

@router.get("/", response_model=list[SupplierResponse])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).filter(Supplier.is_active == True).all()

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, payload: SupplierUpdate, db: Session = Depends(get_db)):
    s = db.query(Supplier).get(supplier_id)
    if not s:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for k,v in payload.dict(exclude_unset=True).items():
        setattr(s, k, v)
    db.commit(); db.refresh(s)
    return s

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    s = db.query(Supplier).get(supplier_id)
    if not s:
        raise HTTPException(status_code=404, detail="Supplier not found")
    s.is_active = False
    db.commit(); db.refresh(s)
    return {"message":"supplier deactivated"}
