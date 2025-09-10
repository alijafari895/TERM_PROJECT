
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models.product import Product
from schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
def add_product(payload: ProductCreate, db: Session = Depends(get_db)):
    if db.query(Product).filter(Product.sku == payload.sku).first():
        raise HTTPException(status_code=400, detail="SKU already exists")
    p = Product(**payload.dict())
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.get("/", response_model=List[ProductResponse])
def list_products(q: Optional[str] = Query(None), category: Optional[str] = None, min_price: Optional[float]=None, max_price: Optional[float]=None,
                  sort_by: Optional[str] = "name", sort_dir: Optional[str] = "asc", limit: int = 20, page: int = 1,
                  db: Session = Depends(get_db)):
    query = db.query(Product)
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%") | Product.sku.ilike(f"%{q}%"))
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    # sorting
    if sort_by not in ("name","price","quantity","sku"):
        sort_by = "name"
    col = getattr(Product, sort_by)
    if sort_dir == "desc":
        query = query.order_by(col.desc())
    else:
        query = query.order_by(col.asc())
    # pagination
    offset = (page-1)*limit
    results = query.offset(offset).limit(limit).all()
    return results

@router.get("/{sku}", response_model=ProductResponse)
def get_product(sku: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.sku == sku).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@router.put("/{sku}", response_model=ProductResponse)
def update_product(sku: str, payload: ProductUpdate, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.sku == sku).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    for k,v in payload.dict(exclude_unset=True).items():
        setattr(p, k, v)
    db.commit(); db.refresh(p)
    return p

@router.delete("/{sku}")
def delete_product(sku: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.sku == sku).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(p); db.commit()
    return {"message":"deleted"}
