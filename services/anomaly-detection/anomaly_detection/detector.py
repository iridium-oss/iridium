"""
Rule-based anomaly detector. Detects congestion spikes, closure flags, demand surge proxies.
Future: hybrid statistical or ML-based detection.
"""

from datetime import datetime, timedelta
from typing import Optional

from iridium_schemas.anomaly import AnomalyEvent
from digital_twin.service import get_snapshot


def get_anomalies(
    segment_ids: Optional[list[str]] = None,
    since: Optional[datetime] = None,
) -> list[AnomalyEvent]:
    """Return active anomalies. Baseline: rule-based on twin state (incident flags, high occupancy)."""
    snapshot = get_snapshot()
    now = datetime.utcnow()
    since = since or (now - timedelta(hours=24))
    out: list[AnomalyEvent] = []
    for e in snapshot.edges:
        if segment_ids and e.edge_id not in segment_ids:
            continue
        if e.incident:
            out.append(
                AnomalyEvent(
                    anomaly_id=f"inc-{e.edge_id}",
                    type="incident",
                    severity="medium",
                    segment_ids=[e.edge_id],
                    detected_at=now,
                    valid_from=snapshot.snapshot_at,
                    description="Incident flag on segment",
                    recommended_response="Consider reroute.",
                )
            )
        if (e.occupancy_pct or 0) > 85:
            out.append(
                AnomalyEvent(
                    anomaly_id=f"cong-{e.edge_id}",
                    type="demand_surge",
                    severity="low",
                    segment_ids=[e.edge_id],
                    detected_at=now,
                    description="High occupancy",
                    recommended_response="Monitor; reroute if persistent.",
                )
            )
    # Dedupe by anomaly_id
    seen: set[str] = set()
    deduped = []
    for a in out:
        if a.anomaly_id not in seen and a.detected_at >= since:
            seen.add(a.anomaly_id)
            deduped.append(a)
    return deduped
