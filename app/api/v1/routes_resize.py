from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
import aiofiles

from app.core.config import OUTPUT_DIR
from app.utils.validators import validate_upload
from app.utils.files import new_filename, ensure_dir
from app.services.image_ops import resize_image

router = APIRouter()

@router.post("/resize")
async def resize(request: Request, file: UploadFile = File(...), max_width: int = 1200):
    content = await file.read()
    validate_upload(file, len(content))

    out_bytes = resize_image(content, max_width=max_width)

    ensure_dir(OUTPUT_DIR)
    filename = new_filename("png")
    out_path = OUTPUT_DIR / filename

    async with aiofiles.open(out_path, "wb") as f:
        await f.write(out_bytes)

    base = str(request.base_url).rstrip("/")
    return JSONResponse({"status":"success","output_url":f"{base}/files/{filename}"})
