"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const MODULES = [
  { id: "network", name: "Network and digital twin", desc: "OSM-based ingestion, PostGIS storage, graph snapshot with provenance." },
  { id: "forecast", name: "Congestion forecasting", desc: "Short-horizon heuristic baseline; ST-GNN pipeline architected." },
  { id: "routing", name: "Multimodal routing", desc: "Time, cost, carbon optimization; OTP/Valhalla integration planned." },
  { id: "equity", name: "Equity analytics", desc: "District-level MES from configured indicators; no synthetic scores." },
  { id: "anomaly", name: "Anomaly detection", desc: "Rule-based pipeline; labeled by type, severity, and source." },
];

export function CoreModules() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="modules">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Core modules
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-text-secondary">
            Implemented and documented. Evaluation scope is baseline system behavior and real-source integration.
          </p>
        </motion.div>
        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {MODULES.map(({ id, name, desc }, i) => (
            <motion.div
              key={id}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="rounded-xl border border-surface-border bg-surface-card/60 p-6"
            >
              <div className="flex items-start gap-4">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-surface-elevated text-text-primary">
                  <Icon name="widgets" size={24} />
                </span>
                <div>
                  <h3 className="font-medium text-text-primary">{name}</h3>
                  <p className="mt-2 text-sm text-text-secondary">{desc}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
