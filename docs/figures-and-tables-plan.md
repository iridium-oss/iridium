# Figures and Tables Plan

Planning document for figures and tables that may appear in a future preprint or paper. No paper title or identifier is assumed.

## Figure Ideas

| Figure | Description | Source / script |
|--------|-------------|----------------|
| System architecture | High-level components: ingestion, digital twin, forecast, routing, equity, anomaly. | docs/architecture.md; draw.io or similar. |
| Data flow | Sources to twin to services. | Based on docs/system-overview.md and data-sources. |
| Federated learning round | Local training, aggregation, distribution. | Based on docs/federated-learning.md. |
| Forecasting pipeline | Graph, features, model, output. | Based on docs/modeling.md. |
| Routing objective | Multi-objective or weighted utility. | Based on docs/routing.md. |
| Equity score construction | District indicators and composite. | Based on docs/fairness.md. |

## Table Ideas

| Table | Description | Source |
|-------|-------------|--------|
| Provider matrix | Data sources, access type, status. | docs/provider-matrix.md. |
| Evaluation metrics | MAE, RMSE, MAPE, etc. | research/evaluation-plan.md. |
| Experimental setup | Datasets, splits, hyperparameters. | To be filled when experiments exist. |
| Symbol glossary | Notation used in formulas. | docs/symbol-glossary.md. |

## Status

These are planning placeholders. Final figure and table numbers, captions, and content will be determined when the preprint is written. The repository keeps notation consistent (docs/math-style-guide.md, docs/symbol-glossary.md) so that the paper and docs align.
