"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const SERVICES = [
  {
    title: "Implementation and integration support",
    description: "Project-based support for deployment, configuration, and go-live. Aligns with how municipal and operator rollouts are executed.",
  },
  {
    title: "Provider onboarding",
    description: "Onboarding of transit and mobility data sources, including GTFS, real-time APIs, and third-party feeds. Supports operational readiness.",
  },
  {
    title: "Transit and source normalization work",
    description: "Data normalization, schema alignment, and source registry setup. Ensures provenance and status semantics are correctly applied.",
  },
  {
    title: "Operational dashboard configuration",
    description: "Configuration of control-room views, alerts, and reporting to match institutional workflows.",
  },
  {
    title: "Training and change management",
    description: "Training for operators and municipal staff; change management for adoption. Standard in public-sector technology rollout.",
  },
  {
    title: "Maintenance and support",
    description: "Ongoing maintenance, updates, and support packages. TwinCity3D and similar platforms offer support as part of deployment.",
  },
  {
    title: "Data quality and provenance setup",
    description: "Setup of data quality checks, provenance metadata, and source-status semantics. Supports audit and accountability.",
  },
  {
    title: "Research partnership support",
    description: "Support for grant-funded or research deployments: documentation, reproducibility, and integration with academic workflows.",
  },
  {
    title: "Custom reporting and policy-analysis support",
    description: "Custom reports and policy-oriented analytics for planning and decision support. Add-on to core platform.",
  },
];

export function ServicesLayer() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="services-layer">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Professional services and institutional enablement
          </h2>
          <p className="mt-4 text-text-secondary">
            A services layer makes the business model realistic for public-sector adoption. Implementation, integration, training, and support are standard in municipal and operator technology deployments; they are proposed as part of the commercial architecture, not claimed as current delivered engagements.
          </p>
        </motion.div>

        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {SERVICES.map((item, i) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.03 }}
              className="rounded-xl border border-surface-border bg-white p-6"
            >
              <div className="flex items-center gap-2">
                <Icon name="engineering" size={22} className="text-accent-luminous shrink-0" />
                <h3 className="font-medium text-text-primary text-sm">{item.title}</h3>
              </div>
              <p className="mt-2 text-sm text-text-secondary">{item.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
