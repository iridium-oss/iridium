"""Partitioning tests: manifest, generation, load."""

from pathlib import Path
import tempfile

import pytest

from federated.partitioning import PartitionManifest, PartitionStrategy, generate_partitions, load_partition_manifest
from federated.partitioning.partition import load_partition_data


def test_generate_partitions_returns_manifests():
    manifests = generate_partitions(
        strategy=PartitionStrategy.BY_DISTRICT,
        num_partitions=3,
        samples_per_partition=50,
        feature_dim=8,
        seed=42,
        output_dir=None,
    )
    assert len(manifests) == 3
    for m in manifests:
        assert m.partition_id.startswith("p_by_district_")
        assert m.sample_count >= 20
        assert m.strategy == PartitionStrategy.BY_DISTRICT
        assert m.label_availability == "full"


def test_generate_partitions_writes_files():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d)
        manifests = generate_partitions(
            strategy=PartitionStrategy.SYNTHETIC_INSTITUTION,
            num_partitions=2,
            samples_per_partition=30,
            feature_dim=8,
            seed=1,
            output_dir=path,
        )
        assert len(manifests) == 2
        for m in manifests:
            assert (path / f"{m.partition_id}_manifest.json").exists()
            assert (path / f"{m.partition_id}_data.npz").exists()
            loaded = load_partition_manifest(m.partition_id, path)
            assert loaded is not None
            assert loaded.partition_id == m.partition_id
            data = load_partition_data(m.partition_id, path)
            assert data is not None
            x, y = data
            assert x.shape[0] >= 20
            assert x.shape[1] == 8
            assert y.shape[0] == x.shape[0]


def test_synthetic_institution_manifest_has_simulation_flag():
    manifests = generate_partitions(
        strategy=PartitionStrategy.SYNTHETIC_INSTITUTION,
        num_partitions=1,
        samples_per_partition=40,
        seed=0,
        output_dir=None,
    )
    assert len(manifests) == 1
    assert manifests[0].metadata.get("simulation_only") is True
    assert manifests[0].metadata.get("synthetic") is True
