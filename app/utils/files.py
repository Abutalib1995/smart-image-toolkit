import uuid
from pathlib import Path

def new_filename(ext: str) -> str:
    ext = ext.lower().lstrip(".")
    return f"{uuid.uuid4()}.{ext}"

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
