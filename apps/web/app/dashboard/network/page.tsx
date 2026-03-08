"use client";

import { useEffect, useState } from "react";
import { apiGet, NetworkGraph } from "@/lib/api";
import { StatusChip } from "@/components/ui/StatusChip";

export default function NetworkPage() {
  const [data, setData] = useState<NetworkGraph | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiGet<NetworkGraph>("/api/v1/network/graph")
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
        Loading network snapshot...
      </div>
    );
  }

  const nodes = data.nodes ?? [];
  const edges = data.edges ?? [];

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Network and digital twin
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        Graph snapshot from real sources. No synthetic graph when network is not loaded.
      </p>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        {data.data_status && <StatusChip status={data.data_status} />}
        <span className="text-sm text-text-muted">Version: {data.version ?? "n/a"}</span>
        <span className="text-sm text-text-muted">Snapshot at: {data.snapshot_at ?? "n/a"}</span>
      </div>

      {data.source_provenance && data.source_provenance.length > 0 && (
        <div className="mt-4 rounded-lg border border-surface-border bg-surface-card/60 p-4">
          <h3 className="text-sm font-medium text-text-primary">Source provenance</h3>
          <ul className="mt-2 space-y-1 text-sm text-text-secondary">
            {data.source_provenance.map((p, i) => (
              <li key={i}>
                {p.source_name}: {p.status} {p.fetched_at && `(${new Date(p.fetched_at).toISOString()})`}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-8 rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden">
        <div className="border-b border-surface-border px-4 py-3">
          <h2 className="font-medium text-text-primary">Nodes ({nodes.length})</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-surface-border text-left text-text-muted">
                <th className="p-3 font-medium">ID</th>
                <th className="p-3 font-medium">Type</th>
                <th className="p-3 font-medium">Mode</th>
                <th className="p-3 font-medium">Lat</th>
                <th className="p-3 font-medium">Lon</th>
              </tr>
            </thead>
            <tbody>
              {nodes.slice(0, 50).map((n) => (
                <tr key={n.node_id} className="border-b border-surface-border/50 text-text-secondary">
                  <td className="p-3 font-mono">{n.node_id}</td>
                  <td className="p-3">{n.node_type ?? ""}</td>
                  <td className="p-3">{n.mode ?? ""}</td>
                  <td className="p-3">{n.lat ?? ""}</td>
                  <td className="p-3">{n.lon ?? ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {nodes.length > 50 && (
          <p className="border-t border-surface-border px-4 py-2 text-xs text-text-muted">
            Showing first 50 of {nodes.length} nodes.
          </p>
        )}
      </div>

      <div className="mt-8 rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden">
        <div className="border-b border-surface-border px-4 py-3">
          <h2 className="font-medium text-text-primary">Edges ({edges.length})</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-surface-border text-left text-text-muted">
                <th className="p-3 font-medium">ID</th>
                <th className="p-3 font-medium">From</th>
                <th className="p-3 font-medium">To</th>
                <th className="p-3 font-medium">Mode</th>
                <th className="p-3 font-medium">Time (min)</th>
                <th className="p-3 font-medium">Cost</th>
                <th className="p-3 font-medium">Incident</th>
              </tr>
            </thead>
            <tbody>
              {edges.slice(0, 50).map((e) => (
                <tr key={e.edge_id} className="border-b border-surface-border/50 text-text-secondary">
                  <td className="p-3 font-mono">{e.edge_id}</td>
                  <td className="p-3 font-mono">{e.from_node}</td>
                  <td className="p-3 font-mono">{e.to_node}</td>
                  <td className="p-3">{e.mode}</td>
                  <td className="p-3">{e.travel_time_min ?? ""}</td>
                  <td className="p-3">{e.cost ?? ""}</td>
                  <td className="p-3">{e.incident ? "Yes" : "No"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {edges.length > 50 && (
          <p className="border-t border-surface-border px-4 py-2 text-xs text-text-muted">
            Showing first 50 of {edges.length} edges.
          </p>
        )}
      </div>
    </div>
  );
}
