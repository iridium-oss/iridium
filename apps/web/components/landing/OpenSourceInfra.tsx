"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

export function OpenSourceInfra() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="opensource">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Open source and infrastructure
          </h2>
          <p className="mt-6 text-text-secondary">
            IRIDIUM is developed in the open. The repository includes the API (FastAPI), network-import service, digital-twin state assembler, weather and traffic provider abstractions, forecasting and routing modules, equity and anomaly pipelines, and this web frontend. Docker Compose and documentation support local deployment. No production or regulatory certification is claimed; deployers must conduct their own assessment.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <a
              href="https://github.com/iridium-oss/iridium"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card px-4 py-2 text-sm font-medium text-text-primary hover:bg-surface-elevated"
            >
              <Icon name="code" size={20} />
              GitHub
            </a>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
