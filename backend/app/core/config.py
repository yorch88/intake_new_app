import os
from functools import lru_cache


class Settings:
    """Application settings loaded from environment variables."""

    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"

    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://mongo:27017")
    CORE_DB_NAME: str = os.getenv("CORE_DB_NAME", "core_db")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))

    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-in-prod")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    EMAIL_SMTP_HOST: str = os.getenv("EMAIL_SMTP_HOST", "smtp.example.com")
    EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    EMAIL_SMTP_USER: str = os.getenv("EMAIL_SMTP_USER", "user")
    EMAIL_SMTP_PASSWORD: str = os.getenv("EMAIL_SMTP_PASSWORD", "password")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@example.com")


@lru_cache
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()
