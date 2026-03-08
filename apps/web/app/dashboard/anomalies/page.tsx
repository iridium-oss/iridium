"use client";

import { useEffect, useState } from "react";
import { apiGet, AnomaliesResponse } from "@/lib/api";
import { Icon } from "@/components/ui/Icon";

export default function AnomaliesPage() {
  const [data, setData] = useState<AnomaliesResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiGet<AnomaliesResponse>("/api/v1/anomalies")
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
        Error: {error}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card/80 px-4 py-6 text-text-secondary">
        <span className="material-symbols-outlined animate-pulse">progress_activity</span>
        Loading anomalies...
      </div>
    );
  }

  const anomalies = data.anomalies ?? [];

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Anomaly monitoring
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        Rule-based detection over speed deviations and provider alerts. Labeled by type, severity, and source.
      </p>

      {anomalies.length === 0 ? (
        <div className="mt-8 rounded-xl border border-surface-border bg-surface-card/80 p-8 text-center text-text-secondary">
          No anomalies in current snapshot. The pipeline operates on real twin state only.
        </div>
      ) : (
        <div className="mt-8 space-y-4">
          {anomalies.map((a, i) => (
            <div
              key={i}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-4"
            >
              <div className="flex items-start gap-3">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-amber-500/20 text-amber-300">
                  <Icon name="warning" size={20} />
                </span>
                <div className="min-w-0 flex-1 text-sm">
                  <p className="font-medium text-text-primary">{a.type ?? "Anomaly"}</p>
                  <p className="mt-1 text-text-secondary">Severity: {a.severity ?? "n/a"}. Confidence: {a.confidence != null ? (a.confidence * 100).toFixed(0) + "%" : "n/a"}.</p>
                  {a.affected_geography && <p className="text-text-muted">Geography: {a.affected_geography}</p>}
                  {a.detected_at && <p className="text-text-muted">Detected: {a.detected_at}</p>}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
