# IRIDIUM Forecasting Engine: Implementation Report

## Summary

The core model layer of IRIDIUM has been implemented as a production-minded forecasting engine with Graph WaveNet as the primary model, DCRNN as a benchmark baseline, and simple statistical baselines. All outputs are traceable to real data and artifacts; no fake predictions or fabricated metrics.

## Completed Components

- **Graph WaveNet integration**: Repository-native PyTorch implementation in `forecasting/models/graph_wavenet/`. Adaptive adjacency and gated temporal convolution; config-driven (configs/graph_wavenet.yaml). Integrated with dataset and feature schemas.

- **DCRNN baseline**: Implemented in `forecasting/models/dcrnn/`. Same I/O contract as Graph WaveNet; used for comparison and robustness checks.

- **Simple baselines**: Persistence, rolling mean, and linear temporal regression in `forecasting/baselines/`. First-class in evaluation and sanity checking.

- **Dataset builder**: Real data only; time-aligned from digital twin snapshots. Manifests record source coverage, time span, geography, missingness, label/feature availability, freshness. No synthetic data in the production path. Explicit downgrade when labels are insufficient (training returns insufficient_data status).

- **Graph construction**: `forecasting/graph/`: build from network nodes/edges; normalized support matrix; reproducible and versioned metadata.

- **Training pipeline**: Config-driven runner; train/val/test temporal split; checkpoints and training_metadata.json; early stopping; seed handling; graceful failure when data is insufficient.

- **Evaluation pipeline**: MAE, RMSE, MAPE (when safe); per-horizon and aggregate; comparison between Graph WaveNet, DCRNN, and simple baselines; no invented benchmarks.

- **Inference and registry**: Production-safe inference wrapper; returns model/dataset/feature version, coverage note, degraded flag; never returns learned forecast when artifact is missing. Registry metadata and validation before load; maturity states (deterministic_baseline, statistical_baseline, ml_baseline, candidate, inactive).

- **API integration**: GET /api/v1/forecast/status, /forecast/models, /forecast/coverage, /forecast/features, /forecast/congestion. Responses distinguish learned model, statistical baseline, deterministic fallback, and unavailable.

- **Documentation**: forecasting-architecture.md, forecasting-models.md, forecasting-data-pipeline.md, forecasting-evaluation.md, forecasting-serving.md, forecasting-limitations.md. Production path, data requirements, degraded mode, and active vs experimental are documented.

- **Tests**: Task spec, graph construction, dataset/sources, baselines, Graph WaveNet and DCRNN forward passes, inference wrapper (no artifact), registry validation. Located under services/forecasting/tests/.

## Limitations (Current Data Coverage)

- **History store**: The congestion forecast API currently uses only the deterministic heuristic. To serve Graph WaveNet, the system needs a stored history of snapshots (or live buffer) to form the input window; the inference wrapper is ready but not wired to the pipeline until history is available.

- **Training data**: Training runs only when sufficient timesteps exist (input_window + horizon + buffer). With empty or small twin snapshots, training correctly returns insufficient_data.

- **Weather/transit**: Feature pipeline and docs allow for weather and transit; integration uses only real sources where actually available in the repo.

- **Federated learning**: The federated package remains experimental and not in the default runtime path; the model and trainer are structured so that a Flower-based federated path can be added later without changing the core interfaces.

## Audit and Cleanup

- Audit document: docs/forecasting-model-audit.md. Existing pipeline classified as production-usable (deterministic baseline); no fake or misleading code in the active path.
- Weak placeholders were not added; the production path uses either the heuristic or the inference wrapper when artifact and data are available. No duplicate model wrappers or inconsistent formulas in the added code.

## Future Federated Readiness

- Model definition and trainer are modular; dataset partitioning boundaries can be isolated; centralized and federated training interfaces are compatible. Extension point for Flower-based training is preserved; federated training is not activated in the default runtime.
