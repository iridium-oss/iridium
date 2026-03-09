"use client";

import { useState } from "react";
import { apiPost, RouteResponse } from "@/lib/api";
import { Icon } from "@/components/ui/Icon";

export default function RoutingPage() {
  const [originLat, setOriginLat] = useState("40.4093");
  const [originLon, setOriginLon] = useState("49.8671");
  const [destLat, setDestLat] = useState("40.413");
  const [destLon, setDestLon] = useState("49.871");
  const [optimize, setOptimize] = useState("time");
  const [result, setResult] = useState<RouteResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = () => {
    setLoading(true);
    setError(null);
    apiPost<RouteResponse, { origin_lat: number; origin_lon: number; destination_lat: number; destination_lon: number; optimize: string }>(
      "/api/v1/routing/plan",
      {
        origin_lat: parseFloat(originLat),
        origin_lon: parseFloat(originLon),
        destination_lat: parseFloat(destLat),
        destination_lon: parseFloat(destLon),
        optimize,
      }
    )
      .then(setResult)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Multimodal route planning
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        Origin and destination (lat, lon). Routing uses real network when loaded; response includes data status.
      </p>

      <div className="mt-8 rounded-xl border border-surface-border bg-surface-card/80 p-6">
        <h2 className="font-medium text-text-primary">Plan route</h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-text-muted">Origin lat</span>
            <input
              type="text"
              value={originLat}
              onChange={(e) => setOriginLat(e.target.value)}
              className="rounded-lg border border-surface-border bg-midnight-prussian px-3 py-2 text-text-primary focus:border-accent-focus focus:outline-none focus:ring-1 focus:ring-accent-focus"
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-text-muted">Origin lon</span>
            <input
              type="text"
              value={originLon}
              onChange={(e) => setOriginLon(e.target.value)}
              className="rounded-lg border border-surface-border bg-midnight-prussian px-3 py-2 text-text-primary focus:border-accent-focus focus:outline-none focus:ring-1 focus:ring-accent-focus"
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-text-muted">Dest lat</span>
            <input
              type="text"
              value={destLat}
              onChange={(e) => setDestLat(e.target.value)}
              className="rounded-lg border border-surface-border bg-midnight-prussian px-3 py-2 text-text-primary focus:border-accent-focus focus:outline-none focus:ring-1 focus:ring-accent-focus"
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-text-muted">Dest lon</span>
            <input
              type="text"
              value={destLon}
              onChange={(e) => setDestLon(e.target.value)}
              className="rounded-lg border border-surface-border bg-midnight-prussian px-3 py-2 text-text-primary focus:border-accent-focus focus:outline-none focus:ring-1 focus:ring-accent-focus"
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-text-muted">Optimize</span>
            <select
              value={optimize}
              onChange={(e) => setOptimize(e.target.value)}
              className="rounded-lg border border-surface-border bg-midnight-prussian px-3 py-2 text-text-primary focus:border-accent-focus focus:outline-none focus:ring-1 focus:ring-accent-focus"
            >
              <option value="time">Time</option>
              <option value="cost">Cost</option>
              <option value="carbon">Carbon</option>
            </select>
          </label>
        </div>
        <button
          type="button"
          onClick={submit}
          disabled={loading}
          className="mt-4 inline-flex items-center gap-2 rounded-lg bg-midnight-electric px-4 py-2.5 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50"
        >
          {loading ? (
            <>
              <span className="material-symbols-outlined animate-spin text-lg">progress_activity</span>
              Planning...
            </>
          ) : (
            <>
              <Icon name="route" size={20} />
              Plan route
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-8 rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="font-medium text-text-primary">Result</h2>
          {result.note && <p className="mt-2 text-sm text-text-secondary">{result.note}</p>}
          <div className="mt-4 space-y-4">
            {(result.alternatives ?? []).map((alt, i) => (
              <div key={i} className="rounded-lg border border-surface-border bg-white p-4">
                <p className="font-medium text-text-primary">
                  Alternative {i + 1}: {alt.total_duration_min != null ? alt.total_duration_min.toFixed(1) : "—"} min. Cost: {alt.total_cost ?? 0}. Carbon: {alt.total_carbon_kg ?? 0} kg.
                </p>
                <p className="mt-2 text-sm text-text-secondary">
                  Segments: {(alt.segments ?? []).map((s) => `${s.mode ?? ""} ${s.duration_min ?? ""} min`).join(", ")}.
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
