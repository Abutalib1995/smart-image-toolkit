from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.config import settings
from app.api.v1.routes_auth import router as auth_router
from app.api.v1.routes_tools import router as tools_router
from app.api.v1.routes_admin import router as admin_router

app = FastAPI(title="Smart Image Toolkit API (Auth)", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tools_router, prefix="/api/v1", tags=["tools"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])

out = Path(settings.OUTPUT_DIR)
out.mkdir(parents=True, exist_ok=True)
app.mount("/files", StaticFiles(directory=str(out)), name="files")

@app.get("/")
def root():
    return {"status":"ok","service":"Smart Image Toolkit API (Auth)"}
