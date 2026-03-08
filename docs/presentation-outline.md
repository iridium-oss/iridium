# Presentation Outline

Suggested structure for a short hackathon or reviewer presentation of IRIDIUM. Adjust timing to slot.

## Opening (30-60 seconds)

- One sentence: IRIDIUM is a real-time urban mobility prediction and optimization platform for Azerbaijani cities, built around federated learning and a digital twin.
- Why it matters: Congestion and inequity; need to combine data without centralising it; privacy by design.

## Architecture (45-60 seconds)

- Federated learning: data stays local; only model updates are shared.
- Digital twin: graph of the network and its state; fed by sensors, weather, events.
- Four modules: forecasting, multimodal routing, Mobility Equity Score, anomaly detection.
- Current state: runnable baseline with real or recorded data when configured; federated and ST-GNN planned.

## Demo (2-3 minutes)

- Follow docs/demo-scenario.md: Overview, Network, Forecast, Routing, Equity, Anomalies, Methodology.
- Emphasise: real-data mode when configured; explicit data_status when not; baseline implementation; extension points clear.
- If live demo fails: use OpenAPI (/docs) or prepared screenshots.

## Technical and Research Credibility (30-45 seconds)

- Schemas and API are documented; research folder has problem statement, methodology, evaluation plan, risks.
- No false claims: no production deployment, no compliance certification.
- Repository is structured for continued development and open source contribution.

## Closing (15-30 seconds)

- Invite judges to clone, run, and read docs/reviewer-guide.md and docs/product-scope.md.
- Thank the track and mentors.

## Backup slides or notes

- Link to repo, docs, and key files (README, architecture, api-spec, reviewer-guide).
- One-line reminder: "Baseline implementation; synthetic data; privacy-by-design architecture."
