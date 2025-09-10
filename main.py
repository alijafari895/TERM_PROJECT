
from fastapi import FastAPI
from database import engine, Base
from routes import user, product, supplier, purchase_order, sales, report

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management API (Complete)")

# include routers
app.include_router(user.router)
app.include_router(product.router)
app.include_router(supplier.router)
app.include_router(purchase_order.router)
app.include_router(sales.router)
app.include_router(report.router)

@app.get("/")
def root():
    return {"message": "Inventory Management API is running - Complete Project"}
