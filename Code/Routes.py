from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from databse import get_db
import model, schema

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

# Create Supplier
@router.post("/addsupplier", response_model=schema.SupplierResponse)
def create_supplier(supplier: schema.SupplierCreate, db: Session = Depends(get_db)):
    if db.query(model.Supplier).filter(model.Supplier.email == supplier.email).first():
        raise HTTPException(status_code=400, detail="Duplicate email.")
    new_supplier = model.Supplier(
        name=supplier.name,
        email=supplier.email,
        Phone=supplier.contact,
        delivery_days=supplier.delivery_days
    )
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

# Get Active Suppliers
@router.get("/showsupplier", response_model=list[schema.SupplierResponse])
def list_suppliers(db: Session = Depends(get_db)):
    return db.query(model.Supplier).filter(model.Supplier.is_active == True).all()

# Deactivate Supplier
@router.put("/deactivesupplier/{supplier_id}")
def deactivate_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(model.Supplier).get(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")
    supplier.is_active = False
    db.commit()
    return {"message": "Supplier deactivated."}

# Update Supplier Info
@router.put("/updatesupplier/{supplier_id}/edit", response_model=schema.SupplierResponse)
def update_supplier_info(supplier_id: int, update: schema.SupplierUpdate, db: Session = Depends(get_db)):
    supplier = db.query(model.Supplier).get(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")
    for field, value in update.dict(exclude_unset=True).items():
        if field == "contact":
            setattr(supplier, "Phone", value)
        else:
            setattr(supplier, field, value)
    db.commit()
    db.refresh(supplier)
    return supplier

# Delete Supplier
@router.delete("/deletesupplier/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(model.Supplier).get(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found.")
    db.delete(supplier)
    db.commit()
    return {"message": "Supplier deleted."}

# Create Order
@router.post("/addorders", response_model=schema.orderResponse)
def create_order(order: schema.orderCreate, db: Session = Depends(get_db)):
    db_order = model.place_order(
        product_name=order.product_name,
        quantity=order.quantity,
        supplier_id=order.supplier_id,
        status=order.order_status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# List Orders
@router.get("/showorders", response_model=list[schema.orderResponse])
def list_orders(db: Session = Depends(get_db)):
    return db.query(model.place_order).all()
