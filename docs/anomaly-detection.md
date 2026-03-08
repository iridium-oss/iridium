# Anomaly Detection and Dynamic Rerouting

This document describes real-time anomaly detection and dynamic rerouting in IRIDIUM: types of incidents, the detection pipeline, the response pipeline, and operational caveats.

## Incidents, Closures, and Event Surges

**Incidents**: Accidents, breakdowns, or other sudden events that reduce capacity or block a segment. Detected via sudden drops in speed or flow, or via explicit incident feeds when available.

**Closures**: Planned or unplanned road or segment closures. May be provided by official feeds (e.g. traffic management) or inferred from zero flow or persistent congestion.

**Event surges**: Large public events that cause demand spikes or changed patterns. Inferred from event calendars combined with unusual flow or delay patterns.

Detection may be rule-based (e.g. threshold on speed drop), model-based (e.g. deviation from forecast), or hybrid. The exact methods will be documented with the implementation.

## Deviation and Severity

A rolling baseline (mean $\mu_{t,w}$ and standard deviation $\sigma_{t,w}$ over window $w$) yields a z-score $z_t = (x_t - \mu_{t,w}) / \sigma_{t,w}$. Anomaly severity or score $S_t$ may combine $z_t$ with event and weather components (e.g. $S_t = \lambda_1 z_t + \lambda_2 e_t + \lambda_3 w_t$ with weights $\lambda_i$). Thresholding or classification then labels anomalies by type and location.

## Detection Pipeline

1. **Input**: Real-time or near-real-time data from the digital twin (speeds, flow, occupancy) and from external sources (incident feeds, event calendar).
2. **Signal processing**: Compute derived signals (e.g. change from baseline, deviation from forecast) and apply thresholds or anomaly scores.
3. **Classification**: Label detected anomalies by type (incident, closure, event surge) and location (segment or zone). Optional confidence or severity.
4. **Output**: Anomaly records are written to the digital twin (e.g. incident flags on edges) and may trigger alerts or the response pipeline.

Latency from event occurrence to detection depends on data freshness and pipeline design; targets will be stated in the implementation docs.

## Response Pipeline

1. **Twin update**: Anomalies update the digital twin so that affected segments have modified weights (e.g. very high cost or blocked) or metadata (e.g. incident flag).
2. **Rerouting**: The routing service uses the updated twin. New route requests and, where supported, in-journey recalculations reflect the anomaly. Dynamic rerouting is thus "recompute route with current twin."
3. **Alerts**: Optional push or pull alerts to operators or users. Format and delivery are deployment-specific.

## Operational Caveats

- **False positives**: Over-sensitive detection can cause unnecessary reroutes or alarm. Tuning and validation are required per deployment.
- **False negatives**: Missed incidents mean routes may still use blocked or degraded segments. Detection is best-effort; critical safety decisions must not rely solely on this pipeline.
- **Latency**: There is a delay from real-world event to twin update to reroute. For fast-moving incidents, users may still be directed into affected areas during that window.
- **Coverage**: Detection quality depends on data coverage. Areas with few sensors or no incident feeds will have weaker detection.
- **Event calendar quality**: Event-driven surge detection depends on complete and timely event data; missing or late events limit accuracy.

These caveats should be communicated to operators and, where appropriate, to end users (e.g. in terms of service or app disclaimers).
