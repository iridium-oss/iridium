"""
Configuration from environment variables.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_BASE_URL: str = "http://localhost:8000"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    LOG_LEVEL: str = "INFO"
    DATA_SAMPLES_DIR: str = "data/samples"
    DATA_SYNTHETIC_DIR: str = "data/synthetic"
    EQUITY_DATA_PATH: str = ""
    APP_VERSION: str = "0.1.0-dev"

    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    def data_samples_path(self) -> Path:
        return Path(self.DATA_SAMPLES_DIR)

    def data_synthetic_path(self) -> Path:
        return Path(self.DATA_SYNTHETIC_DIR)

    def equity_data_path(self) -> Optional[Path]:
        p = Path(self.EQUITY_DATA_PATH).resolve() if self.EQUITY_DATA_PATH else None
        return p if p and p.exists() else None


@lru_cache
def get_settings() -> Settings:
    return Settings()
