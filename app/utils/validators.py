from fastapi import HTTPException, UploadFile
from app.core.config import ALLOWED_MIME, MAX_UPLOAD_MB

def validate_upload(file: UploadFile, size_bytes: int):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=415, detail="Only JPG/PNG/WebP allowed")
    if size_bytes > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"Max upload size is {MAX_UPLOAD_MB}MB")
