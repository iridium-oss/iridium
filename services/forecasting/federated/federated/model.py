"""
Shared model interface for federated congestion forecasting.

Simple linear regression in NumPy for FL: y = X @ w + b.
Parameters are a list of ndarrays [W, b] for Flower get_parameters/set_parameters.
Feature dimension and output dimension are fixed per run; no graph structure in this baseline.
"""

from __future__ import annotations

import numpy as np
from typing import List, Tuple

FEATURE_VERSION = "v1"
MODEL_VERSION = "linear_v1"


def create_model(
    input_dim: int = 8,
    output_dim: int = 1,
    seed: int | None = 42,
) -> Tuple["LinearModel", List[np.ndarray]]:
    """Create model and initial parameters. Deterministic if seed is set."""
    if seed is not None:
        np.random.seed(seed)
    model = LinearModel(input_dim=input_dim, output_dim=output_dim)
    params = model.get_parameters()
    return model, params


class LinearModel:
    """Linear regression for scalar or vector target. Parameters: [W, b]."""

    def __init__(self, input_dim: int = 8, output_dim: int = 1) -> None:
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.w = np.random.randn(input_dim, output_dim) * 0.01
        self.b = np.zeros((output_dim,))

    def get_parameters(self) -> List[np.ndarray]:
        return [self.w.copy(), self.b.copy()]

    def set_parameters(self, parameters: List[np.ndarray]) -> None:
        if len(parameters) != 2:
            raise ValueError("Expected [W, b]")
        self.w = parameters[0].copy()
        self.b = parameters[1].copy()

    def fit_epoch(
        self,
        x: np.ndarray,
        y: np.ndarray,
        lr: float = 0.01,
        batch_size: int = 32,
    ) -> Tuple[float, int]:
        """One epoch of MSE gradient descent. Returns (loss, num_samples)."""
        n = x.shape[0]
        if n == 0:
            return 0.0, 0
        total_loss = 0.0
        for start in range(0, n, batch_size):
            end = min(start + batch_size, n)
            x_b = x[start:end]
            y_b = y[start:end]
            pred = x_b @ self.w + self.b
            err = pred - y_b
            loss = float(np.mean(err ** 2))
            total_loss += loss * (end - start)
            grad_w = x_b.T @ err / (end - start)
            grad_b = np.mean(err, axis=0)
            self.w -= lr * grad_w
            self.b -= lr * grad_b
        return total_loss / n, n

    def evaluate(self, x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """MSE and MAE."""
        n = x.shape[0]
        if n == 0:
            return 0.0, 0.0
        pred = x @ self.w + self.b
        mse = float(np.mean((pred - y) ** 2))
        mae = float(np.mean(np.abs(pred - y)))
        return mse, mae
