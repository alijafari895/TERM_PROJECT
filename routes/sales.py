
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.sale import Sale
from models.product import Product
from schemas.sale import SaleCreate, SaleResponse, SaleItem
from auth import get_current_user
from typing import List

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/checkout", response_model=SaleResponse)
def checkout(payload: SaleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # validate stock
    total = 0.0
    for it in payload.items:
        product = db.query(Product).filter(Product.sku == it.sku).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {it.sku} not found")
        if product.quantity < it.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {it.sku}")
        total += float(it.price) * int(it.quantity)
    # reduce stock
    for it in payload.items:
        product = db.query(Product).filter(Product.sku == it.sku).first()
        product.quantity = product.quantity - it.quantity
        db.add(product)
    sale = Sale(customer_id=current_user.id, items=[it.dict() for it in payload.items], total=total)
    db.add(sale); db.commit(); db.refresh(sale)
    return sale

@router.get("/", response_model=list[SaleResponse])
def list_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()
