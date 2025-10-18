# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "development"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./dev.db"
    LOG_LEVEL: str = "info"
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:5173"
    SECRET_KEY: str = "changeme"

    class Config:
        env_file = ".env"

settings = Settings()
