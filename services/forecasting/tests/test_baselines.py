"""Baseline predictor tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import numpy as np
from forecasting.baselines import persistence_forecast, rolling_mean_forecast, linear_temporal_forecast


def test_persistence():
    h = np.array([[1.0, 2.0], [1.5, 2.5], [2.0, 3.0]])
    out = persistence_forecast(h, horizon=3)
    assert out.shape == (3, 2)
    np.testing.assert_allclose(out[0], [2.0, 3.0])
    np.testing.assert_allclose(out[1], [2.0, 3.0])


def test_rolling_mean():
    h = np.array([[1.0], [2.0], [3.0], [4.0]])
    out = rolling_mean_forecast(h, horizon=2, window=3)
    assert out.shape == (2, 1)
    expected = (2.0 + 3.0 + 4.0) / 3.0
    np.testing.assert_allclose(out[:, 0], expected)


def test_linear_temporal():
    h = np.array([[1.0], [2.0], [3.0], [4.0]])
    out = linear_temporal_forecast(h, horizon=2, window=4)
    assert out.shape == (2, 1)
    assert np.all(np.isfinite(out))
