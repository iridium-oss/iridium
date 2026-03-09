"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const STEPS = [
  { icon: "download" as const, title: "Source ingestion", text: "Configured providers (OSM, Open-Meteo, Baku Metro static, BakuBus AYNA). Each fetch records provenance and response checksum." },
  { icon: "tune" as const, title: "Normalization", text: "Canonical schema: TransitAgency, TransitRoute, TransitStop, TransitFarePolicy, etc. No fabricated fields; missing data stays null." },
  { icon: "account_tree" as const, title: "Digital twin assembly", text: "Merge network, weather, transit, and optional traffic into a single graph. Nodes and edges carry source_provider and source_status." },
  { icon: "api" as const, title: "API and frontend", text: "REST API and dashboard expose network, forecast, routing, equity, anomalies. Every response can include data_status per source." },
  { icon: "schedule" as const, title: "Real-time or semi-realtime", text: "Weather and transit are refreshed on a documented cadence. When a source is down, status is explicit (unavailable, configuration_required)." },
  { icon: "info" as const, title: "Honest degradation", text: "No synthetic substitution in the main path. If GTFS or a provider is not configured, the system says so instead of filling with fake data." },
];

export function HowItWorks() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="how-it-works">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            How it works
          </h2>
          <p className="mt-4 text-text-secondary">
            From source ingestion to API and UI, with explicit source-status semantics and honest degradation when data is missing.
          </p>
        </motion.div>
        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {STEPS.map(({ icon, title, text }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-surface-elevated text-accent-luminous">
                  <Icon name={icon} size={24} />
                </span>
                <h3 className="font-medium text-text-primary">{title}</h3>
              </div>
              <p className="mt-3 text-sm text-text-secondary">{text}</p>
            </motion.div>
          ))}
        </div>
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mt-12 rounded-xl border border-surface-border bg-surface-card/60 p-6"
        >
          <h3 className="font-medium text-text-primary">Source status semantics</h3>
          <p className="mt-2 text-sm text-text-secondary">
            API and UI expose status per source: live, static_schedule_only, unavailable, configuration_required, permission_required. This allows evaluators and deployers to see exactly what is working and what is not.
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            {["live", "static_schedule_only", "unavailable", "configuration_required", "permission_required"].map((s) => (
              <span key={s} className="rounded-md border border-surface-border bg-surface-dark px-3 py-1.5 text-xs font-medium text-text-secondary">
                {s}
              </span>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
