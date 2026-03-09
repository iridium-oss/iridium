"""
Anomalies endpoint.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Query

from anomaly_detection.detector import get_anomalies

router = APIRouter()


@router.get("/anomalies", summary="Active anomalies")
def get_anomalies_list(
    segment_ids: Optional[str] = Query(None, description="Comma-separated segment IDs"),
    since: Optional[datetime] = Query(None),
):
    """Return active anomalies (incidents, closures, demand surge). Baseline: rule-based."""
    seg_list = [s.strip() for s in (segment_ids or "").split(",") if s.strip()] or None
    since = since or (datetime.now(timezone.utc) - timedelta(hours=24))
    result = get_anomalies(segment_ids=seg_list, since=since)
    return {"anomalies": [a.model_dump(mode="json") for a in result]}
