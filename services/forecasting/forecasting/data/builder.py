"""
Build time-aligned forecasting dataset from real sources. Produces manifest and arrays.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

import numpy as np

from .sources import ObservationRow, align_observations_to_matrix, snapshot_to_observations


@dataclass
class DatasetManifest:
    source_coverage: list[str] = field(default_factory=list)
    time_span_start: Optional[datetime] = None
    time_span_end: Optional[datetime] = None
    geography: str = "baku"
    missingness_ratio: float = 0.0
    label_availability: float = 0.0
    feature_availability: float = 0.0
    data_freshness_seconds: Optional[float] = None
    num_entities: int = 0
    num_timesteps: int = 0
    dataset_version: str = "v1"


def build_forecast_dataset(
    snapshots: list[Any],
    entity_order: list[str],
    target_key: str = "congestion_score",
) -> tuple[np.ndarray, np.ndarray, DatasetManifest]:
    """
    Build (T, N) target matrix and (T, N) mask from list of digital twin snapshots.
    Uses only real data; no synthetic fill. Manifest records coverage and availability.
    """
    if not entity_order:
        manifest = DatasetManifest(dataset_version="v1")
        return np.zeros((0, 0), dtype=np.float64), np.zeros((0, 0), dtype=np.float64), manifest
    all_rows: list[ObservationRow] = []
    for snap in snapshots or []:
        all_rows.extend(snapshot_to_observations(snap, entity_id_key="edge_id"))
    mat, mask = align_observations_to_matrix(all_rows, entity_order, value_key=target_key)
    T, N = mat.shape
    total = T * N
    available = float(np.sum(mask))
    missingness = 1.0 - (available / total) if total else 0.0
    label_availability = available / total if total else 0.0
    times = sorted({r.timestamp_utc for r in all_rows})
    span_start = times[0] if times else None
    span_end = times[-1] if times else None
    freshness = None
    if span_end:
        freshness = (datetime.now(timezone.utc) - span_end).total_seconds()
    manifest = DatasetManifest(
        source_coverage=["digital_twin_edges"],
        time_span_start=span_start,
        time_span_end=span_end,
        geography="baku",
        missingness_ratio=missingness,
        label_availability=label_availability,
        feature_availability=label_availability,
        data_freshness_seconds=freshness,
        num_entities=N,
        num_timesteps=T,
        dataset_version="v1",
    )
    return mat, mask, manifest
