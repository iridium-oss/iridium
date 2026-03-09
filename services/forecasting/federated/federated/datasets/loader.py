"""
Load partition data for a client. Used by client_app only.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import numpy as np

from ..partitioning.partition import load_partition_data, load_partition_manifest
from ..partitioning.manifest import PartitionManifest


def load_client_data(
    client_id: str,
    data_dir: Path,
    manifests_dir: Optional[Path] = None,
) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[PartitionManifest]]:
    """
    Load (x, y) and manifest for a client. client_id maps to partition_id in simulation.

    Returns (x, y, manifest). If data insufficient or missing, returns (None, None, manifest or None).
    """
    if manifests_dir is None:
        manifests_dir = data_dir
    manifest = load_partition_manifest(client_id, manifests_dir)
    data = load_partition_data(client_id, data_dir)
    if data is None:
        return None, None, manifest
    x, y = data
    return x, y, manifest
