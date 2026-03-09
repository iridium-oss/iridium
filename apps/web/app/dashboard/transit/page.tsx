"use client";

import { useEffect, useState } from "react";
import {
  apiGet,
  TransitProvidersResponse,
  TransitRoutesResponse,
  TransitReadinessResponse,
  TransitGtfsStatusResponse,
  TransitAlertsResponse,
  TransitPredictedArrivalsResponse,
  TransitSourceStatusResponse,
} from "@/lib/api";
import { StatusChip } from "@/components/ui/StatusChip";
import { Icon } from "@/components/ui/Icon";

function SourceBadge({ sourceStatus, sourceFamily }: { sourceStatus: string; sourceFamily?: string }) {
  const isOfficial = sourceStatus === "official_alerts_only" || sourceFamily === "official_website";
  const isPublicWeb = sourceStatus === "public_web_observed" || sourceStatus === "public_web_operational_context";
  const isLicensed = sourceStatus === "licensed_partner" || sourceStatus === "partner_required";
  const label = isOfficial ? "official" : isPublicWeb ? "public-web observed" : isLicensed ? "licensed partner" : sourceStatus || "unavailable";
  const variant = isOfficial ? "live" : isPublicWeb ? "permission_required" : "unavailable";
  return <StatusChip status={variant} label={label} />;
}

