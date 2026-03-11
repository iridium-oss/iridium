"""
Base interface for forecasting models. Enables registry and unified inference.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import torch


class BaseForecastModel(ABC, torch.nn.Module):
    """Abstract base for Graph WaveNet, DCRNN, etc. Same input/output contract."""

    @abstractmethod
    def forward(
        self,
        x: torch.Tensor,
        adj: torch.Tensor | None = None,
        support: torch.Tensor | None = None,
        **kwargs: Any,
    ) -> torch.Tensor:
        """
        x: (B, T_in, N) or (B, T_in, N, C). Output: (B, T_out, N) or (B, T_out, N, C).
        """
        pass

    @property
    @abstractmethod
    def model_family(self) -> str:
        pass
