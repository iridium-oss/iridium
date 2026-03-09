"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const SEQUENCE = [
  { step: 1, title: "Baku pilot narrative", text: "Demonstrate value with real data: digital twin, transit provider status, routing, and equity analytics. No claim of signed pilots or contracts; this is the strategic plan." },
  { step: 2, title: "Operator and municipal value", text: "Show operational visibility and source transparency to operators and municipalities. Decision support under partial data as a differentiator." },
  { step: 3, title: "Public-sector deployment pathway", text: "Position for public-sector adoption where provenance and data sovereignty matter. Open-source and documentation support evaluation." },
  { step: 4, title: "Expansion to other Azerbaijani cities", text: "Extend to Guba and other cities as the platform proves value and as data sources become available." },
  { step: 5, title: "Regional or enterprise expansion", text: "Later phase: regional deployment or enterprise integrations when product-market fit and partnerships support it." },
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
            Go-to-market
          </h2>
          <p className="mt-4 text-text-secondary">
            Strategic go-to-market plan. We do not claim pilots or signed partnerships unless they exist. Honest framing of sequence and pathway.
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
              className="flex gap-6 rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
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
      </div>
    </section>
  );
}
