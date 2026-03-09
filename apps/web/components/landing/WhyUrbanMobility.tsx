"use client";

import { motion } from "framer-motion";

export function WhyUrbanMobility() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="why">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Why urban mobility needs this
          </h2>
          <p className="mt-6 text-text-secondary">
            Growing cities face congestion, unreliable travel times, and fragmented data held by multiple operators. Effective prediction and optimization require combining sensor data, transit schedules, weather, and events, yet centralizing raw data is often infeasible due to privacy, regulation, and data sovereignty.
          </p>
          <p className="mt-4 text-text-secondary">
            IRIDIUM addresses an operational and architectural gap: many research systems rely on synthetic or offline datasets, while production systems often lack transparent data governance and provenance. We implement a real-data stack where each source is documented, each response carries a data status, and the digital twin is built only from sources that are actually configured and reachable.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
