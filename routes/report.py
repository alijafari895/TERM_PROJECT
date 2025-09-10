
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product
from models.purchase_order import PurchaseOrder, OrderStatus
from models.sale import Sale
from schemas.report import DashboardReport
from datetime import datetime
from auth import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/dashboard", response_model=DashboardReport)
def dashboard(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # require admin
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can access reports")
    total_products = db.query(Product).count()
    low_stock_products = db.query(Product).filter(Product.quantity < Product.min_threshold).count()
    total_purchase_orders = db.query(PurchaseOrder).count()
    total_sales = db.query(Sale).count()
    # orders by status
    orders_by_status = {s.value: db.query(PurchaseOrder).filter(PurchaseOrder.status==s).count() for s in OrderStatus}
    # top selling: count sum quantities by SKU from sales table (simple aggregation)
    top = {}
    all_sales = db.query(Sale).all()
    for s in all_sales:
        for it in s.items:
            sku = it.get("sku")
            q = int(it.get("quantity",0))
            top[sku] = top.get(sku,0) + q
    # sort top
    top_sorted = dict(sorted(top.items(), key=lambda x: x[1], reverse=True)[:10])
    return DashboardReport(
        total_products=total_products,
        low_stock_products=low_stock_products,
        total_purchase_orders=total_purchase_orders,
        total_sales=total_sales,
        top_selling=top_sorted,
        orders_by_status=orders_by_status,
        generated_at=datetime.utcnow()
    )
