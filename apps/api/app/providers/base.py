"""
Provider abstraction for external data sources.

This layer defines a consistent fetch contract, provenance, and timing signals.
It does not implement scheduling. Callers decide when and how to fetch.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Generic, Optional, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class ProviderResult(Generic[T]):
    provider_id: str
    source_family: str
    source_status: str
    fetched_at: datetime
    source_url: Optional[str]
    success: bool
    status_code: Optional[int] = None
    duration_ms: Optional[int] = None
    data: Optional[T] = None
    error_class: Optional[str] = None
    error_message: Optional[str] = None
    confidence: Optional[str] = None
    validation_note: Optional[str] = None


class ProviderBase(Generic[T]):
    provider_id: str
    source_family: str
    source_status: str

    def fetch(self) -> ProviderResult[T]:
        raise NotImplementedError

