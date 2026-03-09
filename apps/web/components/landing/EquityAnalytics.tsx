"use client";

import { motion } from "framer-motion";

export function EquityAnalytics() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="equity">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Equity analytics
          </h2>
          <p className="mt-6 text-text-secondary">
            The Mobility Equity Score (MES) is a district-level composite of normalized indicators with configurable weights. The implementation reads district-level data from a configured path when available; otherwise it returns data status unavailable. MES is presented as a derived analytic index, not an official statistic; policy use should consider confounding factors and external validation.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
