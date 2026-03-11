"""
Federated client application for IRIDIUM. Flower ClientApp.

Each client loads only its partition data, trains the model locally, and returns
updates and metrics. Fails gracefully if local data is insufficient.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from flwr.client import Client, NumPyClient
from flwr.common import Context
from flwr.common.typing import Config, Scalar

try:
    from flwr.client.client_app import ClientApp
except ImportError:
    from flwr.client import ClientApp  # type: ignore

from .datasets.loader import load_client_data
from .task import build_model, get_model_input_dim, get_model_output_dim


def _get_partition_id(context: Context, num_partitions: int) -> str:
    """Map node_id to partition_id for simulation."""
    node_id = getattr(context, "node_id", 0) or 0
    idx = int(node_id) % max(1, num_partitions)
    return f"p_by_district_{idx}"


def _get_data_dir(context: Context) -> Path | None:
    run_config = getattr(context, "run_config", None) or {}
    data_dir = run_config.get("data_dir")
    if data_dir is None:
        return None
    return Path(str(data_dir))


class IridiumNumPyClient(NumPyClient):
    """NumPy client for congestion forecasting model. Uses partition data only."""

    def __init__(
        self,
        partition_id: str,
        x: np.ndarray | None,
        y: np.ndarray | None,
        local_epochs: int = 1,
        batch_size: int = 32,
        learning_rate: float = 0.01,
    ) -> None:
        self.partition_id = partition_id
        self.x = x
        self.y = y
        self.local_epochs = local_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.model, _ = build_model(seed=42)

    def get_parameters(self, config: Config) -> list[np.ndarray]:
        return self.model.get_parameters()

    def fit(
        self, parameters: list[np.ndarray], config: Config
    ) -> tuple[list[np.ndarray], int, dict[str, Scalar]]:
        if self.x is None or self.y is None or self.x.shape[0] < 10:
            return self.model.get_parameters(), 0, {"insufficient_data": 1.0, "num_samples": 0}
        self.model.set_parameters(list(parameters))
        lr = float(config.get("learning_rate", self.learning_rate))
        epochs = int(config.get("local_epochs", self.local_epochs))
        total_loss = 0.0
        total_samples = 0
        for _ in range(epochs):
            loss, n = self.model.fit_epoch(self.x, self.y, lr=lr, batch_size=self.batch_size)
            total_loss += loss
            total_samples = n
        mse, mae = self.model.evaluate(self.x, self.y)
        return (
            self.model.get_parameters(),
            total_samples,
            {
                "loss": total_loss / max(1, epochs),
                "mse": mse,
                "mae": mae,
                "num_samples": total_samples,
                "partition_id": self.partition_id,
            },
        )

    def evaluate(
        self, parameters: list[np.ndarray], config: Config
    ) -> tuple[float, int, dict[str, Scalar]]:
        if self.x is None or self.y is None or self.x.shape[0] < 5:
            return 0.0, 0, {"mae": 0.0, "num_samples": 0}
        self.model.set_parameters(parameters)
        mse, mae = self.model.evaluate(self.x, self.y)
        n = self.x.shape[0]
        return float(mse), n, {"mae": mae, "num_samples": n, "partition_id": self.partition_id}

    def get_properties(self, config: Config) -> dict[str, Scalar]:
        return {
            "partition_id": self.partition_id,
            "input_dim": get_model_input_dim(),
            "output_dim": get_model_output_dim(),
        }


def client_fn(context: Context) -> Client:
    """Build a client for this node. Uses run_config data_dir and node_id for partition."""
    data_dir = _get_data_dir(context)
    num_partitions = int((getattr(context, "run_config", None) or {}).get("num_partitions", 3))
    partition_id = _get_partition_id(context, num_partitions)
    if data_dir is None or not data_dir.exists():
        client = IridiumNumPyClient(partition_id, None, None)
        return client.to_client()
    x, y, _ = load_client_data(partition_id, data_dir, data_dir)
    local_epochs = int((getattr(context, "run_config", None) or {}).get("local_epochs", 1))
    batch_size = int((getattr(context, "run_config", None) or {}).get("batch_size", 32))
    lr = float((getattr(context, "run_config", None) or {}).get("learning_rate", 0.01))
    client = IridiumNumPyClient(
        partition_id, x, y, local_epochs=local_epochs, batch_size=batch_size, learning_rate=lr
    )
    return client.to_client()


app = ClientApp(client_fn=client_fn)
