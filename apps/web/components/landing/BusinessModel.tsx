"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const CURRENT = [
  "Open-source repository (EUPL-1.2). No production certification claimed.",
  "Working demo and dashboard. Real-data integrations where configured.",
  "Documentation and research paper readiness. Zenodo DOI.",
];

const PROPOSED = [
  "SaaS or platform subscriptions for municipalities and operators.",
  "Analytics and planning modules (equity, forecasting, routing).",
  "Premium routing and operations dashboards with source-status visibility.",
  "API access tiers for integrators and partners.",
  "Consulting and deployment support for institutional rollout.",
  "White-label institutional deployment where data stays on-premises.",
];

const FUTURE = [
  "Research and grant-supported deployments.",
  "Partner integrations (e.g. mobility apps, city platforms).",
  "Federated learning experiments and institutional deployment readiness.",
];

export function BusinessModel() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="business-model">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Business model
          </h2>
          <p className="mt-4 text-text-secondary">
            We do not invent current revenue. Below: what is current, what is proposed, and what is future commercial model. Framed as a credible pitch slide, not speculative fantasy.
          </p>
        </motion.div>
        <div className="mt-14 grid gap-8 lg:grid-cols-3">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
          >
            <div className="flex items-center gap-2">
              <Icon name="check_circle" size={24} className="text-accent-luminous" />
              <h3 className="font-medium text-text-primary">Current</h3>
            </div>
            <ul className="mt-4 space-y-2 text-sm text-text-secondary">
              {CURRENT.map((item) => (
                <li key={item} className="flex items-start gap-2">
                  <span className="shrink-0 mt-0.5 h-1.5 w-1.5 rounded-full bg-accent-luminous" />
                  {item}
                </li>
              ))}
            </ul>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.05 }}
            className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
          >
            <div className="flex items-center gap-2">
              <Icon name="pending" size={24} className="text-accent-muted" />
              <h3 className="font-medium text-text-primary">Proposed</h3>
            </div>
            <ul className="mt-4 space-y-2 text-sm text-text-secondary">
              {PROPOSED.map((item) => (
                <li key={item} className="flex items-start gap-2">
                  <span className="shrink-0 mt-0.5 h-1.5 w-1.5 rounded-full bg-accent-muted" />
                  {item}
                </li>
              ))}
            </ul>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
          >
            <div className="flex items-center gap-2">
              <Icon name="schedule" size={24} className="text-text-muted" />
              <h3 className="font-medium text-text-primary">Future</h3>
            </div>
            <ul className="mt-4 space-y-2 text-sm text-text-secondary">
              {FUTURE.map((item) => (
                <li key={item} className="flex items-start gap-2">
                  <span className="shrink-0 mt-0.5 h-1.5 w-1.5 rounded-full bg-text-muted" />
                  {item}
                </li>
              ))}
            </ul>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
