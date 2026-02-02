import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.token_models import EmailVerificationToken, PasswordResetToken

def create_email_verification(db: Session, user_id: str, minutes: int = 60):
    token = secrets.token_urlsafe(32)
    row = EmailVerificationToken(
        user_id=user_id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=minutes),
        used=False,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def get_email_token(db: Session, token: str):
    return db.scalar(select(EmailVerificationToken).where(EmailVerificationToken.token == token))

def create_password_reset(db: Session, user_id: str, minutes: int = 30):
    token = secrets.token_urlsafe(32)
    row = PasswordResetToken(
        user_id=user_id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=minutes),
        used=False,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def get_password_reset(db: Session, token: str):
    return db.scalar(select(PasswordResetToken).where(PasswordResetToken.token == token))
