"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const ITEMS = [
  { icon: "code" as const, title: "Formalized formulation", text: "Mobility graph, routing objective, forecasting target, equity composite, anomaly score consistent with the codebase." },
  { icon: "verified" as const, title: "Reproducible", text: "Open source (EUPL-1.2). Code version, environment variables, and data sources documented." },
  { icon: "science" as const, title: "Baseline evaluation", text: "API semantics, response latency, source-status composition, real weather integration for Baku and Quba." },
];

export function TechnicalCredibility() {
  return (
    <section className="border-t border-surface-border bg-midnight-prussian/50 py-20 sm:py-28" id="credibility">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Technical credibility
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-text-secondary">
            Implemented and evaluated with honest scope. No fabricated benchmarks or synthetic results in the main path.
          </p>
        </motion.div>
        <div className="mt-14 grid gap-8 sm:grid-cols-3">
          {ITEMS.map(({ icon, title, text }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 text-center"
            >
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-midnight-electric/20 text-accent-luminous">
                <Icon name={icon} size={28} />
              </span>
              <h3 className="mt-4 font-medium text-text-primary">{title}</h3>
              <p className="mt-2 text-sm text-text-secondary">{text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
