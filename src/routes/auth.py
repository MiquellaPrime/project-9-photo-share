from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserOut, Token
from src.repository.user import create_user, get_user_by_username
from src.utils.security import verify_password, create_access_token 
from src.core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    role = "admin" if db.query(User).count() == 0 else "user"
    return create_user(db, user.username, user.email, user.password, role)

@router.post("/login", response_model=Token)
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}