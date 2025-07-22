from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.post('/Dashboard/Register_orders', tags=['Register_orders'])
def register_orders():
    return