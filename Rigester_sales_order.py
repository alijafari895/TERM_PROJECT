from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()

def check_inventory(number, inventory):
    return True if number <= inventory else False

@router.post('/Dashboard/Register_orders', tags=['Register_orders'])
def register_orders(name: str, number: int):    
    with sqlite3.connect('Product_info.db') as conn:
        cur = conn.cursor()
        cur.execute('Select Inventory FROM product WHERE name=?', (name,))
        inventory = cur.fetchone()
        
        if inventory:
            if check_inventory(number, inventory):
                
            else:
                raise HTTPException(status_code=409, 
                                    detail="""Sorry, we don't have enough stock for your order.
                                    Please try a smaller quantity or check back later!""")
        else:
            return{"Result" : "Product not founded !"}
    
    return