"""Task definition tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import pytest
from forecasting.task import ForecastingTaskSpec, ForecastTarget, ForecastGranularity, DEFAULT_TASK_SPEC


def test_default_task_spec():
    spec = DEFAULT_TASK_SPEC
    assert spec.horizon_minutes > 0
    assert spec.input_window_minutes > 0
    assert spec.min_coverage_ratio >= 0 and spec.min_coverage_ratio <= 1


def test_task_spec_validation():
    with pytest.raises(ValueError):
        ForecastingTaskSpec(horizon_minutes=0)
    with pytest.raises(ValueError):
        ForecastingTaskSpec(min_coverage_ratio=1.5)
