from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    vision_provider: str = "mock"
    openai_api_key: str = ""
    replicate_api_token: str = ""
    nemotron_provider: str = "mock"
    nvidia_api_key: str = ""
    database_dsn: str = Field(default="", validation_alias="DATABASE_URL")
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def database_url(self) -> str:
        if self.database_dsn:
            return self.database_dsn
        db_path = ROOT_DIR / "northern_shift_guard.db"
        return f"sqlite:///{db_path}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
