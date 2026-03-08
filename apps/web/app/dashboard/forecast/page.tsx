"use client";

import { useEffect, useState } from "react";
import { apiGet, CongestionForecast } from "@/lib/api";
import { StatusChip } from "@/components/ui/StatusChip";

export default function ForecastPage() {
  const [data, setData] = useState<CongestionForecast | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiGet<CongestionForecast>("/api/v1/forecast/congestion?horizon_minutes=120")
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
        Loading forecast...
      </div>
    );
  }

  const segments = (data.segments ?? []).slice(0, 25);

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Congestion forecast
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        Short-horizon congestion or speed forecast per segment. Baseline heuristic; ST-GNN planned.
      </p>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        {data.data_status && <StatusChip status={data.data_status} />}
        <span className="text-sm text-text-muted">Horizon: {data.horizon_minutes} min</span>
        <span className="text-sm text-text-muted">Model: {data.model_version ?? "n/a"}</span>
        {data.note && <span className="text-sm text-text-muted">{data.note}</span>}
      </div>

      <div className="mt-8 rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden">
        <div className="border-b border-surface-border px-4 py-3">
          <h2 className="font-medium text-text-primary">Segments (first 25)</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-surface-border text-left text-text-muted">
                <th className="p-3 font-medium">Segment</th>
                <th className="p-3 font-medium">Timestamp</th>
                <th className="p-3 font-medium">Speed (km/h)</th>
                <th className="p-3 font-medium">Congestion</th>
              </tr>
            </thead>
            <tbody>
              {segments.map((s, i) => (
                <tr key={i} className="border-b border-surface-border/50 text-text-secondary">
                  <td className="p-3 font-mono">{s.segment_id}</td>
                  <td className="p-3">{s.timestamp}</td>
                  <td className="p-3">{s.speed_kmh ?? ""}</td>
                  <td className="p-3">
                    {s.congestion_score != null ? `${(s.congestion_score * 100).toFixed(1)}%` : ""}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
