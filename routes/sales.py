from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from database import get_db
from models.sale import Sale, SaleItem
from models.product import Product
from schemas.sale import SaleCreate, SaleResponse, SaleItem as SaleItemSchema
from auth import get_current_user
from typing import List

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/checkout", response_model=SaleResponse)
def checkout(payload: SaleCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    total = 0.0

    for it in payload.items:
        product = db.query(Product).filter(Product.sku == it.sku).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {it.sku} not found")
        if product.quantity < it.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {it.sku}")
        total += float(it.price) * int(it.quantity)
    

    for it in payload.items:
        product = db.query(Product).filter(Product.sku == it.sku).first()
        product.quantity -= it.quantity
        db.add(product)


    sale = Sale(customer_id=current_user.id, total=total)
    db.add(sale)
    db.commit()
    db.refresh(sale)


    for it in payload.items:
        item = SaleItem(
            sale_id=sale.id,
            sku=it.sku,
            quantity=it.quantity,
            price=it.price
        )
        db.add(item)
    db.commit()
    db.refresh(sale)
    
    return sale


@router.get("/", response_model=List[SaleResponse])
def list_sales(db: Session = Depends(get_db)):

    sales = db.query(Sale).options(selectinload(Sale.items)).all()
    return sales
