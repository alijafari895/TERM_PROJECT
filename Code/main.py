from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI() 

def init_db():
    conn = sqlite3.connect("suppliers.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


class Supplier(BaseModel):
    name: str
    email: str
    phone: str | None = None

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

