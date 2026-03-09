# Modeling

This document describes candidate modeling directions for the IRIDIUM forecasting engine: spatio-temporal graph neural networks (ST-GNN) for congestion prediction, temporal feature engineering, graph construction, evaluation metrics, and model lifecycle concerns.

## ST-GNN for Congestion Prediction

The primary forecasting target is short-horizon (2 to 3 hour) congestion or traffic state. Spatio-temporal graph neural networks are a natural fit: the digital twin provides the graph (road network), and traffic state is both spatial (across segments) and temporal (over time).

**Candidate approaches**:

- Graph Convolutional Networks (GCN) or Graph Attention Networks (GAT) over the road graph, with temporal convolutions or recurrent layers (e.g. TGCN, ASTGCN, or similar).
- Message passing over the twin graph so that each node aggregates information from neighbours and from history.
- Optional: integration of external features (weather, events) via additional input channels or conditioning.

Specific architectures will be documented in the codebase and in research docs as they are implemented. Baseline models (e.g. persistence, simple averaging) will be used for comparison.

## Temporal Feature Engineering

- **Lag features**: Past speeds, occupancy, or flow at multiple lags (e.g. 15 min, 1 h, 2 h).
- **Time-of-day and day-of-week**: Cyclical or categorical encoding for periodicity.
- **Holidays and events**: Binary or categorical indicators from the event calendar.
- **Weather**: Precipitation, temperature, etc., where available.

Feature pipelines must be reproducible and versioned; shared schemas live in `packages/schemas` where they affect APIs or storage.

## Spatio-Temporal Formulation

Let $G = (V, E, W)$ denote the mobility graph. At time $t$, node features are $X_t \in \mathbb{R}^{|V| \times F}$ with $F$ features per node. The forecast for horizon $H$ is $\hat{Y}_{t+1:t+H} = f_{\theta}(X_{t-T+1:t}, G)$ where $T$ is the input window length. A typical loss is MAE: $\mathcal{L}_{\mathrm{MAE}} = \frac{1}{N H} \sum_{i=1}^{N} \sum_{h=1}^{H} | y_{i,t+h} - \hat{y}_{i,t+h} |$ over $N$ entities and $H$ steps. Evaluation may also use RMSE and MAPE; see [research/evaluation-plan.md](../research/evaluation-plan.md).

## Graph Construction Assumptions

- **Nodes**: Typically road segments or junctions; may include transit stops for multimodal use. Segment granularity affects resolution and compute cost.
- **Edges**: Connectivity (adjacency) and optionally edge attributes (length, free-flow time). Directed edges where one-way or asymmetric flow matters.
- **Weights**: Edge weights may be fixed (e.g. inverse distance) or dynamic (current travel time from the twin). Assumptions (e.g. how often weights are updated) affect model behaviour.

Graph construction choices can introduce bias (e.g. under-representing informal or pedestrian links). These are documented in [fairness.md](fairness.md) and in the research risks.

## Evaluation Metrics

- **Forecasting**: Mean Absolute Error (MAE), Root Mean Square Error (RMSE), Mean Absolute Percentage Error (MAPE) for speed or occupancy; or classification metrics for congestion levels if the target is discrete. Metrics will be defined per target variable and horizon in the evaluation plan.
- **Temporal and spatial disaggregation**: Metrics may be reported by time-of-day and by region to detect uneven performance.
- **Baselines**: Persistence, historical average, or simple propagation models. Results must be comparable across the same train/test split and preprocessing.

See [research/evaluation-plan.md](../research/evaluation-plan.md) for a fuller evaluation plan.

## Model Lifecycle

- **Training**: Federated training produces a global model; see [federated-learning.md](federated-learning.md). Local retraining or fine-tuning may be supported in future.
- **Versioning**: Model checkpoints and configs are versioned. Reproducibility requires storing code, data references (or synthetic data), and hyperparameters.
- **Deployment**: The trained model is loaded by the inference service. Version rollout and rollback are deployment responsibilities.
- **Monitoring**: Predictions should be logged (without personal data) and compared to realised values where possible to detect drift or degradation.
