# Models

This directory contains model definitions, training scripts, and federated learning orchestration for the IRIDIUM forecasting engine and any other ML components.

## Purpose

- **Forecasting model**: Spatio-temporal graph neural network (ST-GNN) or equivalent for short-horizon congestion prediction. Architecture and training config are documented in `docs/modeling.md`.
- **Federated orchestration**: Client and server logic for federated learning (local training, update submission, aggregation). Compatible with the architecture described in `docs/federated-learning.md`.
- **Baselines**: Reference implementations of persistence, historical average, or simple propagation for comparison in the evaluation plan.
- **Export and serving**: Export of trained models to a format consumable by the inference service (e.g. ONNX, PyTorch TorchScript, or framework-native checkpoint).

## Technology

PyTorch or TensorFlow for the ST-GNN; federated framework (e.g. Flower, PySyft) for orchestration. Exact choices will be documented here and in the docs. Python is the primary language.

## Structure

Structure will be established as implementation progresses. Expected elements:

- Model architecture definitions (e.g. GCN/GAT + temporal module).
- Training scripts for central and federated settings.
- Config files for hyperparameters and data paths.
- Scripts for evaluation and export.
- No raw or sensitive data in the repository; data paths point to local or configured locations.

## Development

- Training and evaluation should be reproducible: configs and code version are recorded. See `research/evaluation-plan.md` and `research/methodology.md`.
- Model versioning and checkpoint storage are deployment responsibilities; this directory focuses on code and config.

## Testing

Model code may be unit-tested (e.g. forward pass, gradient flow). Integration tests with small synthetic graphs may live in `tests/`. CI runs the test suite as configured in the repository root.
