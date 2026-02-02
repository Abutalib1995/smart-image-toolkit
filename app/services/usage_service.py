from sqlalchemy.orm import Session
from app.models.usage_log import ToolUsageLog

def log_usage(db: Session, user_id: str, tool_name: str, ip: str = ""):
    row = ToolUsageLog(user_id=user_id, tool_name=tool_name, ip=ip)
    db.add(row)
    db.commit()
    return row
