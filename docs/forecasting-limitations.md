# Forecasting Limitations

## Current Data Coverage

- Forecasts depend on **real** digital twin data. When the network is not loaded (no PostGIS or network-import), only the default heuristic segment is returned with limited geographic meaning.
- **Learned models** (Graph WaveNet, DCRNN) require a sufficient history of time-aligned snapshots for training and, at inference time, a recent input window. The current pipeline does not persist a long history of snapshots; once a history store is available, the inference path can be wired to use the learned model when an artifact and recent data exist.
- Weather, transit, and alerts are integrated only where actually available; missing sources do not get synthetic substitutes.

## Model and Evaluation

- No fabricated data, training results, or evaluation metrics. If the model cannot run honestly (e.g. insufficient data), the system returns an explicit unavailable or degraded status.
- MAPE is reported only when denominators are safe (no zero or near-zero targets in the denominator set).
- Federated learning in `federated/` is experimental and not in the default runtime path.

## Operational

- Deterministic baseline is suitable for operational awareness but has no calibrated uncertainty. Learned model outputs also do not yet provide calibrated confidence intervals; the API exposes a reliability_note/confidence_note to that effect.
