"""
Health check endpoint.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Liveness check")
def get_health() -> dict:
    """Return 200 when the service is up."""
    return {"status": "ok"}
