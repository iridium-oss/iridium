"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

export function LiveDemoCta() {
  return (
    <section className="border-t border-surface-border bg-midnight-electric/20 py-20 sm:py-28" id="demo">
      <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Try IRIDIUM end-to-end
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-text-secondary">
            Use the live demo to explore the digital twin, run route planning, view forecasts, and inspect data source status. No synthetic substitution; you see real API behavior and provenance.
          </p>
          <Link
            href="/demo"
            className="mt-10 inline-flex items-center gap-2 rounded-lg bg-midnight-electric px-8 py-4 text-base font-medium text-white shadow-glow transition-opacity hover:opacity-90"
          >
            Launch demo
            <Icon name="play_arrow" size={24} />
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
