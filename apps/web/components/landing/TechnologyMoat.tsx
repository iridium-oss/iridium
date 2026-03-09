"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const ITEMS = [
  "Provenance-aware response model: every boundary can carry source_provider, source_family, source_status.",
  "Source-status semantics implemented and documented. Not marketing; real API and schema.",
  "Modular provider architecture: add Baku Metro, BakuBus, weather, traffic without a single monolith.",
  "Digital twin assembly logic: merge network, weather, transit into one graph with clear provenance.",
  "Future federated learning pathway: architecture and docs in place; no raw data centralization required.",
  "Real-source normalization layer: canonical schema, no fabricated fields. Missing data stays null.",
  "Explainable degraded-mode behavior: when a source is down, the system reports it instead of substituting.",
];

export function TechnologyMoat() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="technology-moat">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Technology moat
          </h2>
          <p className="mt-4 text-text-secondary">
            Real technical advantage and implementation depth. We do not overclaim defensibility; we phrase it as what is built and documented.
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
              <Icon name="code" size={20} className="shrink-0 text-accent-luminous mt-0.5" />
              <span className="text-sm text-text-secondary">{item}</span>
            </motion.li>
          ))}
        </ul>
      </div>
    </section>
  );
}
