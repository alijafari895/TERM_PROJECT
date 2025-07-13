from fastapi import APIRouter
import sqlite3
 
router = APIRouter()

@router.get('search_products/{name}', tags=['search_products'], summary='By name')

def search_products_by_Name (name : str):
    with sqlite3.connect('Product_info.db') as cont:
        cur = cont.cursor()
        
        cur.execute('SELECT * FROM product  WHERE  name=?',
                    (name,))
        product = cur.fetchone()
    
    return {"Result":"Product found !", "Product": product} if product else {"Result":"No product found !"}


@router.get('search_products/{sku}', tags=['search_products'], summary='By SKU')

def search_products_by_SKU (sku : str):
    with sqlite3.connect('Product_info.db') as cont:
        cur = cont.cursor()
        
        cur.execute('SELECT * FROM product  WHERE sku=?',
                    (sku,))
        product = cur.fetchone()
    
    return {"Result":"Product founded !", "Product": product} if product else {"Result":"No product found !"}


@router.get('search_products/{sku}/{name}', tags=['search_products'], summary='By both')

def search_products (sku : str, name : str):
    with sqlite3.connect('Product_info.db') as cont:
        cur = cont.cursor()
        
        cur.execute('SELECT * FROM product  WHERE sku=? AND name=?',
                    (sku,name,))
        product = cur.fetchone()
    
    return {"Result":"Product found !", "Product": product} if product else {"Result":"No product found !"}


@router.get('filter_products/{department}', tags=['filter_product'], summary='by department')

def filter_products_by_department (department : str):
    with sqlite3.connect('Product_info.db') as cont:
        cur = cont.cursor()
        
        cur.execute('SELECT * FROM product WHERE department=?',
                    (department,))
        product = cur.fetchall()
    
    return {"Result":"Product found !", "Product": product} if product else {"Result":"No product found !"}

@router.get('filter_products/{lower_price}/{upper_price}', tags=['filter_product'], summary='by price')

def filter_products_by_price (lower_price: float, upper_price: float):
    with sqlite3.connect('Product_info.db') as cont:
        cur = cont.cursor()
        cur.execute('SELECT * FROM product WHERE price BETWEEN ? AND ?', (lower_price, upper_price))
        product = cur.fetchall()
    
    return {"Result": "Products found!", "Product": product} if product else {"Result": "No products found!"}

@router.get('sort_product/price', tags=['sort_product'], summary='by price')

def sort_products_by_price ():
    
    with sqlite3.connect('Product_info.db') as cont:
        
        cur = cont.cursor()
        cur.execute('SELECT * FROM product ORDER BY price ASC')
        product = cur.fetchall()
        
    return {"Sorted product by price": product} if product else {"Result": "No product found !"}

@router.get('sort_product/name', tags=['sort_product'], summary='by name')

def sort_products_by_name ():
    
    with sqlite3.connect('Product_info.db') as cont:
        
        cur = cont.cursor()
        cur.execute('SELECT * FROM product ORDER BY name ASC')
        product = cur.fetchall()
        
    return {"Sorted product by name": product} if product else {"Result": "No product found !"}

@router.get('show_product/{page}/{limit}', tags=['show_product'])

def show_products (page: int, limit: int):
    
    start_point = limit * (page - 1) + 1
    end_point = limit * page
    
    with sqlite3.connect('Product_info.db') as cont:
        
        cur = cont.cursor()
        cur.execute('SELECT * FROM product WHERE id BETWEEN ? AND ?', (start_point, end_point))
        product = cur.fetchall()
        
    return {"Result": "Product found !", "Product": product} if product else {"Result": "No product found !"}