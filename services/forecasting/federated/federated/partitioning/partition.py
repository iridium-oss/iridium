"""
Partition generation and loading.

Generates partition manifests and provides partition data for clients.
No raw central merge; each partition is self-contained for FL training.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .manifest import PartitionManifest, PartitionStrategy


def generate_partitions(
    strategy: PartitionStrategy,
    num_partitions: int = 3,
    samples_per_partition: int = 100,
    feature_dim: int = 8,
    seed: int | None = 42,
    output_dir: Path | None = None,
) -> list[PartitionManifest]:
    """
    Generate partition manifests and, if output_dir is set, write manifest and data.

    For simulation we use synthetic data clearly marked in metadata.
    Real data partitions would be produced by a separate pipeline from product data.
    """
    if seed is not None:
        np.random.seed(seed)
    manifests: list[PartitionManifest] = []
    for i in range(num_partitions):
        pid = f"p_{strategy.value}_{i}"
        n = max(0, samples_per_partition + (i - num_partitions // 2) * 10)
        n = max(20, n)
        geo = f"district_{i}" if strategy == PartitionStrategy.BY_DISTRICT else None
        if strategy == PartitionStrategy.SYNTHETIC_INSTITUTION:
            meta = {"simulation_only": True, "synthetic": True}
        else:
            meta = {}
        m = PartitionManifest(
            partition_id=pid,
            strategy=strategy,
            coverage_interval_start="2024-01-01",
            coverage_interval_end="2024-01-31",
            source_types=["road", "metro"] if i % 2 == 0 else ["bus"],
            label_availability="full",
            sample_count=n,
            missingness_pct=0.0,
            geography=geo,
            metadata=meta,
        )
        manifests.append(m)
        if output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            manifest_path = output_dir / f"{pid}_manifest.json"
            manifest_path.write_text(m.model_dump_json(indent=2), encoding="utf-8")
            data_path = output_dir / f"{pid}_data.npz"
            x = np.random.randn(n, feature_dim).astype(np.float32)
            y = (x @ np.random.randn(feature_dim, 1) + 0.1 * np.random.randn(n, 1)).astype(
                np.float32
            )
            np.savez(data_path, x=x, y=y)
    return manifests


def load_partition_manifest(partition_id: str, manifests_dir: Path) -> PartitionManifest | None:
    """Load a single partition manifest by ID."""
    path = manifests_dir / f"{partition_id}_manifest.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return PartitionManifest.model_validate(data)


def load_partition_data(partition_id: str, data_dir: Path) -> tuple[np.ndarray, np.ndarray] | None:
    """Load (x, y) for a partition. Returns None if missing or insufficient."""
    path = data_dir / f"{partition_id}_data.npz"
    if not path.exists():
        return None
    with np.load(path) as z:
        x = z["x"]
        y = z["y"]
    if x.shape[0] < 10:
        return None
    return x, y
