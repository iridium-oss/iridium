# Federated Learning Status

This document states the current status of federated learning (FL) in IRIDIUM and how it is presented in the product and API.

## Status: Implemented for Simulation; Not Used for Production Inference

Federated learning is **implemented** in `services/forecasting/federated`: Flower ServerApp and ClientApp, FedAvg strategy, partitioning, and a linear congestion-forecasting model. Simulation is runnable via `scripts/run_simulation.py` or `flwr run`. No FL model is used for **production inference**; the forecast API uses the heuristic baseline only.

## How FL Is Positioned

- **Product and API**: FL is exposed via `/api/v1/federated/status`, `/api/v1/federated/capabilities`, and related endpoints. These report active=false for production inference, model_family=congestion_forecasting, deployment_mode=simulation, maturity=experimental. Forecast, anomaly, equity, and routing use deterministic or rule baselines only.
- **Documentation**: [federated-learning-architecture.md](federated-learning-architecture.md), [federated-learning-operations.md](federated-learning-operations.md), [federated-learning-scope.md](federated-learning-scope.md), and related docs describe the implementation, run commands, and limitations.
- **Code**: FL code in `services/forecasting/federated` is real and runnable. It is not invoked in the main forecast request path unless explicitly wired.

## What Is Active vs Experimental

- **Active (runnable)**: FL simulation with FedAvg, partition generation, and linear model. No secure aggregation or DP by default.
- **Experimental**: Secure aggregation, differential privacy, FedProx/FedAdam; documented and optional.

## Rule

Do not present federated learning as **production inference**. The forecast API does not use a federated model unless explicitly integrated. When referring to FL in pitch or docs, use wording such as "simulation," "institution-lab," or "experimental" as appropriate.
