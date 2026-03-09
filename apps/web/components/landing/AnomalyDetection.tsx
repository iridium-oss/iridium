"use client";

import { motion } from "framer-motion";

export function AnomalyDetection() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="anomaly">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Anomaly detection
          </h2>
          <p className="mt-6 text-text-secondary">
            Rule-based pipeline over speed deviations, optional provider alerts, and event or weather signals. Detected anomalies are labeled by type, severity, confidence, affected geography, and source family (observed, inferred, or provider-reported). The pipeline does not consume synthetic anomaly streams; it operates on real twin state and configured providers.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
