"""
Evaluation metrics: MAE, RMSE, MAPE (when safe). Per-horizon and aggregate.
"""

from __future__ import annotations

import numpy as np


def compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    mask: np.ndarray | None = None,
) -> dict[str, float]:
    """y_true, y_pred: (T, N) or (T, N, H). mask same shape; 1 where valid."""
    if mask is None:
        mask = np.ones_like(y_true, dtype=np.float64)
    mask = np.asarray(mask, dtype=np.float64)
    diff = np.abs(y_true - y_pred)
    sq = (y_true - y_pred) ** 2
    n = np.maximum(mask.sum(), 1e-9)
    mae = (diff * mask).sum() / n
    rmse = np.sqrt((sq * mask).sum() / n)
    safe = np.isfinite(y_true) & (np.abs(y_true) > 1e-8) & (mask > 0.5)
    if np.any(safe):
        pct = np.abs((y_true - y_pred) / np.where(np.abs(y_true) > 1e-8, y_true, 1e-8))
        mape = float(
            (pct * mask * np.where(safe, 1.0, 0.0)).sum()
            / np.maximum((mask * safe).sum(), 1e-9)
            * 100.0
        )
    else:
        mape = float("nan")
    return {"mae": float(mae), "rmse": float(rmse), "mape": float(mape)}


def horizon_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    mask: np.ndarray | None = None,
) -> list[dict[str, float]]:
    """y_true, y_pred: (T, N, H). Return list of metrics per horizon step."""
    if y_true.ndim != 3 or y_pred.ndim != 3:
        return [compute_metrics(y_true, y_pred, mask)]
    H = y_true.shape[2]
    out = []
    for h in range(H):
        m = compute_metrics(
            y_true[..., h], y_pred[..., h], mask[..., h] if mask is not None else None
        )
        m["horizon_step"] = h
        out.append(m)
    return out
