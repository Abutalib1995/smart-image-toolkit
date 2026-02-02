from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from app.utils.validators import validate_upload
from app.services.image_ops import extract_exif

router = APIRouter()

@router.post("/exif")
async def exif(file: UploadFile = File(...)):
    content = await file.read()
    validate_upload(file, len(content))

    return JSONResponse({"status":"success","exif":extract_exif(content)})
