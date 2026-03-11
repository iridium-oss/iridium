"""
Session dependency for FastAPI handlers.
"""

from __future__ import annotations

from collections.abc import Generator

from app.db.engine import get_engine
from sqlalchemy.orm import Session


def get_db_session() -> Generator[Session | None, None, None]:
    engine = get_engine()
    if engine is None:
        yield None
        return
    with Session(engine) as session:
        yield session
