from fastapi import FastAPI
from pydantic import BaseModel
import PM_get
import Rigester_sales_order
import sqlite3

class Product_info(BaseModel):
    id: int
    name: str
    sku: str
    price: float
    department: str
    inventory: int
    min_threshold: int

app = FastAPI()
app.include_router(PM_get.router, prefix='/Dashboard', tags=['Product_management'])
app.include_router(Rigester_sales_order.router, prefix='/Dashboard')

@app.post('/Dashboard/add_products', tags=['Product_management', 'add_product'])

def add_products(product : Product_info):
    with sqlite3.connect('Product_info.db') as cont:
        cur = cont.cursor()
        cur.execute('''INSERT INTO product VALUES (?, ?, ?, ?, ?, ?, ?);''',
                    (product.id, product.name, product.sku, product.price, product.department, product.inventory, product.min_threshold))
        cont.commit()
        
    return{"Result" : "Product added seccessfully !", "Product" : product.dict()}


@app.delete('/Dashboard/delete_products/{sku}', tags=['Product_management', 'delete_products'])

def delete_products(sku : str):
    with sqlite3.connect('Product_info.db') as cont:
        cur = cont.cursor()
        
        cur.execute('SELECT * FROM product WHERE sku = ?', (sku,))
        product = cur.fetchone()
        
        if product:
            cur.execute('DELETE FROM product WHERE sku = ?', (sku,))
            cont.commit()
            
            return {"Result" : "Product deleted seccessfully !", "SKU of product" : sku}
        else :
            
            return{"Result" : "Product not founded !"}
 
    
@app.put('/Dashboard/update_products/{sku}', tags=['Product_management', 'update_products'])

def update_products(sku: str, U_product: Product_info):
    with sqlite3.connect('Product_info.db') as cont:
        cur = cont.cursor()

        cur.execute('SELECT * FROM product WHERE sku = ?', (sku,))
        product = cur.fetchone()

        if product:
            cur.execute('''UPDATE product SET
                            id = ? 
                            name = ?, 
                            sku = ?, 
                            price = ?, 
                            department = ?, 
                            inventory = ?, 
                            min_threshold = ?
                        WHERE sku = ?''',
                        (U_product.id, U_product.name, U_product.sku, U_product.price, 
                        U_product.department, U_product.inventory,
                        U_product.min_threshold, U_product.sku)) 

            cont.commit()
        
        
            #if its invetory = min_threshold then
            if U_product.inventory == product[5]:   
                return{"Massage" : "You need to charge this prodct !",
                    "Result": "Product updated successfully!",
                    "Updated product": U_product.dict()}
            
            else :
                return {"Result": "Product updated successfully!", "Updated product": U_product.dict()}
        
        else:
            return {"Result": "Product not found!"}
