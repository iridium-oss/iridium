"""
DCRNN (Diffusion Convolutional Recurrent Neural Network) baseline for comparison.
Same I/O contract as Graph WaveNet; modular and separate from production path.
"""

from __future__ import annotations

from typing import Any

import torch
import torch.nn as nn

from ..common.base import BaseForecastModel
from ..common.graph_utils import normalize_adj_torch


class DCGRUCell(nn.Module):
    """Single cell: diffusion conv (support) then GRU update."""

    def __init__(self, num_nodes: int, input_dim: int, hidden_dim: int):
        super().__init__()
        self.gru = nn.GRUCell(2 * hidden_dim, hidden_dim)
        self.w_x = nn.Linear(input_dim, hidden_dim)
        self.w_h = nn.Linear(hidden_dim, hidden_dim)

    def forward(
        self,
        x: torch.Tensor,
        h: torch.Tensor,
        support: torch.Tensor,
    ) -> torch.Tensor:
        # x, h: (B, N, dim). support: (N, N)
        x_proj = self.w_x(x)
        h_proj = self.w_h(h)
        x_diff = torch.einsum("ij,bjc->bic", support, x_proj)
        h_diff = torch.einsum("ij,bjc->bic", support, h_proj)
        combined = torch.cat([x_diff, h_diff], dim=-1)
        B, N, _ = combined.shape
        return self.gru(combined.reshape(B * N, -1), h.reshape(B * N, -1)).reshape(B, N, -1)


class DCRNN(BaseForecastModel):
    """
    DCRNN: stack of DCGRU layers, then output projection to horizon.
    Input (B, T_in, N); output (B, horizon, N).
    """

    def __init__(
        self,
        num_nodes: int,
        input_len: int = 12,
        horizon: int = 8,
        input_dim: int | None = None,
        hidden_dim: int = 32,
        num_layers: int = 2,
        dropout: float = 0.3,
    ):
        super().__init__()
        self._num_nodes = num_nodes
        self._input_len = input_len
        self._horizon = horizon
        self._hidden_dim = hidden_dim
        self._num_layers = num_layers
        inp_dim = input_dim if input_dim is not None else 1
        self.cells = nn.ModuleList()
        self.cells.append(DCGRUCell(num_nodes, inp_dim, hidden_dim))
        for _ in range(num_layers - 1):
            self.cells.append(DCGRUCell(num_nodes, hidden_dim, hidden_dim))
        self.dropout = nn.Dropout(dropout)
        self.output_proj = nn.Linear(hidden_dim, horizon)

    @property
    def model_family(self) -> str:
        return "dcrnn"

    def forward(
        self,
        x: torch.Tensor,
        adj: torch.Tensor | None = None,
        support: torch.Tensor | None = None,
        **kwargs: Any,
    ) -> torch.Tensor:
        B, T_in, N = x.shape
        if self._num_nodes != N:
            raise ValueError(f"Expected {self._num_nodes} nodes, got {N}")
        if support is None and adj is not None:
            support = normalize_adj_torch(adj, add_self_loop=True)
        elif support is None:
            support = torch.eye(N, device=x.device, dtype=x.dtype)
        if support.dim() == 3:
            support = support.mean(dim=0)
        h = [
            torch.zeros(B, N, self._hidden_dim, device=x.device, dtype=x.dtype) for _ in self.cells
        ]
        for t in range(T_in):
            xt = x[:, t].unsqueeze(-1)
            for i, cell in enumerate(self.cells):
                inp = xt if i == 0 else h[i - 1]
                h[i] = cell(inp, h[i], support)
        out = self.dropout(h[-1])
        out = self.output_proj(out)
        out = out.transpose(1, 2)
        return out
