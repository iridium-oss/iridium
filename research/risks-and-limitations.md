# Risks and Limitations

This document records known risks and limitations of the IRIDIUM project. It is intended for transparency and for use in evaluation and policy discussion. It will be updated as new risks are identified or mitigated.

## Data and Coverage

- **Spatial and temporal coverage**: Prediction and equity metrics are only as good as the data that feeds the digital twin. Under-covered areas (e.g. informal settlements, peripheral districts) may be misrepresented or absent. Indicators that depend on such data will carry bias.
- **Data quality**: Noisy, stale, or incorrect data will affect forecasting, routing, and anomaly detection. Quality checks and gap handling are part of the design but cannot eliminate risk.
- **Non-IID data in federated learning**: If participants have very different data distributions, the global model may perform poorly for some. Personalisation or weighted aggregation may be needed; not guaranteed in the initial release.

## Privacy and Security

- **No legal guarantee**: The federated design is intended to support privacy-preserving and regulation-aware deployment. It does not by itself ensure compliance with GDPR, local data protection law, or sector-specific rules. Deployers must conduct their own compliance assessment.
- **Inference and model inversion**: Trained models can sometimes leak information about training data. Differential privacy or other formal guarantees will be documented where applied; default settings may not meet strict privacy requirements.
- **Operational security**: Deployment security (secrets, network, access control) is the responsibility of the deployer. The project provides documentation and best practices but cannot guarantee a specific security posture.

## Fairness and Equity

- **Indicator bias**: The Mobility Equity Score depends on chosen indicators and weights. Choices can favour or disadvantage certain areas or groups. Documentation and configurability are intended to make this transparent; the project does not define a single "fair" outcome.
- **Representation gaps**: District-level aggregation can hide within-district inequality. Subgroup analysis (e.g. by demographic) is not in the initial scope and may require additional data and methodology.

## Operational

- **Anomaly detection**: False positives and false negatives are possible. Detection latency means that users may still be directed into affected areas briefly. The system is best-effort; critical safety decisions must not rely solely on it. See [docs/anomaly-detection.md](../docs/anomaly-detection.md).
- **Routing**: Route quality depends on twin accuracy and freshness. Stale or incomplete data will produce suboptimal or incorrect routes. Fare and carbon estimates are simplifications.

## Technical and Research

- **Reproducibility**: Full reproducibility requires access to the same data (or synthetic data), code version, and environment. The project aims to document these; some data may remain restricted.
- **Generalisation**: Methods and models are developed with Azerbaijani cities in mind. Generalisation to other cities or countries may require adaptation of graph construction, data sources, and hyperparameters.

## Risk and limitations table

| Risk | Cause | Operational effect | Mitigation |
|------|--------|--------------------|------------|
| Spatial/temporal coverage bias | Under-covered areas | Misrepresentation or absence in twin and equity | Document gaps; report data_status; do not fabricate. |
| Data quality | Noisy or stale data | Poor forecasts and routing | Quality checks; stale thresholds; explicit status. |
| Non-IID in federated | Different participant distributions | Global model underperforms for some | Personalisation or weighted aggregation; document. |
| No legal guarantee | Design supports but does not ensure compliance | Deployer liability | Deployer compliance assessment; document assumptions. |
| Anomaly false positives/negatives | Detection limits | Unnecessary reroutes or missed incidents | Tuning; operational caveats; do not rely for safety-critical decisions. |
| Routing quality | Stale or incomplete twin | Suboptimal or incorrect routes | Document dependency; freshness and provenance in API. |

## Updates

New risks or limitations identified during development, evaluation, or deployment will be added to this document. Mitigations, when adopted, will be described here or in the relevant technical docs.
