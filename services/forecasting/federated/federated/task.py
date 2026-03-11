"""
Model creation task for Flower. Used by both client and server to build the same architecture.
"""

from __future__ import annotations

import numpy as np

from .model import create_model


def get_model_input_dim() -> int:
    return 8


def get_model_output_dim() -> int:
    return 1


def build_model(seed: int | None = 42) -> tuple:
    """Return (model, initial_parameters) for the agreed architecture."""
    return create_model(
        input_dim=get_model_input_dim(),
        output_dim=get_model_output_dim(),
        seed=seed,
    )


def get_initial_parameters(seed: int | None = 42) -> list[np.ndarray]:
    """Return initial parameters only (for server initialization)."""
    _, params = build_model(seed=seed)
    return params
