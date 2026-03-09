# Federated Learning Scope

This document defines exactly what federated learning in IRIDIUM is responsible for, what is federated, what is not, and which deployment modes exist.

## Model Families That Can Be Federated

| Family | Status | Notes |
|--------|--------|-------|
| Congestion forecasting | Implemented (simulation) | Linear regression baseline in FL; heuristic remains production forecast path. |
| Anomaly scoring | Not federated | Rule-based only; no FL path. |
| District-level predictive signals | Experimental | Can be added as partition-by-district targets. |
| Route-demand estimation | Not federated | Not in scope for current FL. |

## What Is Not Federated

- Production inference: forecast, anomaly, equity, and routing APIs use deterministic or rule baselines. No federated model is served in the main API unless explicitly wired and documented.
- Anomaly detection model: no FL training path.
- Equity composite: file-based; no FL.
- Routing: graph and weights; no FL.

## Active vs Experimental Federated Workloads

- **Active (runnable)**: Congestion forecasting FL simulation. Run via `scripts/run_simulation.py` or `flwr run` from `services/forecasting/federated`. Uses partition data (synthetic for simulation, clearly marked).
- **Experimental**: FedProx, FedAdam, secure aggregation, differential privacy. Implemented where present and labeled; not default.

## Deployment Modes

| Mode | Description | Status |
|------|-------------|--------|
| Simulation | Local Flower simulation with virtual nodes; partition data on disk. | Implemented. |
| Institution lab | Same code, real nodes; each node has its own partition. | Supported by design; deployment topology is doc-only. |
| Staging | Pre-production federation with secure transport. | Future; docs only. |
| Production federation | Live multi-institution FL with SLAs. | Future; not claimed. |

## Partitioning Schemes

- By district: partition_id like p_by_district_0.
- By provider: by_provider.
- By source family: by_source_family.
- By time block: by_time_block.
- Synthetic institution: simulation only; marked in manifest metadata.

## Where This Is Reflected in Code

- `federated/__init__.py`: FL_SCOPE_MODEL_FAMILIES, FL_DEPLOYMENT_MODES.
- `federated/partitioning/manifest.py`: PartitionStrategy enum.
- API `/api/v1/federated/status` and `/api/v1/federated/capabilities`: expose scope and maturity.

No federated model is used for production inference unless explicitly integrated and documented.
