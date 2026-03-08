"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiGet, Health, Version } from "@/lib/api";
import { Icon } from "@/components/ui/Icon";

const QUICK_LINKS = [
  { href: "/dashboard/network", label: "Digital twin", icon: "hub" as const },
  { href: "/dashboard/forecast", label: "Forecast", icon: "trending_up" as const },
  { href: "/dashboard/routing", label: "Routing", icon: "route" as const },
  { href: "/dashboard/equity", label: "Equity", icon: "balance" as const },
  { href: "/dashboard/anomalies", label: "Anomalies", icon: "warning" as const },
];

export default function DashboardOverviewPage() {
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

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Overview
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        System status and quick access to modules. Data status is shown per panel.
      </p>

      {error && (
        <div className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          API unreachable: {error}. Start the API (e.g. make run-api) and refresh.
        </div>
      )}

      {!error && (!health || !version) && (
        <div className="mt-6 flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card/80 px-4 py-3 text-text-secondary">
          <span className="material-symbols-outlined animate-pulse">progress_activity</span>
          Checking API...
        </div>
      )}

      {health && version && (
        <div className="mt-6 rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="flex items-center gap-2 font-medium text-text-primary">
            <Icon name="check_circle" size={20} className="text-green-400" />
            System status
          </h2>
          <p className="mt-2 text-sm text-text-secondary">
            Status: {health.status}. Service: {version.service}. App version: {version.app_version}. API version: {version.api_version}.
          </p>
        </div>
      )}

      <div className="mt-8">
        <h2 className="font-medium text-text-primary">Dashboard</h2>
        <p className="mt-1 text-sm text-text-secondary">
          Navigate to each module below. Data status (live, unavailable, configuration required) is shown per panel where applicable.
        </p>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {QUICK_LINKS.map(({ href, label, icon }) => (
            <Link
              key={href}
              href={href}
              className="flex items-center gap-4 rounded-xl border border-surface-border bg-surface-card/80 p-4 transition-colors hover:bg-surface-elevated"
            >
              <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-midnight-electric/20 text-accent-luminous">
                <Icon name={icon} size={24} />
              </span>
              <span className="font-medium text-text-primary">{label}</span>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
