"use client";

import { useEffect, useState } from "react";
import { apiGet, EquityScore } from "@/lib/api";
import { StatusChip } from "@/components/ui/StatusChip";

export default function EquityPage() {
  const [data, setData] = useState<EquityScore | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiGet<EquityScore>("/api/v1/equity/score")
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
        Loading equity score...
      </div>
    );
  }

  const districts = data.districts ?? [];

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Equity analytics
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        District-level Mobility Equity Score from configured indicators. Returns data_status when path not set.
      </p>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        {data.data_status && <StatusChip status={data.data_status} />}
        {data.note && <span className="text-sm text-text-muted">{data.note}</span>}
      </div>

      {districts.length === 0 ? (
        <div className="mt-8 rounded-xl border border-surface-border bg-surface-card/80 p-8 text-center text-text-secondary">
          No district data in response. Configure EQUITY_DATA_PATH for real district scores.
        </div>
      ) : (
        <div className="mt-8 rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden">
          <div className="border-b border-surface-border px-4 py-3">
            <h2 className="font-medium text-text-primary">Districts</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-surface-border text-left text-text-muted">
                  <th className="p-3 font-medium">District ID</th>
                  <th className="p-3 font-medium">Name</th>
                  <th className="p-3 font-medium">MES</th>
                </tr>
              </thead>
              <tbody>
                {districts.map((d) => (
                  <tr key={d.district_id} className="border-b border-surface-border/50 text-text-secondary">
                    <td className="p-3 font-mono">{d.district_id}</td>
                    <td className="p-3">{d.name ?? ""}</td>
                    <td className="p-3">{d.mes != null ? d.mes.toFixed(3) : ""}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
