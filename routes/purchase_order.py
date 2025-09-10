
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.purchase_order import PurchaseOrder, OrderStatus
from models.product import Product
from models.supplier import Supplier
from schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderResponse, PurchaseOrderUpdate
from datetime import datetime

router = APIRouter(prefix="/purchase-orders", tags=["PurchaseOrders"])

@router.post("/", response_model=PurchaseOrderResponse)
def create_order(payload: PurchaseOrderCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).get(payload.supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    # basic items validation: SKU existence optional, we allow creating order for new SKU names too
    items = [it.dict() for it in payload.items]
    order = PurchaseOrder(supplier_id=payload.supplier_id, items=items, status=OrderStatus.draft)
    db.add(order); db.commit(); db.refresh(order)
    return order

@router.get("/", response_model=list[PurchaseOrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return db.query(PurchaseOrder).all()

@router.put("/{order_id}", response_model=PurchaseOrderResponse)
def update_order(order_id: int, payload: PurchaseOrderUpdate, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrder).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    # update status; if changed to received, increase product inventory automatically and set received_at
    old_status = order.status
    if payload.status:
        order.status = payload.status
    if payload.received_at:
        order.received_at = payload.received_at
    if payload.delivery_time_days is not None:
        order.delivery_time_days = payload.delivery_time_days
    db.commit(); db.refresh(order)
    # handle received transition
    if old_status != order.status and order.status.name == "received":
        # increase inventory based on items
        for it in order.items:
            sku = it.get("sku")
            qty = int(it.get("quantity",0))
            if not sku:
                continue
            product = db.query(Product).filter(Product.sku == sku).first()
            if product:
                product.quantity = (product.quantity or 0) + qty
                db.add(product)
        order.received_at = order.received_at or datetime.utcnow()
        db.add(order)
        db.commit()
    # Update supplier rating if delivery_time provided
    if order.delivery_time_days is not None and order.supplier and order.delivery_time_days>0:
        supplier = order.supplier
        # simplistic scoring: lower delivery_time => better score (max 5)
        score = max(0, min(5, 5 - (order.delivery_time_days/7)))  # rough mapping
        supplier.rating_count = (supplier.rating_count or 0) + 1
        supplier.rating = ((supplier.rating or 0) * (supplier.rating_count-1) + score) / supplier.rating_count
        db.add(supplier); db.commit()
    db.refresh(order)
    return order
