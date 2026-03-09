"""
Federated server application for IRIDIUM. Flower ServerApp.

Initializes global model, runs FedAvg (or configurable strategy). Simulation and institution-lab modes only.
"""

from __future__ import annotations

from typing import Any

from flwr.common import Context
from flwr.server import ServerApp, ServerAppComponents, ServerConfig
from flwr.server.strategy import FedAvg


def server_fn(context: Context) -> Any:
    """Return ServerAppComponents for Flower (flwr 1.x)."""
    run_config = getattr(context, "run_config", None) or {}
    num_rounds = int(run_config.get("num_rounds", 3))
    min_clients = int(run_config.get("min_available_clients", 2))
    strategy = FedAvg(
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=min_clients,
        min_evaluate_clients=min_clients,
        min_available_clients=min_clients,
    )
    config = ServerConfig(num_rounds=num_rounds)
    return ServerAppComponents(strategy=strategy, config=config)


app = ServerApp(server_fn=server_fn)