export default function TransitPage() {
  const [providers, setProviders] = useState<TransitProvidersResponse | null>(null);
  const [routes, setRoutes] = useState<TransitRoutesResponse | null>(null);
  const [readiness, setReadiness] = useState<TransitReadinessResponse | null>(null);
  const [gtfsStatus, setGtfsStatus] = useState<TransitGtfsStatusResponse | null>(null);
  const [alerts, setAlerts] = useState<TransitAlertsResponse | null>(null);
  const [predictedArrivals, setPredictedArrivals] = useState<TransitPredictedArrivalsResponse | null>(null);
  const [sourceStatus, setSourceStatus] = useState<TransitSourceStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      apiGet<TransitProvidersResponse>("/api/v1/transit/providers"),
      apiGet<TransitRoutesResponse>("/api/v1/transit/routes?bakubus_limit=0"),
      apiGet<TransitReadinessResponse>("/api/v1/transit/readiness"),
      apiGet<TransitGtfsStatusResponse>("/api/v1/transit/gtfs/status"),
      apiGet<TransitAlertsResponse>("/api/v1/transit/alerts"),
      apiGet<TransitPredictedArrivalsResponse>("/api/v1/transit/predicted-arrivals"),
      apiGet<TransitSourceStatusResponse>("/api/v1/transit/source-status"),
    ])
      .then(([p, r, rd, g, a, pa, ss]) => {
        setProviders(p);
        setRoutes(r);
        setReadiness(rd);
        setGtfsStatus(g);
        setAlerts(a);
        setPredictedArrivals(pa);
        setSourceStatus(ss);
      })
      .catch((e) => setError(e.message));
  }, []);

  if (error) {
    return (
      <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
        Error: {error}
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Transit
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        BakuBus (AYNA) and Baku Metro. Unified providers; status reflects live, static, or permission-required. No fake realtime predictions.
      </p>

      {!providers && !readiness && (
        <div className="mt-6 flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card/80 px-4 py-6 text-text-secondary">
          <span className="material-symbols-outlined animate-pulse">progress_activity</span>
          Loading transit data...
        </div>
      )}

      {sourceStatus && (
        <div className="mt-8">
          <h2 className="font-medium text-text-primary">Source status</h2>
          <p className="mt-1 text-sm text-text-secondary">
            Data type: official, public-web observed, licensed partner, or unavailable. No fake vehicle positions or ETAs.
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            {(sourceStatus.providers ?? []).map((s) => (
              <div key={s.provider_id} className="flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card/80 px-3 py-2">
                <span className="text-sm font-medium text-text-primary">{s.provider_id}</span>
                <SourceBadge sourceStatus={s.source_status ?? "unavailable"} sourceFamily={s.source_family} />
                {s.configured !== undefined && <span className="text-xs text-text-muted">({s.configured ? "configured" : "not configured"})</span>}
              </div>
            ))}
          </div>
          {sourceStatus.note && <p className="mt-2 text-xs text-text-muted">{sourceStatus.note}</p>}
        </div>
      )}

      {providers && (
        <div className="mt-8">
          <h2 className="font-medium text-text-primary">Providers</h2>
          <p className="mt-1 text-sm text-text-secondary">
            BakuBus and Baku Metro as separate but unified providers. Status badges show live, static, or permission-required.
          </p>
          <div className="mt-4 space-y-3">
            {(providers.providers ?? []).map((p) => (
              <div
                key={p.provider_id}
                className="flex flex-wrap items-center gap-3 rounded-xl border border-surface-border bg-surface-card/80 p-4"
              >
                <span className="font-medium text-text-primary">{p.name}</span>
                <StatusChip
                  status={p.status === "live" ? "live" : p.status === "permission_required" ? "permission_required" : "unavailable"}
                />
                {p.note && <span className="text-sm text-text-muted">{p.note}</span>}
              </div>
            ))}
          </div>
        </div>
      )}

      {alerts && (
        <div className="mt-8">
          <h2 className="font-medium text-text-primary">Official alerts</h2>
          <p className="mt-1 text-sm text-text-secondary">
            Alerts from BakuBus and Baku Metro official pages. Merged by source priority.
          </p>
          <ul className="mt-4 space-y-2">
            {(alerts.alerts || []).slice(0, 15).map((a) => (
              <li key={a.alert_id} className="flex flex-wrap items-center gap-2 rounded-lg border border-surface-border bg-surface-card/80 px-4 py-3">
                <span className="font-medium text-text-primary">{a.title ?? "Alert"}</span>
                <SourceBadge sourceStatus={a.source_status ?? "unavailable"} sourceFamily={a.source_family} />
                {a.source_url && (
                  <a href={a.source_url} target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:underline">
                    Source
                  </a>
                )}
              </li>
            ))}
          </ul>
          {alerts.alerts && alerts.alerts.length > 15 && <p className="mt-2 text-xs text-text-muted">Showing first 15 of {alerts.alerts.length} alerts.</p>}
          {alerts.source_note && <p className="mt-2 text-xs text-text-muted">{alerts.source_note}</p>}
        </div>
      )}

      {predictedArrivals && (
        <div className="mt-8">
          <h2 className="font-medium text-text-primary">Predicted arrivals</h2>
          <p className="mt-1 text-sm text-text-secondary">
            Stop-level predictions where observed (e.g. from Yandex). Public-web observed; not official operator feed.
          </p>
          {(predictedArrivals.predicted_arrivals?.length ?? 0) === 0 && (predictedArrivals.stop_statuses?.length ?? 0) === 0 ? (
            <p className="mt-4 text-sm text-text-muted">No predicted arrivals or stop statuses in this sample. Data may be JS-rendered on source pages.</p>
          ) : (
            <>
              {predictedArrivals.predicted_arrivals && predictedArrivals.predicted_arrivals.length > 0 && (
                <ul className="mt-4 space-y-2">
                  {predictedArrivals.predicted_arrivals.slice(0, 10).map((p) => (
                    <li key={p.prediction_id} className="rounded-lg border border-surface-border bg-surface-card/80 px-4 py-2 text-sm text-text-secondary">
                      Stop {p.stop_id} | predicted {p.predicted_at ?? "n/a"} | {p.source_provider} ({p.source_status})
                    </li>
                  ))}
                </ul>
              )}
              {predictedArrivals.stop_statuses && predictedArrivals.stop_statuses.length > 0 && (
                <p className="mt-2 text-xs text-text-muted">Stop statuses: {predictedArrivals.stop_statuses.map((s) => s.stop_id).join(", ")}</p>
              )}
            </>
          )}
          {predictedArrivals.source_note && <p className="mt-2 text-xs text-text-muted">{predictedArrivals.source_note}</p>}
        </div>
      )}

      {routes && (
        <div className="mt-8">
          <h2 className="font-medium text-text-primary">Routes</h2>
          <p className="mt-1 text-sm text-text-secondary">
            Metro lines and bus routes (metro only when bakubus_limit=0). Add ?bakubus_limit=10 to fetch bus routes from AYNA.
          </p>
          <div className="mt-4 rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-surface-border text-left text-text-muted">
                    <th className="p-3 font-medium">Route ID</th>
                    <th className="p-3 font-medium">Agency</th>
                    <th className="p-3 font-medium">Short name</th>
                    <th className="p-3 font-medium">Source</th>
                  </tr>
                </thead>
                <tbody>
                  {(routes.routes || []).slice(0, 30).map((r) => (
                    <tr key={r.route_id} className="border-b border-surface-border/50 text-text-secondary">
                      <td className="p-3 font-mono">{r.route_id}</td>
                      <td className="p-3">{r.agency_id}</td>
                      <td className="p-3">{r.short_name ?? ""}</td>
                      <td className="p-3">{r.source_provider} ({r.source_status})</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {routes.routes && routes.routes.length > 30 && (
              <p className="border-t border-surface-border px-4 py-2 text-xs text-text-muted">
                Showing first 30 of {routes.routes.length} routes.
              </p>
            )}
          </div>
        </div>
      )}

      {readiness && (
        <div className="mt-8">
          <h2 className="font-medium text-text-primary">Readiness for OTP</h2>
          <p className="mt-1 text-sm text-text-secondary">
            Static stop discovery, route visualization, transfer graph, timetable routing. Honest about missing stop_times.
          </p>
          <ul className="mt-4 space-y-2 text-sm text-text-secondary">
            <li className="flex items-center gap-2">
              {readiness.static_stop_discovery ? (
                <Icon name="check_circle" size={18} className="text-green-400" />
              ) : (
                <Icon name="cancel" size={18} className="text-red-400" />
              )}
              Static stop discovery
            </li>
            <li className="flex items-center gap-2">
              {readiness.route_visualization ? (
                <Icon name="check_circle" size={18} className="text-green-400" />
              ) : (
                <Icon name="cancel" size={18} className="text-red-400" />
              )}
              Route visualization
            </li>
            <li className="flex items-center gap-2">
              {readiness.transfer_graph ? (
                <Icon name="check_circle" size={18} className="text-green-400" />
              ) : (
                <Icon name="cancel" size={18} className="text-red-400" />
              )}
              Transfer graph
            </li>
            <li className="flex items-center gap-2">
              {readiness.timetable_routing ? (
                <Icon name="check_circle" size={18} className="text-green-400" />
              ) : (
                <Icon name="cancel" size={18} className="text-red-400" />
              )}
              Timetable routing (not available without exact stop_times)
            </li>
          </ul>
          {readiness.missing_for_otp && readiness.missing_for_otp.length > 0 && (
            <div className="mt-4 rounded-lg border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-sm text-amber-200">
              <p className="font-medium">Missing for production OTP</p>
              <ul className="mt-2 list-inside list-disc">
                {readiness.missing_for_otp.map((m, i) => (
                  <li key={i}>{m}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {gtfsStatus && (
        <div className="mt-8">
          <h2 className="font-medium text-text-primary">GTFS status</h2>
          <p className="mt-1 text-sm text-text-secondary">
            Repository-generated GTFS; not operator-issued.
          </p>
          <div className="mt-4 rounded-xl border border-surface-border bg-surface-card/80 p-4">
            <p className="text-sm text-text-secondary">{gtfsStatus.label}</p>
            <p className="mt-2 text-sm text-text-muted">Built: {gtfsStatus.built ? "Yes" : "No"}. {gtfsStatus.note}</p>
          </div>
        </div>
      )}
    </div>
  );
}
