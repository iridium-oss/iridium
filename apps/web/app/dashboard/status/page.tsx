"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiGet, Health, Version, EOStatusResponse, IntegrationsStatusResponse } from "@/lib/api";
import { Icon } from "@/components/ui/Icon";
import { StatusChip } from "@/components/ui/StatusChip";

export default function StatusPage() {
  const [health, setHealth] = useState<Health | null>(null);
  const [version, setVersion] = useState<Version | null>(null);
  const [eoStatus, setEoStatus] = useState<EOStatusResponse | null>(null);
  const [integrations, setIntegrations] = useState<IntegrationsStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      apiGet<Health>("/health"),
      apiGet<Version>("/version"),
      apiGet<EOStatusResponse>("/api/v1/eo/status").catch(() => null),
      apiGet<IntegrationsStatusResponse>("/api/v1/system/integrations/status").catch(() => null),
    ])
      .then(([h, v, eo, int]) => {
        setHealth(h);
        setVersion(v);
        setEoStatus(eo ?? null);
        setIntegrations(int ?? null);
      })
      .catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
        API unreachable: {error}
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        System status
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        Health and version from the IRIDIUM API. Observability endpoints when available.
      </p>

      <div className="mt-8 grid gap-6 sm:grid-cols-2">
        <div className="rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="flex items-center gap-2 font-medium text-text-primary">
            <Icon name="monitor_heart" size={20} />
            Health
          </h2>
          {health ? (
            <p className="mt-2 text-sm text-text-secondary">Status: {health.status}</p>
          ) : (
            <p className="mt-2 text-sm text-text-muted">Checking...</p>
          )}
        </div>
        <div className="rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="flex items-center gap-2 font-medium text-text-primary">
            <Icon name="info" size={20} />
            Version
          </h2>
          {version ? (
            <ul className="mt-2 space-y-1 text-sm text-text-secondary">
              <li>Service: {version.service}</li>
              <li>App: {version.app_version}</li>
              <li>API: {version.api_version}</li>
            </ul>
          ) : (
            <p className="mt-2 text-sm text-text-muted">Checking...</p>
          )}
        </div>
        <div className="rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="flex items-center gap-2 font-medium text-text-primary">
            <Icon name="satellite_alt" size={20} />
            Earth observation
          </h2>
          {eoStatus ? (
            <div className="mt-2">
              <div className="flex flex-wrap items-center gap-2">
                <StatusChip status={eoStatus.data_status} />
                {eoStatus.enabled ? (
                  <span className="text-sm text-text-secondary">Enabled</span>
                ) : (
                  <span className="text-sm text-text-muted">Disabled</span>
                )}
              </div>
              {eoStatus.providers_available?.length ? (
                <p className="mt-1 text-xs text-text-muted">
                  Providers: {eoStatus.providers_available.join(", ")}
                </p>
              ) : null}
              {eoStatus.note && (
                <p className="mt-1 text-xs text-text-muted">{eoStatus.note}</p>
              )}
            </div>
          ) : (
            <p className="mt-2 text-sm text-text-muted">Not configured or unavailable.</p>
          )}
        </div>
        <div className="rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="flex items-center gap-2 font-medium text-text-primary">
            <Icon name="link" size={20} />
            Integrations
          </h2>
          {integrations ? (
            <div className="mt-2">
              <p className="text-sm text-text-secondary">
                {integrations.total_providers} providers by domain. See Providers page for verify and details.
              </p>
              {Object.keys(integrations.domains || {}).length > 0 && (
                <ul className="mt-2 space-y-1 text-xs text-text-muted">
                  {Object.entries(integrations.domains).map(([domain, list]) => (
                    <li key={domain}>
                      {domain}: {list.length}
                    </li>
                  ))}
                </ul>
              )}
              <Link
                href="/dashboard/providers"
                className="mt-3 inline-block text-sm font-medium text-indigo-600 hover:text-indigo-800"
              >
                View all providers
              </Link>
            </div>
          ) : (
            <p className="mt-2 text-sm text-text-muted">Loading...</p>
          )}
        </div>
      </div>
    </div>
  );
}
