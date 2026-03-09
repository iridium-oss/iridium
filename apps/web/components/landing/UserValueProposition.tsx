"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const PERSONAS = [
  { icon: "person" as const, title: "City residents", value: "Clear journey options, fare awareness, and disruption visibility when data is available. No false certainty from synthetic data." },
  { icon: "directions_bus" as const, title: "Public transport riders", value: "Multimodal routing with time, cost, and carbon. Source status so they know what is live vs partial." },
  { icon: "business" as const, title: "Operators", value: "Unified view of network and real-time state. Alerts and anomaly labels with source. Operational visibility without centralizing raw data." },
  { icon: "account_balance" as const, title: "Municipalities", value: "Planning support, equity analytics, and decision support under partial data. Transparent degradation when sources are unavailable." },
  { icon: "policy" as const, title: "Planning and policy teams", value: "District-level equity metrics, source-backed statistics, and reproducible methodology. No black-box or fabricated KPIs." },
  { icon: "school" as const, title: "Research and academic collaborators", value: "Open-source stack, documented provenance, and publication-ready positioning. Reproducibility and citation support." },
];

export function UserValueProposition() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="user-value">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            User value proposition
          </h2>
          <p className="mt-4 text-text-secondary">
            Value across residents, riders, operators, municipalities, planners, and researchers. Each persona benefits from real data and explicit provenance.
          </p>
        </motion.div>
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {PERSONAS.map(({ icon, title, value }, i) => (
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
              <p className="mt-3 text-sm text-text-secondary">{value}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
