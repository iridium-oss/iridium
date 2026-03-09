# Forecasting Data Pipeline

## Sources

Only **real** data sources integrated or available in the repository are used:

- **Network topology**: Digital twin nodes and edges (from PostGIS/network-import when configured).
- **Edge state**: speed_kmh, occupancy_pct from twin snapshot.
- **Weather / transit / alerts**: Included where genuinely available and time-aligned; no synthetic feeds in the production model path.

## Dataset Builder

`forecasting/data/builder.py` builds time-aligned datasets from a list of digital twin snapshots. It produces:

- A **target matrix** `(T, N)` and a **mask** `(T, N)` for valid observations.
- A **DatasetManifest** with: source_coverage, time_span_start/end, geography, missingness_ratio, label_availability, feature_availability, data_freshness_seconds, num_entities, num_timesteps, dataset_version.

Observations are built per edge from snapshot state; congestion score is derived from speed and occupancy when present. No synthetic fill for missing labels; insufficient labels lead to explicit downgrade of the model path (no fabricated supervision).

## Feature Engineering

`forecasting/features/`: Deterministic pipeline with versioned schema. Features include historical target lags, rolling mean/std, hour and day-of-week encoding. Training and inference use the same transformations. Feature coverage and missingness are recorded.

## Data Requirements

- Minimum timesteps for training: input_window + horizon + buffer (e.g. 10+ steps).
- Minimum coverage ratio (configurable) for serving learned model.
- Graph and entity order must match the dataset (same node/edge IDs and ordering).
