"""
Federated learning configuration. Validated via pydantic.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class FederatedConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="IRIDIUM_FL_", extra="ignore")

    data_dir: Optional[Path] = Field(None, description="Directory with partition manifests and data")
    artifacts_dir: Path = Field(Path("artifacts"), description="Where to save checkpoints and metrics")
    num_rounds: int = Field(3, ge=1, le=500)
    min_available_clients: int = Field(2, ge=1, le=100)
    local_epochs: int = Field(1, ge=1, le=50)
    batch_size: int = Field(32, ge=1, le=1024)
    learning_rate: float = Field(0.01, gt=0.0, le=1.0)
    num_partitions: int = Field(3, ge=1, le=100)
    seed: Optional[int] = Field(42, description="Reproducibility seed")

    @field_validator("data_dir", mode="before")
    @classmethod
    def path_from_str(cls, v: Optional[str]) -> Optional[Path]:
        if v is None or v == "":
            return None
        return Path(v)

    @field_validator("artifacts_dir", mode="before")
    @classmethod
    def artifacts_path(cls, v: str | Path) -> Path:
        return Path(v) if v else Path("artifacts")
