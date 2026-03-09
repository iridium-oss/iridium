# Federated Learning Deployment

Deployment modes, topology, and what is runnable now vs future.

## Modes

| Mode | Description | Runnable now |
|------|-------------|--------------|
| Simulation | Local Flower simulation; virtual nodes; partition data on disk. | Yes. Use `scripts/run_simulation.py` or `flwr run`. |
| Institution lab | Same code; real nodes; each node has its own partition and runs a client. | Design supported; topology and launch are deployment-specific. |
| Staging | Pre-production federation with TLS and optional secure aggregation. | Future; document assumptions. |
| Production federation | Multi-institution FL with SLAs and operational support. | Future; not claimed. |

## Simulation

- Install: `pip install "flwr[simulation]"`. From `services/forecasting/federated`, run `python scripts/run_simulation.py` or `flwr run .`.
- Partitions must be generated or provided; set data_dir so clients load partition data.
- No real network between nodes; all in one process or Ray backend.

## Institution Lab

- Each institution runs a Flower client with its partition. Server runs separately. Network and identity are deployment responsibilities.
- Use the same ClientApp and ServerApp; configure server address and TLS per Flower docs.
- Node configuration templates and secure transport assumptions should be documented per deployment.

## Environment Validation

- Check that data_dir exists and contains expected partition manifests and data when clients need local data.
- Check that required config (num_rounds, min_available_clients, etc.) is set (via run_config or env).

## What Is Currently Runnable

- Full FL simulation with generated (synthetic) partitions and FedAvg. Linear model; congestion forecasting family.
- API endpoints for status, capabilities, runs, models, privacy-status (no fabricated run data).

## What Is Future

- Production inference using a federated checkpoint.
- Secure aggregation and DP enabled by default or in production.
- Automatic run listing and model registry in the API.
