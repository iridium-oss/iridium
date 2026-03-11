"""Inference wrapper tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from pathlib import Path

import numpy as np
from forecasting.inference import ForecastInferenceWrapper


def test_wrapper_no_artifact_returns_none():
    wrapper = ForecastInferenceWrapper(
        artifact_dir=Path(__file__).resolve().parent / "nonexistent_artifacts"
    )
    loaded = wrapper.load(["e1", "e2"])
    assert loaded is False
    out = wrapper.predict(np.random.randn(12, 2).astype(np.float32), np.eye(2), ["e1", "e2"])
    assert out is None
