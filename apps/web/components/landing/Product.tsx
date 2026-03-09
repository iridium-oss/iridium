"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const CAPABILITIES = [
  { icon: "hub" as const, title: "Digital twin assembly", text: "Graph-based assembly of network and state from OSM, weather, and transit. Only configured, real sources; no synthetic substitution." },
  { icon: "route" as const, title: "Route planning", text: "Multimodal journey planning with time, cost, carbon, and transfer penalties. Objective and source-status are explicit." },
  { icon: "source" as const, title: "Source-aware transit operations", text: "Baku Metro and BakuBus provider abstraction. Status per source: live, static, permission_required, unavailable." },
  { icon: "trending_up" as const, title: "Forecasting pathway", text: "Short-horizon congestion forecast. Heuristic baseline today; ST-GNN pipeline architected for future use." },
  { icon: "warning" as const, title: "Anomaly awareness", text: "Rule-based detection over speed deviations and provider alerts. Labeled by type, severity, and source." },
  { icon: "balance" as const, title: "Equity analytics", text: "District-level Mobility Equity Score from normalized indicators. Transparent methodology; no synthetic scores." },
  { icon: "verified" as const, title: "Provenance and source-status transparency", text: "Every response can carry data status. API and UI expose what is live, partial, or unavailable." },
];

export function Product() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="product">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Product
          </h2>
          <p className="mt-4 text-text-secondary">
            A single platform for digital twin assembly, routing, forecasting, equity, and anomaly detection, with explicit provenance at every boundary.
          </p>
        </motion.div>
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {CAPABILITIES.map(({ icon, title, text }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
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
