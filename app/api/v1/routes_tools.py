from fastapi import APIRouter, UploadFile, File, Request, Depends
from fastapi.responses import JSONResponse
import aiofiles
from pathlib import Path
import uuid
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_user
from app.core.config import settings
from app.utils.validators import validate_upload
from app.services.image_ops import compress_jpeg, resize_image, convert_image, add_text_watermark, extract_exif
from app.services.usage_service import log_usage

router = APIRouter()

def _out_dir() -> Path:
    p = Path(settings.OUTPUT_DIR)
    p.mkdir(parents=True, exist_ok=True)
    return p

async def _save(out_bytes: bytes, ext: str) -> str:
    filename = f"{uuid.uuid4()}.{ext}"
    out_path = _out_dir() / filename
    async with aiofiles.open(out_path, "wb") as f:
        await f.write(out_bytes)
    return filename

@router.post("/compress")
async def compress(request: Request, file: UploadFile = File(...), quality: int = 75,
                   user=Depends(get_current_user), db: Session = Depends(get_db)):
    content = await file.read()
    validate_upload(file, len(content))
    out_bytes = compress_jpeg(content, quality=quality)
    filename = await _save(out_bytes, "jpg")
    log_usage(db, user.id, "compress", request.client.host if request.client else "")
    base = str(request.base_url).rstrip("/")
    return JSONResponse({"status":"success","output_url":f"{base}/files/{filename}"})

@router.post("/resize")
async def resize(request: Request, file: UploadFile = File(...), max_width: int = 1200,
                 user=Depends(get_current_user), db: Session = Depends(get_db)):
    content = await file.read()
    validate_upload(file, len(content))
    out_bytes = resize_image(content, max_width=max_width)
    filename = await _save(out_bytes, "png")
    log_usage(db, user.id, "resize", request.client.host if request.client else "")
    base = str(request.base_url).rstrip("/")
    return JSONResponse({"status":"success","output_url":f"{base}/files/{filename}"})

@router.post("/convert")
async def convert(request: Request, file: UploadFile = File(...), format: str = "webp", quality: int = 85,
                  user=Depends(get_current_user), db: Session = Depends(get_db)):
    content = await file.read()
    validate_upload(file, len(content))
    out_bytes, ext = convert_image(content, fmt=format, quality=quality)
    filename = await _save(out_bytes, ext)
    log_usage(db, user.id, "convert", request.client.host if request.client else "")
    base = str(request.base_url).rstrip("/")
    return JSONResponse({"status":"success","output_url":f"{base}/files/{filename}","format":ext})

@router.post("/watermark")
async def watermark(request: Request, file: UploadFile = File(...), text: str="YourBrand", opacity: float=0.35,
                    user=Depends(get_current_user), db: Session = Depends(get_db)):
    content = await file.read()
    validate_upload(file, len(content))
    out_bytes = add_text_watermark(content, text=text, opacity=opacity)
    filename = await _save(out_bytes, "png")
    log_usage(db, user.id, "watermark", request.client.host if request.client else "")
    base = str(request.base_url).rstrip("/")
    return JSONResponse({"status":"success","output_url":f"{base}/files/{filename}"})

@router.post("/exif")
async def exif(request: Request, file: UploadFile = File(...),
               user=Depends(get_current_user), db: Session = Depends(get_db)):
    content = await file.read()
    validate_upload(file, len(content))
    data = extract_exif(content)
    log_usage(db, user.id, "exif", request.client.host if request.client else "")
    return JSONResponse({"status":"success","exif":data})
