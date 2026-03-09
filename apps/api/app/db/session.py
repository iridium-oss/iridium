"""
Session dependency for FastAPI handlers.
"""

from __future__ import annotations

from collections.abc import Generator
from typing import Optional

from sqlalchemy.orm import Session

from app.db.engine import get_engine


def get_db_session() -> Generator[Optional[Session], None, None]:
    engine = get_engine()
    if engine is None:
        yield None
        return
    with Session(engine) as session:
        yield session

