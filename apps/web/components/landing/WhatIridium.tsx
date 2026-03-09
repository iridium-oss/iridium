"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const POINTS = [
  { icon: "hub" as const, title: "Digital twin", text: "Graph-based assembly of network topology and state from OSM, weather, and optional traffic and transit sources." },
  { icon: "route" as const, title: "Multimodal routing", text: "Journey planning with time, cost, carbon, and transfer penalties. OTP and Valhalla integration planned." },
  { icon: "trending_up" as const, title: "Congestion forecasting", text: "Short-horizon speed and congestion forecasts. Heuristic baseline today; ST-GNN pipeline designed for future use." },
  { icon: "balance" as const, title: "Equity analytics", text: "District-level Mobility Equity Score from normalized indicators. Transparent methodology and bias documentation." },
  { icon: "warning" as const, title: "Anomaly detection", text: "Rule-based detection over speed deviations and provider alerts. Labeled by type, severity, and source." },
];

export function WhatIridium() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="what">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            What IRIDIUM does
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-text-secondary">
            A single platform for prediction, routing, equity, and anomaly detection, with explicit provenance and data-status semantics at every boundary.
          </p>
        </motion.div>
        <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {POINTS.map(({ icon, title, text }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-midnight-electric/20 text-accent-luminous">
                  <Icon name={icon} size={24} />
                </span>
                <h3 className="text-lg font-medium text-text-primary">{title}</h3>
              </div>
              <p className="mt-3 text-sm text-text-secondary">{text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
