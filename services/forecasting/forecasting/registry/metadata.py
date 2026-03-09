"""
Model registry metadata. Every artifact has family, version, dataset/feature/graph version, maturity.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional


class ModelMaturity(str, Enum):
    DETERMINISTIC_BASELINE = "deterministic_baseline"
    STATISTICAL_BASELINE = "statistical_baseline"
    ML_BASELINE = "ml_baseline"
    CANDIDATE = "candidate"
    INACTIVE = "inactive"


def registry_metadata_from_training(
    model_family: str,
    model_version: str,
    dataset_version: str,
    feature_version: str,
    graph_version: Optional[str],
    training_config: dict[str, Any],
    evaluation_summary: Optional[dict[str, Any]],
    maturity: ModelMaturity = ModelMaturity.CANDIDATE,
) -> dict[str, Any]:
    return {
        "model_family": model_family,
        "model_version": model_version,
        "dataset_version": dataset_version,
        "feature_version": feature_version,
        "graph_version": graph_version or "v1",
        "training_config": training_config,
        "evaluation_summary": evaluation_summary,
        "maturity": maturity.value,
    }
