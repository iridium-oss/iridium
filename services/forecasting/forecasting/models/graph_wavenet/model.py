"""
Graph WaveNet: spatial-temporal model with adaptive adjacency and dilated temporal convolution.
Repository-native PyTorch implementation for IRIDIUM forecasting.
"""

from __future__ import annotations

from typing import Any

import torch
import torch.nn as nn

from ..common.base import BaseForecastModel
from ..common.graph_utils import normalize_adj_torch


class GatedTemporalConv(nn.Module):
    """Causal 1D conv with gating. Left-pad so output length = input length. Input (B, C, T); output (B, out_channels, T)."""

    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 2):
        super().__init__()
        self.conv = nn.Conv1d(in_channels, 2 * out_channels, kernel_size)
        self._kernel_size = kernel_size

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        pad = (self._kernel_size - 1, 0)
        x = torch.nn.functional.pad(x, pad)
        out = self.conv(x)
        p, q = out.chunk(2, dim=1)
        return torch.tanh(p) * torch.sigmoid(q)


class GraphConvLayer(nn.Module):
    """Graph convolution: H = sigma( support @ X @ W ). support can be (N,N) or (2, N, N) for two supports."""

    def __init__(self, in_dim: int, out_dim: int):
        super().__init__()
        self.linear = nn.Linear(in_dim, out_dim)

    def forward(
        self,
        x: torch.Tensor,
        support: torch.Tensor,
    ) -> torch.Tensor:
        # x: (B, T, N, C). support: (N, N) or (K, N, N)
        if support.dim() == 3:
            support = support.mean(dim=0)
        out = torch.einsum("ij,btjc->btic", support, x)
        return self.linear(out)


class GraphWaveNet(BaseForecastModel):
    """
    Graph WaveNet: K layers of Gated TCN + Graph Conv with residual and skip.
    Adaptive adjacency from node embeddings; optional predefined support.
    Input (B, T_in, N); output (B, T_out, N). T_out = horizon_steps.
    """

    def __init__(
        self,
        num_nodes: int,
        in_channels: int = 1,
        out_channels: int = 1,
        input_len: int = 12,
        horizon: int = 8,
        hidden_dim: int = 32,
        num_layers: int = 4,
        kernel_size: int = 2,
        dropout: float = 0.3,
        use_adaptive_adj: bool = True,
    ):
        super().__init__()
        self._num_nodes = num_nodes
        self._input_len = input_len
        self._horizon = horizon
        self._hidden_dim = hidden_dim
        self._use_adaptive_adj = use_adaptive_adj
        self.start_conv = nn.Conv1d(1, hidden_dim, 1)
        self.receptive_field = 1
        self.tcn_layers = nn.ModuleList()
        self.gcn_layers = nn.ModuleList()
        for _ in range(num_layers):
            self.tcn_layers.append(GatedTemporalConv(hidden_dim, hidden_dim, kernel_size))
            self.receptive_field += (kernel_size - 1) * (2 ** min(_, 10))
            self.gcn_layers.append(GraphConvLayer(hidden_dim, hidden_dim))
        self.receptive_field = min(self.receptive_field, input_len)

        if use_adaptive_adj:
            self.node_emb1 = nn.Parameter(torch.randn(num_nodes, 10))
            self.node_emb2 = nn.Parameter(torch.randn(10, num_nodes))

        self.skip_layers = nn.ModuleList(
            [nn.Conv1d(hidden_dim, hidden_dim, 1) for _ in range(num_layers)]
        )
        self.end_conv_1 = nn.Conv1d(hidden_dim, 16, 1)
        self.end_conv_2 = nn.Conv1d(16, horizon, 1)
        self.dropout = nn.Dropout(dropout)

    @property
    def model_family(self) -> str:
        return "graph_wavenet"

    def _adaptive_support(self, device: torch.device) -> torch.Tensor:
        adj = torch.relu(torch.mm(self.node_emb1, self.node_emb2))
        return normalize_adj_torch(adj, add_self_loop=True)

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
        x = x.permute(0, 2, 1).reshape(B * N, 1, T_in)
        x = self.start_conv(x)
        x = x.view(B, N, -1, T_in).permute(0, 3, 1, 2)
        skip = 0
        for tcn, gcn, skip_conv in zip(self.tcn_layers, self.gcn_layers, self.skip_layers):
            residual = x
            xt = x.permute(0, 2, 1, 3).reshape(B * N, -1, T_in)
            xt = tcn(xt)
            x = xt.view(B, N, -1, T_in).permute(0, 3, 1, 2)
            if support is not None:
                supp = support
            else:
                supp = self._adaptive_support(x.device)
            x = gcn(x, supp)
            x = self.dropout(x)
            x = x + residual
            sk = x.permute(0, 2, 1, 3).reshape(B * N, -1, T_in)
            skip = skip + skip_conv(sk)
        x = torch.relu(skip)
        x = torch.relu(self.end_conv_1(x))
        x = self.end_conv_2(x)
        x = x[..., -1].view(B, N, self._horizon).permute(0, 2, 1)
        return x
