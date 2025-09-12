from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, Token, UserResponse
from auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup", response_model=UserResponse)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == payload.username) | (User.email == payload.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    hashed_password = get_password_hash(payload.password)
    user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hashed_password,
        role=payload.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token({
        "sub": user.username,
        "role": user.role,
        "user_id": user.id
    })
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
