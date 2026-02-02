from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

def get_user_by_email(db: Session, email: str):
    return db.scalar(select(User).where(User.email == email))

def get_user_by_id(db: Session, user_id: str):
    return db.get(User, user_id)

def create_user(db: Session, email: str, password_hash: str):
    user = User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def set_verified(db: Session, user_id: str, verified: bool = True):
    user = get_user_by_id(db, user_id)
    user.is_verified = verified
    db.commit()
    return user

def set_password(db: Session, user_id: str, password_hash: str):
    user = get_user_by_id(db, user_id)
    user.password_hash = password_hash
    db.commit()
    return user
