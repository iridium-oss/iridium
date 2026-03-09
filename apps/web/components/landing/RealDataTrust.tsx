"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const SOURCE_TYPES = [
  { icon: "verified" as const, title: "Official data", text: "Baku Metro official site, Ministry tariff announcements, BakuBus official pages. Used for fares, network structure, and operator profile. Source label and URL are stored and displayed." },
  { icon: "public" as const, title: "Public-web observed data", text: "When we use observed data (e.g. from public transport or metro pages), it is never presented as official operator or GTFS data. Provenance is explicit; source_status reflects the acquisition method." },
  { icon: "handshake" as const, title: "Licensed partner data", text: "When partner or third-party feeds are integrated under license, they are documented and labeled. No assumption of universal availability." },
  { icon: "lock" as const, title: "Unavailable or permission-required", text: "Baku Metro and BakuBus operator GTFS are marked permission_required until an official or authorised feed is provided. The system does not substitute synthetic GTFS." },
  { icon: "block" as const, title: "No synthetic substitution", text: "In the main runtime path, IRIDIUM never fills missing data with synthetic or fabricated feeds. When a source is unavailable, the API and UI show explicit status so stakeholders can assess reliability." },
];

export function RealDataTrust() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="real-data-trust">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Real data, explicit provenance
          </h2>
          <p className="mt-4 text-text-secondary">
            Trusted by design. Every source type is documented; every response can carry a data status. IRIDIUM refuses synthetic substitution in the main path.
          </p>
        </motion.div>
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {SOURCE_TYPES.slice(0, 4).map(({ icon, title, text }, i) => (
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
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-8 rounded-xl border-2 border-accent-luminous/30 bg-accent-glow/20 p-8"
        >
          <div className="flex items-start gap-4">
            <Icon name="block" size={28} className="shrink-0 text-accent-luminous" />
            <div>
              <h3 className="font-medium text-text-primary">No synthetic substitution</h3>
              <p className="mt-2 text-text-secondary">
                In the main runtime path, IRIDIUM never fills missing data with synthetic or fabricated feeds. When a source is unavailable, the API and UI show explicit status so stakeholders can assess reliability. This is one of the strongest differentiators for public-sector and operator use.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
