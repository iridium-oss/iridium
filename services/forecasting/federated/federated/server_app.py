"""
Federated server application for IRIDIUM. Flower ServerApp.

Initializes global model, runs FedAvg (or configurable strategy). Simulation and institution-lab modes only.
"""

from __future__ import annotations

from typing import Any

from flwr.common import Context

try:
    from flwr.server import ServerApp, ServerAppComponents, ServerConfig
    from flwr.server.strategy import FedAvg
except ImportError:
    from flwr.serverapp import ServerApp
    from flwr.serverapp.strategy import FedAvg
    ServerAppComponents = getattr(__import__("flwr.serverapp", fromlist=["ServerAppComponents"]), "ServerAppComponents", None)
    ServerConfig = getattr(__import__("flwr.serverapp", fromlist=["ServerConfig"]), "ServerConfig", None)


def server_fn(context: Context) -> Any:
    """Return ServerAppComponents for Flower."""
    run_config = getattr(context, "run_config", None) or {}
    num_rounds = int(run_config.get("num_rounds", 3))
    min_clients = int(run_config.get("min_available_clients", 2))
    try:
        strategy = FedAvg(
            fraction_fit=1.0,
            fraction_evaluate=1.0,
            min_fit_clients=min_clients,
            min_evaluate_clients=min_clients,
            min_available_clients=min_clients,
        )
    except TypeError:
        strategy = FedAvg(
            fraction_train=1.0,
            fraction_evaluate=1.0,
            min_train_nodes=min_clients,
            min_evaluate_nodes=min_clients,
            min_available_nodes=min_clients,
        )
    if ServerConfig is not None and ServerAppComponents is not None:
        config = ServerConfig(num_rounds=num_rounds)
        return ServerAppComponents(strategy=strategy, config=config)
    return strategy


app = ServerApp(server_fn=server_fn)
