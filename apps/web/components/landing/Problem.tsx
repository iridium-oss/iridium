"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const PROBLEMS = [
  {
    icon: "split" as const,
    title: "Fragmented transit and city data",
    text: "Transit, traffic, weather, and events sit in separate systems. No single view combines them with clear source labels and refresh status.",
  },
  {
    icon: "schedule" as const,
    title: "Weak real-time transparency",
    text: "Operators and riders often lack clear visibility into what data is live, what is stale, and what is missing. Systems that hide gaps reduce trust.",
  },
  {
    icon: "groups" as const,
    title: "Poor coordination across operators and city systems",
    text: "Multi-operator and multi-mode coordination requires a shared, source-aware layer. Today many dashboards are operator-specific or opaque.",
  },
  {
    icon: "route" as const,
    title: "Routing and disruption visibility gaps",
    text: "Journey planning and disruption awareness depend on unified network and real-time state. Partial or unlabeled data leads to wrong assumptions.",
  },
  {
    icon: "warning" as const,
    title: "Low trust in partial or opaque urban data",
    text: "When systems substitute synthetic data or do not label sources, planners and operators cannot rely on outputs for decisions.",
  },
  {
    icon: "accessibility" as const,
    title: "Accessibility and mobility inequity blind spots",
    text: "Without district-level and equity-aware analytics, cities cannot target interventions or measure fairness of service.",
  },
];

export function Problem() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="problem">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            The problem
          </h2>
          <p className="mt-4 text-text-secondary">
            Urban mobility suffers from fragmented data, weak real-time transparency, and low trust when source and status are unclear.
          </p>
        </motion.div>
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {PROBLEMS.map(({ icon, title, text }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-elevated text-accent-luminous">
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
