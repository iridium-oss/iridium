"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const DIFFERENTIATORS = [
  { icon: "verified" as const, title: "Explicit source truthfulness", text: "Every source is labeled; every response can carry data status. No pretending unavailable data is present." },
  { icon: "block" as const, title: "No synthetic substitution", text: "Main runtime path never fills gaps with synthetic or fabricated data. Honest degradation builds trust." },
  { icon: "hub" as const, title: "Modular real-data architecture", text: "Digital twin and providers are modular. Add or remove sources without hiding status." },
  { icon: "account_balance" as const, title: "Public-sector suitability", text: "Designed for municipalities and operators who need auditability and data sovereignty." },
  { icon: "info" as const, title: "Source-status semantics", text: "live, static_schedule_only, unavailable, configuration_required, permission_required. Clear and documented." },
  { icon: "psychology" as const, title: "Future federated-learning path", text: "Architecture supports federated learning so training can stay distributed. Raw data does not need to centralize." },
  { icon: "science" as const, title: "Research and deployment duality", text: "Same codebase serves research (reproducibility, paper) and deployment (demo, operator value)." },
  { icon: "visibility" as const, title: "Open and inspectable", text: "Open-source stack. Technical posture can be reviewed and extended. No black-box claims." },
];

export function WhyIridiumWins() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="why-iridium-wins">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Why IRIDIUM wins
          </h2>
          <p className="mt-4 text-text-secondary">
            The why we win slide: explicit source truthfulness, no synthetic substitution, modular architecture, and public-sector suitability. These differentiators underpin a credible commercial model for municipalities and operators (see Business model and Go-to-market).
          </p>
        </motion.div>
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {DIFFERENTIATORS.map(({ icon, title, text }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.03 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-midnight-electric/20 text-accent-luminous">
                <Icon name={icon} size={24} />
              </span>
              <h3 className="mt-3 font-medium text-text-primary">{title}</h3>
              <p className="mt-2 text-sm text-text-secondary">{text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
