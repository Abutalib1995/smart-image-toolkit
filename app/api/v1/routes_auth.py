from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.core.security import hash_password, verify_password, create_token
from app.services.user_service import get_user_by_email, create_user, set_verified, set_password
from app.services.token_service import create_email_verification, get_email_token, create_password_reset, get_password_reset
from app.core.config import settings

router = APIRouter()

class SignupReq(BaseModel):
    email: EmailStr
    password: str

class LoginReq(BaseModel):
    email: EmailStr
    password: str

class TokenReq(BaseModel):
    token: str

class ForgotReq(BaseModel):
    email: EmailStr

class ResetReq(BaseModel):
    token: str
    new_password: str

@router.post("/signup")
def signup(body: SignupReq, db: Session = Depends(get_db)):
    if get_user_by_email(db, body.email):
        raise HTTPException(status_code=400, detail="User already exists")

    user = create_user(db, body.email, hash_password(body.password))

    verify_row = create_email_verification(db, user.id)
    verify_link = f"{settings.FRONTEND_URL}/verify-email?token={verify_row.token}"

    return {"status":"success","message":"Account created. Verify email.","verify_link":verify_link}

@router.post("/verify-email")
def verify_email(body: TokenReq, db: Session = Depends(get_db)):
    row = get_email_token(db, body.token)
    if not row or row.used:
        raise HTTPException(status_code=400, detail="Invalid token")
    if row.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    row.used = True
    db.commit()
    set_verified(db, row.user_id, True)
    return {"status":"success","message":"Email verified"}

@router.post("/login")
def login(body: LoginReq, db: Session = Depends(get_db)):
    user = get_user_by_email(db, body.email)
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    access = create_token(user.email, minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh = create_token(user.email, minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60)
    return {"status":"success","access_token":access,"refresh_token":refresh}

@router.post("/forgot-password")
def forgot(body: ForgotReq, db: Session = Depends(get_db)):
    user = get_user_by_email(db, body.email)
    if not user:
        return {"status":"success","message":"If account exists, reset email sent."}

    row = create_password_reset(db, user.id)
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={row.token}"
    return {"status":"success","message":"Reset link created","reset_link":reset_link}

@router.post("/reset-password")
def reset(body: ResetReq, db: Session = Depends(get_db)):
    row = get_password_reset(db, body.token)
    if not row or row.used:
        raise HTTPException(status_code=400, detail="Invalid token")
    if row.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    row.used = True
    db.commit()
    set_password(db, row.user_id, hash_password(body.new_password))
    return {"status":"success","message":"Password updated"}
