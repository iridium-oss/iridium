"use client";

import { useEffect, useState } from "react";
import { apiGet, NetworkGraph } from "@/lib/api";
import { StatusChip } from "@/components/ui/StatusChip";

export default function ProvenancePage() {
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
        Loading...
      </div>
    );
  }

  const provenance = data.source_provenance ?? [];

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Data source and provenance
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        Per-source status and provenance from the digital twin snapshot. No synthetic substitution.
      </p>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        {data.data_status && <StatusChip status={data.data_status} />}
      </div>

      <div className="mt-8 space-y-4">
        {provenance.length === 0 ? (
          <div className="rounded-xl border border-surface-border bg-surface-card/80 p-8 text-center text-text-secondary">
            No provenance entries in response.
          </div>
        ) : (
          provenance.map((p, i) => (
            <div
              key={i}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-5"
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-medium text-text-primary">{p.source_name}</span>
                {p.status != null && <StatusChip status={p.status} />}
              </div>
              {p.fetched_at && (
                <p className="mt-2 text-sm text-text-muted">Fetched: {new Date(p.fetched_at).toISOString()}</p>
              )}
              {p.note && <p className="mt-1 text-sm text-text-secondary">{p.note}</p>}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
