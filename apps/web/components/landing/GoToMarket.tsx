"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const SEQUENCE = [
  {
    step: 1,
    title: "Baku demonstration narrative",
    text: "Demonstrate value with real data: digital twin, transit provider status, routing, and equity analytics. No claim of signed pilots or contracts; this is the strategic plan.",
  },
  {
    step: 2,
    title: "Operator and municipal value",
    text: "Show operational visibility and source transparency to operators and municipalities. Decision support under partial data as a differentiator.",
  },
  {
    step: 3,
    title: "Public-sector deployment pathway",
    text: "Position for public-sector adoption where provenance and data sovereignty matter. Open-source and documentation support evaluation.",
  },
  {
    step: 4,
    title: "Expansion to other Azerbaijani cities",
    text: "Extend to Guba and other cities as the platform proves value and as data sources become available.",
  },
  {
    step: 5,
    title: "Regional or enterprise expansion",
    text: "Later phase: regional deployment or enterprise integrations when product-market fit and partnerships support it.",
  },
];

const ADOPTION_PATHS = [
  {
    title: "Municipal adoption path",
    items: [
      "Evaluation via open-source, documentation, and demo. No invented pilot contracts.",
      "Procurement and integration logic: deployment-led sales (city or agency adopts platform for operations or planning), not consumer-only growth.",
      "Institutional trust and governance: provenance, auditability, and deployment options (cloud, on-premises, sovereign) support procurement and compliance.",
    ],
  },
  {
    title: "Operator adoption path",
    items: [
      "Transit and mobility operators as buyers of operations dashboards, routing intelligence, and source-backed analytics.",
      "Pilot-to-platform path: demonstrate value in a controlled context; scale to full deployment when adoption criteria are met. No claim of current signed pilots.",
      "Integration with operator systems and data (GTFS, real-time APIs) as part of implementation services.",
    ],
  },
  {
    title: "Procurement and integration",
    items: [
      "Public-sector procurement often specifies deployment location, data handling, and vendor obligations. Multiple deployment models support compliant tenders.",
      "Integration with legacy systems and internal networks is addressed via on-premises or hybrid deployment and professional services.",
    ],
  },
];

export function GoToMarket() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="go-to-market">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Go-to-market and procurement
          </h2>
          <p className="mt-4 text-text-secondary">
            Strategic go-to-market plan reflecting public-sector reality. We do not claim pilots or signed partnerships unless they exist. Honest framing of adoption pathway, procurement logic, and deployment-led growth.
          </p>
        </motion.div>

        <div className="mt-14 space-y-6">
          {SEQUENCE.map(({ step, title, text }, i) => (
            <motion.div
              key={step}
              initial={{ opacity: 0, x: -12 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="flex gap-6 rounded-xl border border-surface-border bg-surface-card/80 p-6"
            >
              <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-midnight-electric/20 text-lg font-medium text-accent-luminous">
                {step}
              </span>
              <div>
                <h3 className="font-medium text-text-primary">{title}</h3>
                <p className="mt-2 text-sm text-text-secondary">{text}</p>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="mt-16">
          <h3 className="text-xl font-medium text-text-primary border-b border-surface-border pb-3 mb-8">
            Adoption paths and procurement logic
          </h3>
          <div className="grid gap-8 lg:grid-cols-3">
            {ADOPTION_PATHS.map((path, i) => (
              <motion.div
                key={path.title}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="rounded-xl border border-surface-border bg-white p-6"
              >
                <div className="flex items-center gap-2 mb-4">
                  <Icon name="route" size={22} className="text-accent-luminous shrink-0" />
                  <h4 className="font-medium text-text-primary">{path.title}</h4>
                </div>
                <ul className="space-y-3 text-sm text-text-secondary">
                  {path.items.map((item) => (
                    <li key={item} className="flex items-start gap-2">
                      <span className="shrink-0 mt-1.5 h-1.5 w-1.5 rounded-full bg-accent-muted" />
                      {item}
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
