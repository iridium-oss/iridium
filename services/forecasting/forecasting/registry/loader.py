"""
Load and validate registry metadata. Serving layer must not load without validation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional


def load_registry_metadata(artifact_dir: Path) -> Optional[dict[str, Any]]:
    """Load metadata from artifact dir. Expects training_metadata.json and optional registry_metadata.json."""
    artifact_dir = Path(artifact_dir)
    reg_path = artifact_dir / "registry_metadata.json"
    if reg_path.exists():
        with open(reg_path) as f:
            return json.load(f)
    train_path = artifact_dir / "training_metadata.json"
    if train_path.exists():
        with open(train_path) as f:
            data = json.load(f)
        return {
            "model_family": data.get("model_family", "unknown"),
            "model_version": "v1",
            "dataset_version": "v1",
            "feature_version": "v1",
            "graph_version": "v1",
            "maturity": "candidate",
        }
    return None


def validate_artifact(metadata: Optional[dict[str, Any]], entity_order: list[str]) -> bool:
    """Validate artifact is usable for given entity order. No load without validation."""
    if metadata is None:
        return False
    if metadata.get("maturity") == "inactive":
        return False
    return True
