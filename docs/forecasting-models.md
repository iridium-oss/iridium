# Forecasting Models

## Graph WaveNet (Primary)

Repository-native PyTorch implementation in `forecasting/models/graph_wavenet/`. Uses:

- **Gated temporal convolution**: Causal dilated 1D conv with gating for temporal receptive field.
- **Graph convolution**: Spatial mixing with support matrix (normalized adjacency or adaptive).
- **Adaptive adjacency**: Optional learned dependency matrix from node embeddings.
- **Residual and skip connections** across layers.

Input: `(B, T_in, N)`; output: `(B, T_out, N)` where `T_out` is the forecast horizon in steps. Config: input_len, horizon, hidden_dim, num_layers, dropout, use_adaptive_adj (see `configs/graph_wavenet.yaml`).

## DCRNN (Baseline)

Implementation in `forecasting/models/dcrnn/`. Diffusion convolutional GRU cells; same I/O contract as Graph WaveNet. Used for benchmarking and robustness checks, not as the default serving model.

## Simple Baselines

- **Persistence**: Last observed value repeated over the horizon.
- **Rolling mean**: Mean of last W steps repeated.
- **Linear temporal**: Per-entity linear trend on last window, extrapolated.

Implemented in `forecasting/baselines/`. First-class in evaluation and comparison tables.

## Model Registry and Maturity

Artifacts are tagged with maturity: `deterministic_baseline`, `statistical_baseline`, `ml_baseline`, `candidate`, `inactive`. The serving layer does not load artifacts without validation and does not serve `inactive` models.
