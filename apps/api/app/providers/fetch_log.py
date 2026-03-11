"""
Persistence for provider fetch outcomes.

This is best-effort: if DB is disabled, it returns without side effects.
"""

from __future__ import annotations

from app.db.models import SourceFetchLog
from app.providers.base import ProviderResult
from sqlalchemy.orm import Session


def record_fetch_log(session: Session | None, result: ProviderResult) -> None:
    if session is None:
        return
    log = SourceFetchLog(
        provider_id=result.provider_id,
        source_url=result.source_url,
        status_code=result.status_code,
        success=result.success,
        error_class=result.error_class,
        error_message=result.error_message,
        fetched_at=result.fetched_at,
        duration_ms=result.duration_ms,
    )
    session.add(log)
    session.commit()
