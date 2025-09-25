from sqlalchemy.orm import Session
from src.core.models.user import User
from src.utils.security import hash_password

def create_user(db: Session, username: str, email: str, password: str, role: str = "user") -> User:
    hashed_password = hash_password(password)
    db_user = User(username=username, email=email, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()