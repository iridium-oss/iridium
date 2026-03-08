# Presenter Flow

Suggested narrative for a live demo. Keep tone formal and honest about data status.

## Opening

- "IRIDIUM is a real-time urban mobility prediction and optimization platform for Azerbaijani cities. It uses a digital twin of the transport network, real data sources when configured, and four modules: forecasting, multimodal routing, Mobility Equity Score, and anomaly detection."
- "This demo runs in public-only mode: we use Open-Meteo for weather and, if loaded, OSM for the network. Traffic and transit require credentials or operator agreements and are not configured here; the UI shows that explicitly."

## When a panel shows unavailable or configuration required

- "This panel shows [unavailable / configuration required] because [traffic / transit / equity data] is not configured for this run. In a production or pilot deployment, you would set the required credentials or data paths; the platform does not substitute synthetic data."
- Point to docs/real-data-mode.md and docs/operator-integration-requirements.md for what is needed to enable each source.

## When the network graph is empty

- "The network graph is loaded from OpenStreetMap via our fetch and network-import pipeline. For this demo we have not run the import; you can run make fetch-real-data and then network-import to populate it. The digital twin then merges this with weather and optional traffic."

## Closing

- "All data shown is either live from configured sources or explicitly marked as unavailable. The project is open source under EUPL-1.2; documentation and citation details are in the repository."
