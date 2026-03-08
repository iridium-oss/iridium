"""
Forecasting pipeline: data prep, feature assembly, baseline predictor.
Uses digital twin from state assembler when available. Sets data_status from twin; no fabricated metrics.
"""

from datetime import datetime, timedelta
from typing import Optional

from iridium_schemas.forecast import CongestionForecastResponse, ForecastSegment
from iridium_schemas.provenance import DATA_STATUS_CONFIGURATION_REQUIRED
from digital_twin.state_assembler import get_assembled_snapshot


def _baseline_congestion(segment_id: str, horizon_minutes: int, snapshot_edges: list, step_min: int = 15) -> list[ForecastSegment]:
    """Heuristic baseline from twin edges when present. No trained model; no fabricated observations."""
    now = datetime.utcnow()
    segments: list[ForecastSegment] = []
    base_speed = 30.0
    base_occupancy = 0.2
    for e in snapshot_edges:
        if getattr(e, "edge_id", None) == segment_id or not segment_id:
            base_speed = getattr(e, "speed_kmh", None) or 30.0
            base_occupancy = (getattr(e, "occupancy_pct", None) or 20.0) / 100.0
            if segment_id:
                break
    seg_id = segment_id or (snapshot_edges[0].edge_id if snapshot_edges else "default")
    for i in range(0, horizon_minutes + 1, step_min):
        t = now + timedelta(minutes=i)
        decay = 1.0 - 0.3 * (i / max(horizon_minutes, 1))
        congestion = min(1.0, base_occupancy * decay + 0.3 * (1 - decay))
        speed = max(5.0, base_speed * (1.0 - 0.5 * congestion))
        segments.append(
            ForecastSegment(
                segment_id=seg_id,
                timestamp=t,
                speed_kmh=round(speed, 1),
                congestion_score=round(congestion, 3),
                occupancy_pct=round(congestion * 100, 1),
            )
        )
    return segments


def get_congestion_forecast(
    horizon_minutes: int = 120,
    segment_ids: Optional[list[str]] = None,
) -> CongestionForecastResponse:
    """Return congestion forecast. Data status from twin; heuristic when no real model."""
    snapshot = get_assembled_snapshot()
    data_status = snapshot.data_status or DATA_STATUS_CONFIGURATION_REQUIRED
    if segment_ids:
        all_segments = []
        for seg_id in segment_ids[:10]:
            all_segments.extend(_baseline_congestion(seg_id, horizon_minutes, snapshot.edges))
        segments = sorted(all_segments, key=lambda s: (s.segment_id, s.timestamp))
    else:
        segments = _baseline_congestion("", horizon_minutes, snapshot.edges)
    return CongestionForecastResponse(
        segments=segments,
        horizon_minutes=horizon_minutes,
        generated_at=datetime.utcnow(),
        model_version="baseline-heuristic",
        note="Heuristic from twin state. Real-data training and ST-GNN planned.",
        data_status=data_status,
    )
