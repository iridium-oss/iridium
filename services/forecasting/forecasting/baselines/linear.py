"""
Simple temporal linear regression baseline (per entity): fit y = a * t + b on last window, extrapolate.
"""

from __future__ import annotations

import numpy as np


def linear_temporal_forecast(
    history: np.ndarray,
    horizon: int,
    window: int | None = None,
) -> np.ndarray:
    """
    Per-column: fit linear trend on last `window` steps (or all), extrapolate for horizon steps.
    """
    if history.size == 0:
        return np.full((horizon, 1) if history.ndim == 2 else (horizon,), np.nan, dtype=np.float64)
    if history.ndim == 1:
        history = history.reshape(-1, 1)
    T, N = history.shape
    W = min(window or T, T)
    if W < 2:
        last = history[-1]
        return np.broadcast_to(last, (horizon, N)).astype(np.float64)
    x = np.arange(W, dtype=np.float64)
    out = np.full((horizon, N), np.nan, dtype=np.float64)
    for n in range(N):
        y = history[-W:, n]
        valid = ~np.isnan(y)
        if np.sum(valid) < 2:
            out[:, n] = np.nanmean(y)
            continue
        xx, yy = x[valid], y[valid]
        A = np.stack([xx, np.ones_like(xx)], axis=1)
        coeffs, _, _, _ = np.linalg.lstsq(A, yy, rcond=None)
        a, b = coeffs[0], coeffs[1]
        for h in range(horizon):
            out[h, n] = a * (W + h) + b
    return out
