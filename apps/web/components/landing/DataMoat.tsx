"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const ITEMS = [
  "Ability to unify official, observed, and partner sources under one schema with clear labels.",
  "Provenance tracking on ingestion: source URL, fetched_at, response checksum where applicable.",
  "Source hierarchy and priority policy (e.g. official alerts over observed) documented and implementable.",
  "Historical accumulation potential: as more sources and time series are added, the twin can improve without fabricating history.",
  "Domain-specific transport normalization: GTFS-style routes, stops, fare policy; Baku Metro and BakuBus provider abstraction.",
  "Future city-specific operational intelligence layer: same architecture can extend to more cities and modes.",
];

export function DataMoat() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="data-moat">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Data moat
          </h2>
          <p className="mt-4 text-text-secondary">
            Distinct from technology moat. We do not overclaim. No fantasy about proprietary data unless it truly exists. Strategic section on unification and provenance, not fake claims.
          </p>
        </motion.div>
        <ul className="mt-10 space-y-4">
          {ITEMS.map((item, i) => (
            <motion.li
              key={i}
              initial={{ opacity: 0, x: -8 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
              className="flex items-start gap-3 rounded-xl border border-surface-border bg-surface-card/80 p-4 backdrop-blur"
            >
              <Icon name="storage" size={20} className="shrink-0 text-accent-luminous mt-0.5" />
              <span className="text-sm text-text-secondary">{item}</span>
            </motion.li>
          ))}
        </ul>
      </div>
    </section>
  );
}
