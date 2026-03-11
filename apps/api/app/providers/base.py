"""
Provider abstraction for external data sources.

This layer defines a consistent fetch contract, provenance, and timing signals.
It does not implement scheduling. Callers decide when and how to fetch.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ProviderResult(Generic[T]):
    provider_id: str
    source_family: str
    source_status: str
    fetched_at: datetime
    source_url: str | None
    success: bool
    status_code: int | None = None
    duration_ms: int | None = None
    data: T | None = None
    error_class: str | None = None
    error_message: str | None = None
    confidence: str | None = None
    validation_note: str | None = None


class ProviderBase(Generic[T]):
    provider_id: str
    source_family: str
    source_status: str

    def fetch(self) -> ProviderResult[T]:
        raise NotImplementedError
