"""
Database engine and session factory.

DB is optional. When disabled, the API runs in stateless mode.
"""

from __future__ import annotations

from app.core.settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def create_db_engine() -> Engine | None:
    settings = get_settings()
    if not settings.db.enabled:
        return None
    if not settings.db.dsn:
        raise RuntimeError("Database is enabled but IRIDIUM_DB__DSN is not configured")
    dsn = settings.db.dsn.get_secret_value()
    return create_engine(dsn, pool_pre_ping=True)


_ENGINE: Engine | None = None


def get_engine() -> Engine | None:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = create_db_engine()
    return _ENGINE
