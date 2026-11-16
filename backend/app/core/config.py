"""
Centralised application settings loaded from environment / .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Praxion"
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://praxion:praxion@localhost:5432/praxion"
    SYNC_DATABASE_URL: str = "postgresql://praxion:praxion@localhost:5432/praxion"

    # LLM
    GEMINI_API_KEY: str = ""
    LLM_PROVIDER: str = "gemini"   # gemini | ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # Policy Engine
    OPA_URL: str = "http://localhost:8181"

    # Observability
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    OTEL_SERVICE_NAME: str = "praxion-backend"

    # Frontend
    FRONTEND_ORIGIN: str = "http://localhost:3000"

    # JWT
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()
