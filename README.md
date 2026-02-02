# Smart Image Toolkit API (FastAPI)

Production-ready Python FastAPI backend providing:
- Compress image
- Resize image
- Convert image (JPG/PNG/WebP)
- Add watermark
- Extract EXIF metadata

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open docs: http://127.0.0.1:8000/docs

## Render deploy
Build Command:
```bash
pip install -r requirements.txt
```

Start Command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Env:
- OUTPUT_DIR=/tmp/outputs
- CORS_ORIGINS=*
- MAX_UPLOAD_MB=10

## API
Base `/api/v1`
- POST /compress?quality=75
- POST /resize?max_width=1200
- POST /convert?format=webp
- POST /watermark?text=YourBrand&opacity=0.35
- POST /exif
