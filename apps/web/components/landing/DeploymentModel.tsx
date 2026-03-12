"use client";
import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const MODELS = [
  {
    title: "Cloud-hosted subscription",
    description: "Platform delivered as a service with multi-tenant or dedicated instance. Standard for rapid adoption and lower initial procurement friction.",
    who: "Municipalities and operators without strict on-premises requirements.",
  },
  {
    title: "Municipality-hosted deployment",
    description: "Platform installed and operated in the city or agency data center. Data remains under direct institutional control.",
    who: "Public-sector buyers with existing IT infrastructure and data governance requirements.",
  },
  {
    title: "Operator-hosted deployment",
    description: "Deployment within the transit or mobility operator environment. Aligns with operator control over operational data.",
    who: "Transit operators and mobility service providers.",
  },
  {
    title: "Sovereign or on-premises deployment",
    description: "Full deployment in the customer environment for sensitive or regulated contexts. No data leaves the institutional boundary.",
    who: "Institutions with sovereignty, compliance, or procurement rules requiring on-premises software.",
  },
  {
    title: "White-label institutional deployment",
    description: "Institution-branded instance, optionally hosted by the institution or as a managed service. Supports co-branded or white-label positioning.",
    who: "Cities and operators requiring their own branding; consistent with Trafi, OpenMove, O-CITY white-label offerings.",
  },
  {
    title: "Hybrid deployment",
    description: "Sensitive data stays local; aggregated or non-sensitive workloads may use cloud. Supports gradual adoption and data-governance constraints.",
    who: "Institutions balancing innovation with data residency and governance.",
  },
];

const WHY_IT_MATTERS = [
  { label: "Procurement", text: "Public-sector procurement often specifies deployment location, data handling, and vendor obligations. Multiple deployment options support compliant tenders." },
  { label: "Data governance", text: "Cities and operators must meet data governance and retention rules. Local or sovereign deployment supports audit and control." },
  { label: "Sovereignty", text: "Sovereign deployment is standard in city technology stacks (e.g. Snap4City, TwinCity3D); it addresses institutional and regulatory expectations." },
  { label: "Legacy integration", text: "On-premises or hybrid models ease integration with legacy systems and internal networks." },
  { label: "Institutional trust", text: "Deployment choice supports trust: institutions can select the model that matches their risk and governance posture." },
];

export function DeploymentModel() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="deployment-model">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Delivery and deployment models
          </h2>
          <p className="mt-4 text-text-secondary">
            Multiple delivery options align with how public-sector and operator technology is procured and operated. Deployment model affects procurement, data governance, sovereignty, integration with legacy systems, and institutional trust.
          </p>
        </motion.div>

        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {MODELS.map((item, i) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6"
            >
              <div className="flex items-center gap-2">
                <Icon name="dns" size={24} className="text-accent-luminous shrink-0" />
                <h3 className="font-medium text-text-primary">{item.title}</h3>
              </div>
              <p className="mt-3 text-sm text-text-secondary">{item.description}</p>
              <p className="mt-2 text-xs text-text-muted">Who it is for: {item.who}</p>
            </motion.div>
          ))}
        </div>

        <div className="mt-16">
          <h3 className="text-lg font-medium text-text-primary mb-4">Why deployment choice matters in public-sector and operator settings</h3>
          <ul className="space-y-4">
            {WHY_IT_MATTERS.map((item, i) => (
              <motion.li
                key={item.label}
                initial={{ opacity: 0, x: -8 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="flex gap-4 rounded-lg border border-surface-border bg-white p-4"
              >
                <span className="shrink-0 font-medium text-text-primary">{item.label}</span>
                <span className="text-sm text-text-secondary">{item.text}</span>
              </motion.li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
