"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const DRIVERS = [
  {
    icon: "apartment" as const,
    title: "Growing urban complexity",
    text: "Cities manage more modes, more operators, and higher expectations for reliability and equity. Single-operator or single-dashboard views are no longer enough.",
  },
  {
    icon: "hub" as const,
    title: "Fragmented mobility systems",
    text: "Transit, traffic, weather, and events live in separate systems. Combining them without a clear provenance model leads to opaque or untrusted insights.",
  },
  {
    icon: "payments" as const,
    title: "Cashless and digital transport",
    text: "Official tariff and cashless payment adoption (e.g. BakıKART, qualifying bus routes) increase the need for fare-aware routing and transparent policy representation.",
  },
  {
    icon: "schedule" as const,
    title: "Real-time journey intelligence",
    text: "Riders and operators expect real-time or near-real-time visibility. Systems that hide data status or substitute synthetic data undermine trust.",
  },
  {
    icon: "verified" as const,
    title: "Transparent public-service data",
    text: "Municipalities and regulators need systems that distinguish official data, observed data, and unavailable data. IRIDIUM is designed for that from the ground up.",
  },
  {
    icon: "psychology" as const,
    title: "Mature geospatial and AI infrastructure",
    text: "OpenStreetMap, Open-Meteo, GTFS-style models, and federated learning frameworks are mature enough to build a real-data-first platform without synthetic fallbacks.",
  },
];

export function WhyNow() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="why-now">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Why now
          </h2>
          <p className="mt-4 text-text-secondary">
            The convergence of urban complexity, fragmented data, and mature infrastructure makes a provenance-aware urban mobility platform both necessary and feasible. In 2026 Baku hosts WUF13; the timing is urgent and the city is globally relevant for the urban agenda.
          </p>
        </motion.div>
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {DRIVERS.map(({ icon, title, text }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-midnight-electric/20 text-accent-luminous">
                  <Icon name={icon} size={24} />
                </span>
                <h3 className="text-lg font-medium text-text-primary">{title}</h3>
              </div>
              <p className="mt-3 text-sm text-text-secondary">{text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
