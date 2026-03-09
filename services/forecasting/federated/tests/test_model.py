"""Model tests: create, get/set parameters, fit_epoch, evaluate."""

import numpy as np
import pytest

from federated.model import LinearModel, create_model
from federated.task import build_model, get_initial_parameters


def test_create_model_deterministic():
    m1, p1 = create_model(input_dim=4, output_dim=1, seed=42)
    m2, p2 = create_model(input_dim=4, output_dim=1, seed=42)
    assert len(p1) == 2
    assert p1[0].shape == (4, 1)
    assert p1[1].shape == (1,)
    np.testing.assert_array_almost_equal(p1[0], p2[0])
    np.testing.assert_array_almost_equal(p1[1], p2[1])


def test_linear_model_fit_epoch():
    model = LinearModel(input_dim=4, output_dim=1)
    np.random.seed(0)
    x = np.random.randn(64, 4).astype(np.float32)
    y = (x @ np.array([[1.0], [0.5], [-0.3], [0.2]]) + 0.1).astype(np.float32)
    loss_before, _ = model.evaluate(x, y)
    loss_after_epoch, n = model.fit_epoch(x, y, lr=0.01, batch_size=16)
    assert n == 64
    loss_after, _ = model.evaluate(x, y)
    assert loss_after <= loss_before + 0.01


def test_linear_model_set_get_parameters():
    model, params = build_model(seed=42)
    model.set_parameters([p + 1.0 for p in params])
    got = model.get_parameters()
    assert len(got) == 2
    np.testing.assert_array_almost_equal(got[0], params[0] + 1.0)
    np.testing.assert_array_almost_equal(got[1], params[1] + 1.0)


def test_get_initial_parameters():
    params = get_initial_parameters(seed=99)
    assert len(params) == 2
    assert params[0].ndim == 2
    assert params[1].ndim == 1
