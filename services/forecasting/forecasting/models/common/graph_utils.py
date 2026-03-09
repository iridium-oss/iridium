"""
Graph utilities for PyTorch models. Normalized adjacency and sparse handling.
"""

from __future__ import annotations

from typing import Optional

import torch


def normalize_adj_torch(adj: torch.Tensor, add_self_loop: bool = True) -> torch.Tensor:
    """Symmetric normalized adjacency: D^{-1/2} (A + I) D^{-1/2}."""
    if adj.dim() != 2 or adj.size(0) != adj.size(1):
        raise ValueError("adj must be square 2D")
    a = adj + torch.eye(adj.size(0), device=adj.device, dtype=adj.dtype) if add_self_loop else adj
    deg = a.sum(dim=1).clamp(min=1e-9)
    d_inv_sqrt = deg.pow(-0.5)
    return d_inv_sqrt.unsqueeze(1) * a * d_inv_sqrt.unsqueeze(0)


def sparse_to_torch(adj_np, device: Optional[torch.device] = None) -> torch.Tensor:
    """Convert numpy adjacency to torch float tensor."""
    import numpy as np
    t = torch.from_numpy(np.asarray(adj_np, dtype=np.float32))
    if device is not None:
        t = t.to(device)
    return t
