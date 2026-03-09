"""
Convert digital twin snapshot and real sources into observation rows for forecasting.
No synthetic data in production path.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

import numpy as np


@dataclass
class ObservationRow:
    timestamp_utc: datetime
    entity_id: str
    target_value: Optional[float]
    speed_kmh: Optional[float]
    occupancy_pct: Optional[float]
    congestion_score: Optional[float]
    source_completeness: float


def _congestion_from_speed_occupancy(speed_kmh: Optional[float], occupancy_pct: Optional[float]) -> Optional[float]:
    """Map speed and occupancy to a [0, 1] congestion score. Higher = more congested."""
    if speed_kmh is not None and occupancy_pct is not None:
        s = max(0.0, min(1.0, 1.0 - (speed_kmh or 0) / 120.0))
        o = (occupancy_pct or 0) / 100.0
        return float(0.5 * s + 0.5 * o)
    if speed_kmh is not None:
        return float(max(0.0, min(1.0, 1.0 - (speed_kmh or 0) / 120.0)))
    if occupancy_pct is not None:
        return (occupancy_pct or 0) / 100.0
    return None


def snapshot_to_observations(
    snapshot: Any,
    entity_id_key: str = "edge_id",
) -> list[ObservationRow]:
    """
    Convert a digital twin snapshot (nodes, edges) into one observation row per edge per snapshot time.
    Uses only real fields: speed_kmh, occupancy_pct. No synthetic values.
    """
    rows: list[ObservationRow] = []
    ts = getattr(snapshot, "snapshot_at", None) or (snapshot.get("snapshot_at") if isinstance(snapshot, dict) else None)
    if not ts:
        ts = datetime.now(timezone.utc)
    if isinstance(ts, str):
        try:
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            ts = datetime.now(timezone.utc)
    edges = getattr(snapshot, "edges", None) or (snapshot.get("edges") if isinstance(snapshot, dict) else [])
    for e in edges:
        eid = getattr(e, "edge_id", None) or (e.get("edge_id") if isinstance(e, dict) else None)
        if not eid:
            continue
        speed = getattr(e, "speed_kmh", None)
        if speed is None and isinstance(e, dict):
            speed = e.get("speed_kmh")
        occ = getattr(e, "occupancy_pct", None)
        if occ is None and isinstance(e, dict):
            occ = e.get("occupancy_pct")
        target = _congestion_from_speed_occupancy(speed, occ)
        completeness = 1.0 if (speed is not None or occ is not None) else 0.0
        rows.append(
            ObservationRow(
                timestamp_utc=ts,
                entity_id=str(eid),
                target_value=target,
                speed_kmh=float(speed) if speed is not None else None,
                occupancy_pct=float(occ) if occ is not None else None,
                congestion_score=target,
                source_completeness=completeness,
            )
        )
    return rows


def align_observations_to_matrix(
    rows: list[ObservationRow],
    entity_order: list[str],
    value_key: str = "congestion_score",
) -> tuple[np.ndarray, np.ndarray]:
    """
    Build (T, N) matrix of values and (T, N) mask from observation rows.
    entity_order defines column index per entity_id; missing values are NaN and mask 0.
    """
    if not entity_order:
        return np.zeros((0, 0), dtype=np.float64), np.zeros((0, 0), dtype=np.float64)
    e2i = {e: i for i, e in enumerate(entity_order)}
    # Group by timestamp
    from collections import defaultdict
    by_ts: dict[datetime, list[ObservationRow]] = defaultdict(list)
    for r in rows:
        by_ts[r.timestamp_utc].append(r)
    sorted_ts = sorted(by_ts.keys())
    T, N = len(sorted_ts), len(entity_order)
    mat = np.full((T, N), np.nan, dtype=np.float64)
    mask = np.zeros((T, N), dtype=np.float64)
    for t, ts in enumerate(sorted_ts):
        for r in by_ts[ts]:
            i = e2i.get(r.entity_id)
            if i is None:
                continue
            val = getattr(r, value_key, None) or r.target_value
            if val is not None:
                mat[t, i] = float(val)
                mask[t, i] = 1.0
    return mat, mask
