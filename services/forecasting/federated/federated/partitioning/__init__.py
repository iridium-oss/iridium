"""
Data partitioning for federated learning.

Strategies: by district, by provider/source_family, by time block, synthetic institution (simulation only).
Partition manifests are versioned and include coverage, sample counts, and quality metadata.
"""

from .manifest import PartitionManifest, PartitionStrategy
from .partition import generate_partitions, load_partition_manifest

__all__ = [
    "PartitionManifest",
    "PartitionStrategy",
    "generate_partitions",
    "load_partition_manifest",
]
