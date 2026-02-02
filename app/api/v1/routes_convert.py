from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
import aiofiles

from app.core.config import OUTPUT_DIR
from app.utils.validators import validate_upload
from app.utils.files import new_filename, ensure_dir
from app.services.image_ops import convert_image

router = APIRouter()

@router.post("/convert")
async def convert(request: Request, file: UploadFile = File(...), format: str = "webp", quality: int = 85):
    content = await file.read()
    validate_upload(file, len(content))

    out_bytes, ext = convert_image(content, fmt=format, quality=quality)

    ensure_dir(OUTPUT_DIR)
    filename = new_filename(ext)
    out_path = OUTPUT_DIR / filename

    async with aiofiles.open(out_path, "wb") as f:
        await f.write(out_bytes)

    base = str(request.base_url).rstrip("/")
    return JSONResponse({"status":"success","format":ext,"output_url":f"{base}/files/{filename}"})
