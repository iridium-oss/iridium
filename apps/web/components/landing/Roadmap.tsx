"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const PHASES = [
  { phase: 1, title: "Real-source digital twin baseline", text: "OSM network, weather, transit providers. Source status and provenance on every boundary. Implemented." },
  { phase: 2, title: "Transit and route intelligence hardening", text: "GTFS builder, routing with fare and carbon. OTP/Valhalla integration when feeds available. In progress." },
  { phase: 3, title: "Richer realtime and partner integrations", text: "More providers, optional traffic, partner data under license. Status semantics extended." },
  { phase: 4, title: "Forecasting and anomaly depth", text: "ST-GNN pipeline, anomaly refinement. Better short-horizon and operational alerts." },
  { phase: 5, title: "Equity analytics maturity", text: "District data pipelines, methodology publication. Policy-ready indicators with documentation." },
  { phase: 6, title: "Federated learning experiments and institutional deployment readiness", text: "Orchestration (e.g. Flower), experiments, and deployment playbooks for institutions." },
];

export function Roadmap() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="roadmap">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Roadmap
          </h2>
          <p className="mt-4 text-text-secondary">
            Realistic phases aligned with proposed commercial modules (routing, analytics, equity, federated learning readiness). Honest and visually clear. No invented timelines or deliverables.
          </p>
        </motion.div>
        <div className="mt-14 space-y-4">
          {PHASES.map(({ phase, title, text }, i) => (
            <motion.div
              key={phase}
              initial={{ opacity: 0, x: -12 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="flex gap-6 rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-midnight-electric/20 text-lg font-medium text-accent-luminous">
                {phase}
              </span>
              <div>
                <h3 className="font-medium text-text-primary">{title}</h3>
                <p className="mt-2 text-sm text-text-secondary">{text}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
