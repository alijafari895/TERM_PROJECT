from fastapi import FastAPI
from databse import engine
from model import Base
from routes import router as supplier_router

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(supplier_router)
