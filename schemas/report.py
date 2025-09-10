
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class DashboardReport(BaseModel):
    total_products: int
    low_stock_products: int
    total_purchase_orders: int
    total_sales: int
    top_selling: Dict[str, int]
    orders_by_status: Dict[str, int]
    generated_at: datetime
