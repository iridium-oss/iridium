"""
Forecasting task definition. Drives training and serving.

Target variables, horizon, granularity, input window, and degraded-mode policy
are defined here and in config. No synthetic targets; insufficient labels
downgrade the model path explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ForecastTarget(str, Enum):
    CONGESTION_SCORE = "congestion_score"
    SPEED_KMH = "speed_kmh"
    OCCUPANCY_PCT = "occupancy_pct"
    DELAY_PROXY = "delay_proxy"
    STRESS_INDEX = "stress_index"


class ForecastGranularity(str, Enum):
    NODE_LEVEL = "node"
    EDGE_LEVEL = "edge"
    CORRIDOR_LEVEL = "corridor"
    DISTRICT_SUMMARY = "district"


@dataclass
class ForecastingTaskSpec:
    """Canonical specification for the forecasting task. Used by dataset builder, training, and inference."""

    target: ForecastTarget = ForecastTarget.CONGESTION_SCORE
    horizon_minutes: int = 120
    horizon_steps: int = 8
    step_minutes: int = 15
    granularity: ForecastGranularity = ForecastGranularity.EDGE_LEVEL
    input_window_steps: int = 12
    input_window_minutes: int = 180
    training_cadence_minutes: int | None = 15
    inference_cadence_minutes: int | None = 15
    min_coverage_ratio: float = 0.5
    feature_schema_version: str = "v1"
    graph_version: str | None = None

    def __post_init__(self) -> None:
        if self.horizon_minutes <= 0 or self.input_window_minutes <= 0:
            raise ValueError("horizon_minutes and input_window_minutes must be positive")
        if self.min_coverage_ratio < 0.0 or self.min_coverage_ratio > 1.0:
            raise ValueError("min_coverage_ratio must be in [0, 1]")


DEFAULT_TASK_SPEC = ForecastingTaskSpec()

# Degraded-mode policy: when coverage or labels are below threshold, do not train or serve learned model;
# return deterministic_baseline or unavailable with explicit status in response.
