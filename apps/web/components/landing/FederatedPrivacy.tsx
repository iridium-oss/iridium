"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

export function FederatedPrivacy() {
  return (
    <section className="border-t border-surface-border bg-midnight-prussian/50 py-20 sm:py-28" id="federated">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mx-auto max-w-3xl text-center"
        >
          <span className="inline-flex items-center gap-2 rounded-full border border-surface-border bg-surface-card/80 px-4 py-1.5 text-sm text-text-secondary backdrop-blur">
            <Icon name="lock" size={18} />
            Privacy-aware architecture
          </span>
          <h2 className="mt-6 text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Federated learning and privacy-aware architecture
          </h2>
          <p className="mt-6 text-text-secondary">
            The federated learning pathway is specified in architecture and documentation: client nodes perform local updates, the server aggregates model parameters. Training can remain distributed without centralizing raw data. Flower or equivalent orchestration is planned; no federated experiments are reported in the current baseline. The design keeps raw personal data out of the central path.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
