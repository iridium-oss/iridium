"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

export function ResearchPublication() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="research">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="flex flex-col gap-8 sm:flex-row sm:items-center sm:justify-between"
        >
          <div>
            <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
              Research and publication readiness
            </h2>
            <p className="mt-4 max-w-2xl text-text-secondary">
              The project includes an academic manuscript (IEEE-style) framing IRIDIUM as a provenance-aware real-data baseline. Preprint packaging and citation metadata are maintained in the repository.
            </p>
          </div>
          <a
            href="https://github.com/iridium-oss/iridium"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card px-5 py-2.5 text-sm font-medium text-text-primary hover:bg-surface-elevated"
          >
            <Icon name="menu_book" size={20} />
            Paper and citation
          </a>
        </motion.div>
      </div>
    </section>
  );
}
