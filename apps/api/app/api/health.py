"""
Health check endpoint.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.db.engine import get_engine

router = APIRouter()


@router.get("/health", summary="Liveness check")
def get_health() -> dict:
    """Return 200 when the service is up."""
    return {"status": "ok"}


@router.get(
    "/ready",
    summary="Readiness check",
    description="Reports whether the service is ready to serve traffic. Does not guarantee external providers.",
)
def get_ready() -> dict:
    settings = get_settings()
    now = datetime.now(timezone.utc).isoformat()

    checks: dict[str, dict] = {}
    ok = True

    if settings.db.enabled:
        try:
            engine = get_engine()
            if engine is None:
                ok = False
                checks["database"] = {"ok": False, "note": "DB enabled but engine not available"}
            else:
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                checks["database"] = {"ok": True}
        except SQLAlchemyError:
            ok = False
            checks["database"] = {"ok": False, "note": "DB connection failed"}
    else:
        checks["database"] = {"ok": True, "note": "disabled"}

    if settings.cache.enabled:
        try:
            import redis

            r = redis.Redis.from_url(settings.cache.redis_url.get_secret_value())
            r.ping()
            checks["cache"] = {"ok": True}
        except Exception:
            ok = False
            checks["cache"] = {"ok": False, "note": "Redis connection failed"}
    else:
        checks["cache"] = {"ok": True, "note": "disabled"}

    payload = {"status": "ready" if ok else "not_ready", "time_utc": now, "checks": checks}
    return JSONResponse(status_code=200 if ok else 503, content=payload)
