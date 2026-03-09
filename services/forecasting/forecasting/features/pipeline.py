"""
Deterministic feature pipeline. Same logic for training and inference.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import numpy as np

from .schema import FEATURE_NAMES


@dataclass
class FeatureCoverage:
    ratio: float
    missing_per_feature: dict[str, float]
    schema_version: str


def _rolling_mean(x: np.ndarray, w: int) -> np.ndarray:
    out = np.full_like(x, np.nan, dtype=np.float64)
    for i in range(w - 1, x.shape[0]):
        window = x[i - w + 1 : i + 1]
        if np.any(~np.isnan(window)):
            out[i] = np.nanmean(window)
    return out


def _rolling_std(x: np.ndarray, w: int) -> np.ndarray:
    out = np.full_like(x, np.nan, dtype=np.float64)
    for i in range(w - 1, x.shape[0]):
        window = x[i - w + 1 : i + 1]
        if np.sum(~np.isnan(window)) >= 2:
            out[i] = np.nanstd(window)
    return out


def build_features(
    target_matrix: np.ndarray,
    timestamps: Optional[list[datetime]] = None,
    schema_version: str = "v1",
) -> tuple[np.ndarray, FeatureCoverage]:
    """
    Build (T, N, F) feature tensor from (T, N) target matrix.
    Features: lags 1..3, rolling mean/std (w=3), hour and dow sin/cos.
    Deterministic; NaNs where inputs are missing.
    """
    T, N = target_matrix.shape
    F = len(FEATURE_NAMES)
    out = np.full((T, N, F), np.nan, dtype=np.float64)
    for n in range(N):
        x = target_matrix[:, n]
        out[:, n, 0] = np.roll(x, 1)
        out[0, n, 0] = np.nan
        out[:, n, 1] = np.roll(x, 2)
        out[:2, n, 1] = np.nan
        out[:, n, 2] = np.roll(x, 3)
        out[:3, n, 2] = np.nan
        out[:, n, 3] = _rolling_mean(x, 3)
        out[:, n, 4] = _rolling_std(x, 3)
        if timestamps and len(timestamps) == T:
            for t in range(T):
                dt = timestamps[t]
                h = dt.hour + dt.minute / 60.0
                d = dt.weekday()
                out[t, n, 5] = np.sin(2 * np.pi * h / 24.0)
                out[t, n, 6] = np.cos(2 * np.pi * h / 24.0)
                out[t, n, 7] = np.sin(2 * np.pi * d / 7.0)
                out[t, n, 8] = np.cos(2 * np.pi * d / 7.0)
    missing_per = {name: float(np.isnan(out[..., i]).mean()) for i, name in enumerate(FEATURE_NAMES)}
    ratio = 1.0 - float(np.isnan(out).mean())
    return out, FeatureCoverage(ratio=ratio, missing_per_feature=missing_per, schema_version=schema_version)
