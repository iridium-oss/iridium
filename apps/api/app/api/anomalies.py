"""
Anomalies endpoint.
"""

from datetime import UTC, datetime, timedelta

from anomaly_detection.detector import get_anomalies
from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/anomalies", summary="Active anomalies")
def get_anomalies_list(
    segment_ids: str | None = Query(None, description="Comma-separated segment IDs"),
    since: datetime | None = Query(None),
):
    """Return active anomalies (incidents, closures, demand surge). Baseline: rule-based."""
    seg_list = [s.strip() for s in (segment_ids or "").split(",") if s.strip()] or None
    since = since or (datetime.now(UTC) - timedelta(hours=24))
    result = get_anomalies(segment_ids=seg_list, since=since)
    return {
        "anomalies": [a.model_dump(mode="json") for a in result],
        "model_type": "rule_baseline",
        "model_maturity": "production_baseline",
        "data_status": "live",
        "note": "Rule-based detection from digital twin state only. No synthetic data.",
    }
