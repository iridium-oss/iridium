"""
Equity score endpoint. Real or recorded data only; no synthetic path.
"""

from equity.score import get_equity_scores
from fastapi import APIRouter, Query

from app.config import get_settings

router = APIRouter()


@router.get("/equity/score", summary="Mobility Equity Score")
def get_equity_score(
    district_ids: str | None = Query(None, description="Comma-separated district IDs"),
):
    """District-level equity indicators from real or recorded data. Returns data_status when no data configured."""
    settings = get_settings()
    data_dir = settings.equity_data_path()
    ids = [s.strip() for s in (district_ids or "").split(",") if s.strip()] or None
    result = get_equity_scores(district_ids=ids, data_dir=data_dir)
    return result.model_dump(mode="json")
