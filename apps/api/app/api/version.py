"""
Version endpoint for debugging.
"""

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter()


@router.get("/version", summary="API and service version")
def get_version() -> dict:
    """Return API version and service identifier."""
    settings = get_settings()
    return {"api_version": "v1", "app_version": settings.APP_VERSION, "service": "iridium-api"}
