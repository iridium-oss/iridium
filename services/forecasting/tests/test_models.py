"""Model forward pass tests."""

import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

import torch
from forecasting.models import DCRNN, GraphWaveNet


def test_graph_wavenet_forward():
    N, T_in, H = 5, 12, 8
    model = GraphWaveNet(num_nodes=N, input_len=T_in, horizon=H)
    x = torch.rand(2, T_in, N)
    support = torch.eye(N) + torch.rand(N, N) * 0.1
    support = support / support.sum(dim=1, keepdim=True)
    out = model(x, support=support)
    assert out.shape == (2, H, N)
    assert out.isfinite().all()


def test_dcrnn_forward():
    N, T_in, H = 5, 12, 8
    model = DCRNN(num_nodes=N, input_len=T_in, horizon=H)
    x = torch.rand(2, T_in, N)
    support = torch.eye(N)
    out = model(x, support=support)
    assert out.shape == (2, H, N)
    assert out.isfinite().all()
