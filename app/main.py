from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import CORS_ORIGINS, OUTPUT_DIR
from app.api.v1.routes_compress import router as compress_router
from app.api.v1.routes_resize import router as resize_router
from app.api.v1.routes_convert import router as convert_router
from app.api.v1.routes_watermark import router as watermark_router
from app.api.v1.routes_exif import router as exif_router

app = FastAPI(title="Smart Image Toolkit API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compress_router, prefix="/api/v1", tags=["compress"])
app.include_router(resize_router, prefix="/api/v1", tags=["resize"])
app.include_router(convert_router, prefix="/api/v1", tags=["convert"])
app.include_router(watermark_router, prefix="/api/v1", tags=["watermark"])
app.include_router(exif_router, prefix="/api/v1", tags=["exif"])

app.mount("/files", StaticFiles(directory=str(OUTPUT_DIR)), name="files")

@app.get("/")
def root():
    return {"status": "ok", "service": "Smart Image Toolkit API"}
