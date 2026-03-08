# Anomaly Detection Service

Rule-based baseline for detecting incidents, closures, and demand surge proxies. Consumes digital twin state and returns anomaly objects with type, severity, affected area, and optional recommended response. Future evolution toward hybrid or ML-based detection.

## Implemented

- get_anomalies(segment_ids, since) returns list of AnomalyEvent.
- Rules: incident flag on edge; high occupancy (>85%) as demand_surge proxy.
- Timestamp and validity window; recommended_response placeholder.

## Future

- Statistical deviation from forecast; event-calendar-driven surge detection.
- Lower latency and fewer false positives via tuned thresholds or learned detector.
