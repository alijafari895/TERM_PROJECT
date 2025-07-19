# add Headers
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

# Made APP
app = FastAPI() 

#Writh the DB Function and Creat Table for add Supplier
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

#Writh the Function and Table for add Product req from Supplier
def init_addreq():
    conn = sqlite3.connect("suppliers.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Addreq (
            ID INTEGER PRIMARY KEY AUTOINCREMENT ,
            Productname TEXT NOT NULL ;
            Suppliername TEXT NOT NULL ;
            TIME TEXT NOT NULL ;
                   )

    """)

#Made accepteable value for supplier curl
class Supplier(BaseModel):
    Name: str
    Email: str
    Phone: str | None = None

#Made accepteable value for Addreq curl
class Addreq(BaseModel):
    Productname: str
    Suppliername: str
    TIME: str



