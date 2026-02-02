# Smart Image Toolkit API - Auth Edition (PostgreSQL + Admin)

Upgraded backend with:
- PostgreSQL (SQLAlchemy + Alembic)
- Signup/Login (JWT access + refresh)
- Email verification token
- Forgot password token
- Role based admin endpoints
- Image tools protected with JWT
- Usage logs

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# create .env from .env.example and set DATABASE_URL
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

## Render
- Create PostgreSQL
- Set env vars
- Build: pip install -r requirements.txt
- Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
