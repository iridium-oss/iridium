# Federated Learning Evaluation

How federated runs are evaluated and compared to baselines. No invented results.

## Metrics

- **Training**: Loss (MSE), MAE, num_samples per client per round. Aggregated (e.g. weighted average) at server.
- **Evaluation**: Same metrics on client-side evaluate; optional server-side aggregate evaluation.
- **Convergence**: Round-wise loss and MAE; document number of rounds and client participation.

## Comparison to Centralized Baseline

Where possible, compare federated runs to a centralized baseline trained on the same (or pooled) data under the same model and feature schema. Report:

- Global validation metrics (e.g. MAE, RMSE) for federated vs centralized.
- Per-partition or per-client metrics to assess heterogeneity and fairness.

Do not invent comparison results. If evaluation data is limited, narrow claims and say so explicitly.

## Artifacts and Plots

- Save round-wise metrics (loss, MAE, num_samples) in run artifacts.
- Optional: round-wise loss curves, participation histograms, partition skew summaries. Generate only from real runs.

## Experiment Directory

Structure for real experiments (e.g. under `research/federated-experiments/` or `artifacts/runs/`):

- run_id/
  - config.json
  - partition_manifest_versions
  - round_metrics.json
  - final_checkpoint (optional)
  - summary.md (optional)

Link each run to git commit, dataset version, and partition strategy.

## Client Participation and Failure

- Log client selection and participation per round.
- Log client failures and dropouts. Do not substitute fake participation.
