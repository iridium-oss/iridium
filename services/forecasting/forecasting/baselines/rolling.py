"""
Rolling mean baseline: forecast = mean of last W observations, repeated over horizon.
"""

from __future__ import annotations

import numpy as np


def rolling_mean_forecast(
    history: np.ndarray,
    horizon: int,
    window: int = 3,
) -> np.ndarray:
    """
    history: (T, N). forecast = mean(history[-window:], axis=0), repeated for each step.
    """
    if history.size == 0:
        return np.full((horizon, 1) if history.ndim == 2 else (horizon,), np.nan, dtype=np.float64)
    if history.ndim == 1:
        history = history.reshape(-1, 1)
    W = min(window, history.shape[0])
    tail = history[-W:]
    mu = np.nanmean(tail, axis=0)
    return np.broadcast_to(mu, (horizon, mu.shape[0])).astype(np.float64)
