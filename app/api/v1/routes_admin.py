from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.core.deps import require_admin
from app.models.user import User
from app.models.usage_log import ToolUsageLog

router = APIRouter()

@router.get("/users")
def users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    rows = db.scalars(select(User).order_by(User.created_at.desc())).all()
    return {"status":"success","users":[
        {"id":u.id,"email":u.email,"role":u.role,"is_verified":u.is_verified,"is_active":u.is_active,"created_at":str(u.created_at)}
        for u in rows
    ]}

@router.get("/logs")
def logs(db: Session = Depends(get_db), admin=Depends(require_admin)):
    rows = db.scalars(select(ToolUsageLog).order_by(ToolUsageLog.created_at.desc()).limit(200)).all()
    return {"status":"success","logs":[
        {"id":l.id,"user_id":l.user_id,"tool_name":l.tool_name,"ip":l.ip,"created_at":str(l.created_at)}
        for l in rows
    ]}
