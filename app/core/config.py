import os
from pathlib import Path

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/tmp/outputs"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}

CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
