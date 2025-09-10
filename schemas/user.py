
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str
    role: Optional[str] = "customer"

    @validator("password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        has_digit = any(ch.isdigit() for ch in v)
        has_alpha = any(ch.isalpha() for ch in v)
        if not (has_digit and has_alpha):
            raise ValueError("Password must include letters and numbers")
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    role: str

    class Config:
        orm_mode = True
