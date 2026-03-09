# Federated Learning Limitations

Honest limitations of the IRIDIUM federated learning subsystem. No overclaiming.

## Implementation

- **Model**: Linear regression only in FL. No ST-GNN or deep model in federated path.
- **Production inference**: The forecast API does not use a federated model unless explicitly wired. Default is heuristic baseline.
- **Secure aggregation**: Not enabled by default. When enabled, document it.
- **Differential privacy**: Not enabled by default. When used, document parameters and that DP does not imply regulatory compliance.

## Data and Experiments

- **Simulation data**: Partition data used in repo examples is synthetic and marked in manifest metadata. Real data must be provided by deployers.
- **No invented results**: Evaluation and comparison to centralized baseline are reported only when actually run. Do not fabricate metrics or run summaries.

## Deployment

- **Production federation**: Not claimed. Only simulation and institution-lab design are supported. Multi-institution production FL is future work.
- **Legal**: The design supports privacy-aware deployment but does not guarantee GDPR or other compliance. Deployers conduct their own assessment.

## Non-IID and Heterogeneity

- Non-IID data across clients can hurt global model quality. FedAvg is not optimized for high heterogeneity; FedProx or personalization may be added later. Document when used.

## Operational

- Run metadata and model artifacts are not automatically exposed in the API. Integrate with artifact store and run registry if needed.
- Client dropout and failures are logged; strategy enforces min_available_clients. No silent substitution of fake clients.
