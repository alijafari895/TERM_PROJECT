# add Headers
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

# Made APP
app = FastAPI() 

#Writh the DB Function and Creat Table for add Suplier
def init_db():
    conn = sqlite3.connect("suppliers.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Suppliers (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT NOT NULL,
            Phone TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

#Made accepteable value for curl
class Supplier(BaseModel):
    name: str
    email: str
    phone: str | None = None


# Add curl
@app.post("/suppliers/") 
def create_supplier(supplier: Supplier):
    conn = sqlite3.connect("suppliers.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Suppliers (name, email, phone) VALUES (?, ?, ?)",
                   (supplier.name, supplier.email, supplier.phone))
    conn.commit()
    supplier_id = cursor.lastrowid
    conn.close()
    return {"id": supplier_id, **supplier.dict()}

