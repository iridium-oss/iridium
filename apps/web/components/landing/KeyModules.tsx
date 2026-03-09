"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const MODULES = [
  { id: "twin", name: "Digital twin", what: "Assembles network and state from OSM, weather, transit.", who: "Operators, planners, API consumers.", data: "OSM, Open-Meteo, Baku Metro static, BakuBus AYNA.", maturity: "Implemented.", why: "Single source of truth for network and live state." },
  { id: "routing", name: "Routing", what: "Multimodal journey planning with time, cost, carbon.", who: "Riders, planners, dashboards.", data: "Twin graph, fare policy when available.", maturity: "Baseline implemented; OTP/Valhalla planned.", why: "Enables optimization and comparison across objectives." },
  { id: "forecast", name: "Forecasting", what: "Short-horizon congestion and speed forecasts.", who: "Operators, traffic management.", data: "Twin state, historical when configured.", maturity: "Heuristic baseline; ST-GNN designed.", why: "Supports proactive operations and alerts." },
  { id: "anomaly", name: "Anomaly intelligence", what: "Rule-based detection over deviations and alerts.", who: "Operators, incident response.", data: "Twin state, provider alerts.", maturity: "Implemented.", why: "Surfaces disruptions with type and source label." },
  { id: "equity", name: "Mobility equity", what: "District-level Mobility Equity Score.", who: "Planners, policy teams.", data: "Configured district indicators.", maturity: "Implemented when data path set.", why: "Makes inequity visible for targeting." },
  { id: "provenance", name: "Provenance", what: "Source and status on every boundary.", who: "All stakeholders.", data: "Provider metadata, fetch provenance.", maturity: "Implemented.", why: "Trust and auditability." },
  { id: "transit-ops", name: "Transit operations", what: "Source-aware transit provider abstraction.", who: "Operators, dashboards.", data: "Baku Metro, BakuBus, optional GTFS.", maturity: "Baku Metro static + BakuBus AYNA live.", why: "Unified view without fabricating feeds." },
];

export function KeyModules() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="key-modules">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Key modules
          </h2>
          <p className="mt-4 text-text-secondary">
            Pitch-deck style overview: what each module does, who it helps, what data it uses, maturity, and why it matters.
          </p>
        </motion.div>
        <div className="mt-14 space-y-6">
          {MODULES.map(({ id, name, what, who, data, maturity, why }, i) => (
            <motion.div
              key={id}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.03 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <div className="flex flex-wrap items-center justify-between gap-4">
                <h3 className="text-lg font-medium text-text-primary">{name}</h3>
                <span className="rounded-md border border-surface-border bg-surface-dark px-2.5 py-1 text-xs font-medium text-text-muted">
                  {maturity}
                </span>
              </div>
              <p className="mt-3 text-sm text-text-secondary">{what}</p>
              <div className="mt-4 grid gap-2 text-sm sm:grid-cols-2">
                <div><span className="text-text-muted">Who it helps:</span> <span className="text-text-secondary">{who}</span></div>
                <div><span className="text-text-muted">Data:</span> <span className="text-text-secondary">{data}</span></div>
              </div>
              <p className="mt-3 text-sm text-text-muted">Why it matters: {why}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
