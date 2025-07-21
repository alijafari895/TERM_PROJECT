from model import Supplier , Base
from pydantic import BaseModel , EmailStr
from typing import Optional
from pydantic import Field

#make acceptable value for supplier
class SupplierCreate(BaseModel):
    name: str
    email: EmailStr
    contact: str | None = None
    delivery_days : int

#make acceptable value for active or not
class SupplierResponse(SupplierCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

#for changing info
class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    contact: Optional[str] = Field(None)
    delivery_time_days: Optional[int] = Field(None)