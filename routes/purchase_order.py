from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.purchase_order import PurchaseOrder, PurchaseOrderItem, OrderStatus
from models.product import Product
from models.supplier import Supplier
from schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderResponse, PurchaseOrderUpdate
from datetime import datetime

router = APIRouter(prefix="/purchase-orders", tags=["PurchaseOrders"])

# Create order
@router.post("/", response_model=PurchaseOrderResponse)
def create_order(payload: PurchaseOrderCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).get(payload.supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    order = PurchaseOrder(supplier_id=payload.supplier_id, status=OrderStatus.draft)
    db.add(order)
    db.commit()
    db.refresh(order)

    # Insert items into PurchaseOrderItem table
    for it in payload.items:
        item = PurchaseOrderItem(
            order_id=order.id,
            sku=it.sku,
            name=it.name,
            quantity=it.quantity
        )
        db.add(item)
    db.commit()
    db.refresh(order)
    return order

# List orders
@router.get("/", response_model=list[PurchaseOrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return db.query(PurchaseOrder).all()

# Update order
@router.put("/{order_id}", response_model=PurchaseOrderResponse)
def update_order(order_id: int, payload: PurchaseOrderUpdate, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrder).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    old_status = order.status
    if payload.status:
        order.status = payload.status
    if payload.delivery_time_days is not None:
        order.delivery_time_days = payload.delivery_time_days
    if payload.received_at:
        order.received_at = payload.received_at

    db.commit()
    db.refresh(order)

    # handle received transition
    if old_status != order.status and order.status == OrderStatus.received:
        # increase inventory based on items
        for it in order.items:
            product = db.query(Product).filter(Product.sku == it.sku).first()
            if product:
                product.quantity = (product.quantity or 0) + it.quantity
                db.add(product)
        order.received_at = order.received_at or datetime.utcnow()
        db.add(order)
        db.commit()

    # Update supplier rating if delivery_time provided
    if order.delivery_time_days is not None and order.supplier and order.delivery_time_days > 0:
        supplier = order.supplier
        score = max(0, min(5, 5 - (order.delivery_time_days / 7)))
        supplier.rating_count = (supplier.rating_count or 0) + 1
        supplier.rating = ((supplier.rating or 0) * (supplier.rating_count - 1) + score) / supplier.rating_count
        db.add(supplier)
        db.commit()

    db.refresh(order)
    return order
