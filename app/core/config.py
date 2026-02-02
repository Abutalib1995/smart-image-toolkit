from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    FRONTEND_URL: str = "http://localhost:5173"

    CORS_ORIGINS: str = "*"
    OUTPUT_DIR: str = "/tmp/outputs"
    MAX_UPLOAD_MB: int = 10

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
