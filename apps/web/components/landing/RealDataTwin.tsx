"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

export function RealDataTwin() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="real-data">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <motion.div
            initial={{ opacity: 0, x: -12 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
              Real data and digital twin layer
            </h2>
            <p className="mt-6 text-text-secondary">
              The digital twin is assembled only from configured, live sources. Every external source is documented with acquisition method, access type, and refresh cadence. When a source is unavailable or unconfigured, the system returns an explicit data status (live, unavailable, configuration required, permission required) rather than substituting synthetic data.
            </p>
            <ul className="mt-6 space-y-3 text-text-secondary">
              <li className="flex items-start gap-2">
                <Icon name="check_circle" size={20} className="shrink-0 text-accent-luminous" />
                <span>OpenStreetMap-based network ingestion with provenance in manifest</span>
              </li>
              <li className="flex items-start gap-2">
                <Icon name="check_circle" size={20} className="shrink-0 text-accent-luminous" />
                <span>Open-Meteo weather integration for Baku and Quba</span>
              </li>
              <li className="flex items-start gap-2">
                <Icon name="check_circle" size={20} className="shrink-0 text-accent-luminous" />
                <span>Provider abstraction for traffic and transit; status per source</span>
              </li>
            </ul>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: 12 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="rounded-xl border border-surface-border bg-surface-card/80 p-8 backdrop-blur"
          >
            <h3 className="font-medium text-text-primary">Source status semantics</h3>
            <p className="mt-2 text-sm text-text-secondary">
              API and UI expose data status per source so the platform can be evaluated and extended without pretending unavailable sources are present.
            </p>
            <div className="mt-6 flex flex-wrap gap-2">
              {["live", "unavailable", "configuration_required", "permission_required"].map((s) => (
                <span key={s} className="rounded-md border border-surface-border bg-surface-dark px-3 py-1.5 text-xs font-medium text-text-secondary">
                  {s}
                </span>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
