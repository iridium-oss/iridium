"use client";

import { useEffect, useState } from "react";
import { apiGet, Health, Version } from "@/lib/api";
import { Icon } from "@/components/ui/Icon";

export default function StatusPage() {
  const [health, setHealth] = useState<Health | null>(null);
  const [version, setVersion] = useState<Version | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([apiGet<Health>("/health"), apiGet<Version>("/version")])
      .then(([h, v]) => {
        setHealth(h);
        setVersion(v);
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
      </div>
    </div>
  );
}
