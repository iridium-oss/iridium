# IRIDIUM Federated Learning Subsystem

Federated learning layer for IRIDIUM using Flower. Scope: congestion forecasting model family. FedAvg baseline; simulation and institution-lab modes.

## Scope

- **Model family**: Congestion forecasting (linear regression baseline in FL).
- **Deployment**: Simulation (local virtual nodes); institution-lab (real nodes, same code). Production federation is future work.
- **Partitioning**: By district, by provider, by source family, by time block, or synthetic institution (simulation only).

See [docs/federated-learning-scope.md](../../../docs/federated-learning-scope.md) and [docs/federated-learning-architecture.md](../../../docs/federated-learning-architecture.md).

## Requirements

- Python >= 3.12
- `pip install "flwr[simulation]"` (from repo root or this directory)

## Structure

- `federated/`: ClientApp, ServerApp, model, task, partitioning, datasets, config.
- `scripts/run_simulation.py`: Generate partitions and run Flower simulation.
- `configs/`: Strategy and run configs (optional).
- `artifacts/`: Generated partitions and run outputs (gitignored).

## Run Simulation

1. From repo root, add federated to path and install deps:
   ```
   pip install "flwr[simulation]" numpy pydantic pydantic-settings
   cd services/forecasting/federated && pip install -e .
   ```

2. Generate partitions and run:
   ```
   python scripts/run_simulation.py
   ```
   Partitions are written to `artifacts/partitions/`. Set `IRIDIUM_FL_data_dir` to that path so clients load data (or pass run_config if your Flower version supports it).

3. Or use Flower CLI from this directory (if pyproject [tool.flwr.app.components] is set):
   ```
   flwr run .
   ```

## API

The main IRIDIUM API exposes:

- `GET /api/v1/federated/status`: Active flag, model family, deployment mode, maturity.
- `GET /api/v1/federated/capabilities`: Plain FL, secure aggregation, DP, partitioning, strategies.
- `GET /api/v1/federated/runs`, `GET /api/v1/federated/runs/{id}`, `GET /api/v1/federated/models`, `GET /api/v1/federated/privacy-status`.

No fabricated run results or performance claims.

## Tests

```
cd services/forecasting/federated && python -m pytest tests/ -v
```

## Limitations

- FL is not used for production inference. Forecast API uses heuristic baseline only.
- Secure aggregation and differential privacy are not enabled by default; document when enabled.
- Partition data for simulation is synthetic and marked in manifest metadata.
