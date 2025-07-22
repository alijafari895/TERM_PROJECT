from fastapi import APIRouter
import sqlite3

router = APIRouter()

def check_inventory(number, inventory):
    return True if number <= inventory else False

@router.post('/Dashboard/Register_orders', tags=['Register_orders'])
def register_orders(name: str, number: int):
    return