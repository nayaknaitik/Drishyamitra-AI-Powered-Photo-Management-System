from __future__ import annotations

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    flask_env: str = Field(default="development", alias="FLASK_ENV")
    flask_debug: bool = Field(default=True, alias="FLASK_DEBUG")
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")

    jwt_secret_key: str = Field(default="change-me-too", alias="JWT_SECRET_KEY")
    jwt_access_token_expires_minutes: int = Field(default=60, alias="JWT_ACCESS_TOKEN_EXPIRES_MINUTES")

    database_url: str = Field(
        default="postgresql+psycopg2://drishyamitra:drishyamitra@localhost:5432/drishyamitra",
        alias="DATABASE_URL",
    )
    sqlite_fallback_path: str = Field(default="./drishyamitra.db", alias="SQLITE_FALLBACK_PATH")

    redis_url: str | None = Field(default=None, alias="REDIS_URL")
    celery_broker_url: str | None = Field(default=None, alias="CELERY_BROKER_URL")
    celery_result_backend: str | None = Field(default=None, alias="CELERY_RESULT_BACKEND")

    upload_root: str = Field(default="./uploads", alias="UPLOAD_ROOT")
    max_content_length_mb: int = Field(default=25, alias="MAX_CONTENT_LENGTH_MB")

    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.1-70b-versatile", alias="GROQ_MODEL")

    public_base_url: AnyUrl | None = Field(default=None, alias="PUBLIC_BASE_URL")

    smtp_host: str | None = Field(default=None, alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_username: str | None = Field(default=None, alias="SMTP_USERNAME")
    smtp_password: str | None = Field(default=None, alias="SMTP_PASSWORD")
    smtp_from: str | None = Field(default=None, alias="SMTP_FROM")

    twilio_account_sid: str | None = Field(default=None, alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str | None = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    twilio_whatsapp_from: str | None = Field(default=None, alias="TWILIO_WHATSAPP_FROM")


settings = Settings()


