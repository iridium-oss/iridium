"use client";

import { useCallback, useEffect, useState } from "react";
import { apiGet, apiPost } from "@/lib/api";
import type { ProviderEntry, SystemProvidersResponse } from "@/lib/api";
import { StatusChip } from "@/components/ui/StatusChip";
import { Icon } from "@/components/ui/Icon";

export default function ProvidersPage() {
  const [data, setData] = useState<SystemProvidersResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [verifying, setVerifying] = useState<string | null>(null);

  const load = useCallback(() => {
    apiGet<SystemProvidersResponse>("/api/v1/system/providers")
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleVerify = (providerId: string) => {
    setVerifying(providerId);
    apiPost<{ validation_status: string; message: string }>(
      `/api/v1/system/providers/${encodeURIComponent(providerId)}/verify`,
      {}
    )
      .then(() => load())
      .catch(() => load())
      .finally(() => setVerifying(null));
  };

  if (error) {
    return (
      <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
        {error}
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Providers
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        External APIs and data sources. Source family, status, and capabilities. Run verify to check connectivity.
      </p>

      {!data ? (
        <div className="mt-6 flex items-center gap-2 text-text-muted">
          <span className="material-symbols-outlined animate-pulse">progress_activity</span>
          Loading...
        </div>
      ) : (
        <div className="mt-6 space-y-4">
          {data.providers.map((p) => (
            <div
              key={p.id}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-4"
            >
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div>
                  <h2 className="font-medium text-text-primary">{p.display_name}</h2>
                  <p className="mt-0.5 text-xs text-text-muted">
                    {p.id} {p.domain ? `| ${p.domain}` : ""}
                  </p>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <StatusChip status={p.source_status} label={p.source_status} />
                  {p.validation_status && p.validation_status !== "not_checked" && (
                    <StatusChip status={p.validation_status} label={p.validation_status} />
                  )}
                  <button
                    type="button"
                    onClick={() => handleVerify(p.id)}
                    disabled={verifying === p.id}
                    className="rounded border border-surface-border bg-white px-3 py-1.5 text-xs font-medium text-text-primary hover:bg-surface-deep disabled:opacity-50"
                  >
                    {verifying === p.id ? "Checking..." : "Verify"}
                  </button>
                </div>
              </div>
              {p.note && (
                <p className="mt-2 text-xs text-text-secondary">{p.note}</p>
              )}
              {p.required_env_vars && p.required_env_vars.length > 0 && (
                <p className="mt-1 text-xs text-text-muted">
                  Required env: {p.required_env_vars.join(", ")}
                </p>
              )}
              {p.capabilities && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {p.capabilities.supports_search && (
                    <span className="rounded bg-sky-100 px-1.5 py-0.5 text-xs text-sky-800">search</span>
                  )}
                  {p.capabilities.supports_metadata && (
                    <span className="rounded bg-sky-100 px-1.5 py-0.5 text-xs text-sky-800">metadata</span>
                  )}
                  {p.capabilities.supports_alerts && (
                    <span className="rounded bg-amber-100 px-1.5 py-0.5 text-xs text-amber-800">alerts</span>
                  )}
                  {p.capabilities.supports_realtime && (
                    <span className="rounded bg-green-100 px-1.5 py-0.5 text-xs text-green-800">realtime</span>
                  )}
                  {p.capabilities.supports_routing && (
                    <span className="rounded bg-purple-100 px-1.5 py-0.5 text-xs text-purple-800">routing</span>
                  )}
                  {p.capabilities.supports_web_observation && (
                    <span className="rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-700">web_observed</span>
                  )}
                  {p.capabilities.supports_auth && (
                    <span className="rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-700">auth</span>
                  )}
                </div>
              )}
              {p.frontend_consumer_surfaces && p.frontend_consumer_surfaces.length > 0 && (
                <p className="mt-1 text-xs text-text-muted">
                  Surfaces: {p.frontend_consumer_surfaces.join(", ")}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
