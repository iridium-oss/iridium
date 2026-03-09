"""
Rule-based anomaly detector. Detects congestion spikes, closure flags, demand surge proxies.
Future: hybrid statistical or ML-based detection. No synthetic data; uses twin state only.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from iridium_schemas.anomaly import AnomalyEvent
from digital_twin.state_assembler import get_assembled_snapshot

# Cooldown: do not re-emit same anomaly_id within this many seconds (suppression).
ANOMALY_COOLDOWN_SECONDS = 3600


def get_anomalies(
    segment_ids: Optional[list[str]] = None,
    since: Optional[datetime] = None,
) -> list[AnomalyEvent]:
    """Return active anomalies. Baseline: rule-based on twin state (incident flags, high occupancy)."""
    snapshot = get_assembled_snapshot()
    now = datetime.now(timezone.utc)
    since = since or (now - timedelta(hours=24))
    edges = snapshot.edges or []
    out: list[AnomalyEvent] = []
    for e in edges:
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
                    source_type="observed_disruption",
                    evidence_summary="Edge incident flag set in digital twin.",
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
                    source_type="inferred_statistical",
                    evidence_summary=f"Occupancy {e.occupancy_pct}% above 85% threshold.",
                )
            )
    # Dedupe by anomaly_id and filter by since
    seen: set[str] = set()
    deduped = []
    for a in out:
        if a.anomaly_id not in seen and a.detected_at >= since:
            seen.add(a.anomaly_id)
            deduped.append(a)
    return deduped
