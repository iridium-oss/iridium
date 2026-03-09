# Federated Learning Operations

Run commands, artifact locations, and observability for the IRIDIUM federated learning subsystem.

## Run Commands

### Generate partitions only

From `services/forecasting/federated`:

```
python -c "
from pathlib import Path
from federated.partitioning import PartitionStrategy, generate_partitions
from federated.task import get_model_input_dim
d = Path('artifacts/partitions')
d.mkdir(parents=True, exist_ok=True)
generate_partitions(PartitionStrategy.BY_DISTRICT, num_partitions=3, samples_per_partition=100, feature_dim=get_model_input_dim(), seed=42, output_dir=d)
print('Partitions in artifacts/partitions')
"
```

### Run simulation (with Flower installed)

From `services/forecasting/federated`:

```
pip install "flwr[simulation]"
python scripts/run_simulation.py
```

Or, if using Flower CLI and pyproject components:

```
flwr run .
```

### Environment

- `IRIDIUM_FL_data_dir`: Directory containing partition manifests and data (e.g. `artifacts/partitions`). If unset, clients run with no local data and return insufficient_data.
- `IRIDIUM_FL_artifacts_dir`: Where to save checkpoints and metrics (default `artifacts`).

## Artifact Locations

- Partitions: `services/forecasting/federated/artifacts/partitions/` (or as configured). Each partition: `{partition_id}_manifest.json`, `{partition_id}_data.npz`.
- Run outputs: In artifacts_dir; structure is deployment-specific. No run metadata is stored in the API by default.

## Observability

- Flower logs round progress when run. No built-in integration with IRIDIUM observability yet; use structured logs and saved run metadata for round-level and client participation.
- Round-level metadata (loss, MAE, num_samples per client) is returned by the strategy; persist it in your run summary if needed.

## Failure Handling

- **Insufficient client data**: Client returns num_samples=0 and insufficient_data in metrics; server aggregation still runs with remaining clients.
- **Client dropout**: Strategy min_available_clients enforces minimum; round may fail if too few clients respond.
- **Missing partition files**: Client loads no data and reports insufficient_data; do not substitute synthetic data in production paths.

## What Is Not Done

- No automatic run enumeration in the API (runs list is empty unless wired to artifact store).
- No production inference path using a federated checkpoint; forecast API uses heuristic only unless explicitly integrated.
