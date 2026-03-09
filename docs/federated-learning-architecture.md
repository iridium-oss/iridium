# Federated Learning Architecture

This document describes the IRIDIUM federated learning architecture: components, data flow, and how FL connects to the forecasting stack. It matches the implementation in `services/forecasting/federated`.

## Overview

Federated learning allows training a congestion forecasting model across multiple data-holding nodes without centralizing raw data. Each node (client) holds a partition; clients receive the global model, train locally, and send updates to the server. The server aggregates updates (e.g. FedAvg) and produces a new global model.

## Components

| Component | Role |
|-----------|------|
| ServerApp | Flower server: initializes strategy (FedAvg), runs rounds, aggregates updates. |
| ClientApp | Flower client: loads partition data, runs local training, returns parameters and metrics. |
| Model | Shared linear regression (NumPy): same architecture on all clients and server. |
| Partitioning | Generates partition manifests and data (by district, provider, source family, time, or synthetic). |
| Task | Model creation and initial parameters; used by server and clients. |

## Data Flow

1. Partitions are generated or provided per node (no raw central merge). Each partition has a manifest (partition_id, sample_count, strategy, coverage, geography, etc.) and optional data files (x, y).
2. Server starts with initial_arrays (from task.get_initial_parameters()). Strategy runs num_rounds.
3. Each round: server sends current global parameters and config to selected clients. Clients load local partition only, fit model, return updated parameters and metrics. Server aggregates (e.g. weighted average by num_examples) and updates global model.
4. No raw data leaves clients; only model parameters and scalars (loss, MAE, num_samples) are sent.

## Integration with Forecasting Stack

- The **production forecast API** uses the heuristic baseline in `forecasting/pipeline.py`. It does not load a federated model unless explicitly wired.
- The **federated model** (linear regression) is a separate artifact produced by FL runs. To use it for inference, a separate integration step would load the checkpoint and expose it; that is not the default.
- Feature dimension and schema are aligned (e.g. input_dim=8) so that when real feature pipelines exist, they can feed the same model interface.

## Strategy and Config

- FedAvg is the baseline. Config: num_rounds, min_available_clients, local_epochs, batch_size, learning_rate (via run_config or pyproject).
- Optional strategies (FedProx, FedAdam) can be added and selected via config; they are not default.

## Security and Privacy

- **Plain FL**: Default. No secure aggregation; server sees client updates.
- **Secure aggregation**: Optional; not enabled by default. Document when enabled.
- **Differential privacy**: Optional; not enabled by default. Document when enabled and that DP does not imply automatic regulatory compliance.

See [federated-learning-privacy.md](federated-learning-privacy.md) and [federated-learning-limitations.md](federated-learning-limitations.md).

## Deployment Modes

- **Simulation**: `flwr run` or `run_simulation()` with virtual nodes; partition data on disk. Implemented.
- **Institution lab**: Same ServerApp/ClientApp; each institution runs a client with its own partition. Topology and transport are deployment responsibilities.
- **Production federation**: Future; not claimed.

All modes are documented; only simulation is runnable out of the box with the repo.
