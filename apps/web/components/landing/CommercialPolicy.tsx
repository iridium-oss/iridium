"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const POLICY_ITEMS = [
  "Current commercial model and current traction are clearly separated. The site and product materials describe what can be sold and how, not what has been sold.",
  "Future revenue lines and expansion modules are labeled as proposed or strategic. They are not presented as current revenue.",
  "No invented customers, contracts, pilots, grants, or partnerships. Only real proof points (repository, demo, integrations, documentation) are used as traction.",
  "No false investor-style vanity claims. No fabricated usage figures, installs, or deployment status.",
  "No fake numbers. No pricing is stated unless the repository already contains a justified pricing framework.",
];

export function CommercialPolicy() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="commercial-policy">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl flex items-center gap-3">
            <Icon name="policy" size={28} className="text-accent-luminous shrink-0" />
            Business model without overclaiming
          </h2>
          <p className="mt-4 text-text-secondary">
            Content policy for the site and product documentation. These rules preserve repository and website honesty and ensure that commercial narrative remains credible.
          </p>
        </motion.div>

        <ul className="mt-10 space-y-4">
          {POLICY_ITEMS.map((item, i) => (
            <motion.li
              key={i}
              initial={{ opacity: 0, x: -8 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="flex gap-3 rounded-lg border border-surface-border bg-white p-4"
            >
              <span className="shrink-0 flex h-6 w-6 items-center justify-center rounded-full bg-accent-muted/30 text-xs font-medium text-text-primary">
                {i + 1}
              </span>
              <span className="text-sm text-text-secondary">{item}</span>
            </motion.li>
          ))}
        </ul>
      </div>
    </section>
  );
}
