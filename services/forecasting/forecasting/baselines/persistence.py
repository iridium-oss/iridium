"""
Persistence baseline: forecast = last observed value.
"""

from __future__ import annotations

import numpy as np


def persistence_forecast(
    history: np.ndarray,
    horizon: int,
) -> np.ndarray:
    """
    history: (T, N) or (T,) last observed values (T = input window).
    horizon: number of steps to forecast.
    Returns: (horizon, N) or (horizon,) forecast; uses last row of history repeated.
    """
    if history.size == 0:
        return np.full((horizon, 1) if history.ndim == 2 else (horizon,), np.nan, dtype=np.float64)
    if history.ndim == 1:
        history = history.reshape(-1, 1)
    last = history[-1]
    return np.broadcast_to(last, (horizon, last.shape[0])).astype(np.float64)
