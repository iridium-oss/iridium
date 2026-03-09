"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const PROOF_POINTS = [
  { icon: "code" as const, title: "Repository maturity", text: "Structured monorepo: API, transit-ingestion, routing, weather, frontend. CI, lint, docs workflows. No fabricated benchmarks." },
  { icon: "play_arrow" as const, title: "Working demo", text: "Live demo and dashboard. Real API behavior; no synthetic substitution in main path." },
  { icon: "link" as const, title: "Real-data integrations", text: "Open-Meteo weather for Baku and Guba. Baku Metro static network; BakuBus AYNA API. Source status per provider." },
  { icon: "source" as const, title: "Source-backed architecture", text: "Provider registry, provenance on fetch, source_status in responses. Documented in docs and API." },
  { icon: "cloud" as const, title: "Live weather integration", text: "Open-Meteo live when API is reachable. Unavailable on failure; no fake weather." },
  { icon: "directions_bus" as const, title: "Transit source integration", text: "Baku Metro (official site) and BakuBus (AYNA). GTFS builder for repo-generated feed. Permission_required where operator feed not yet provided." },
  { icon: "menu_book" as const, title: "Research paper and preprint readiness", text: "Academic manuscript (IEEE-style). Preprint packaging and citation metadata in repository." },
  { icon: "tag" as const, title: "Zenodo DOI", text: "Software citation via Zenodo. DOI and version documented." },
  { icon: "folder_open" as const, title: "Open-source structure", text: "EUPL-1.2. Code, schemas, and docs in the open. No production certification claimed." },
  { icon: "description" as const, title: "Documentation depth", text: "Architecture, data provenance, operator integration, real-data mode, and baseline docs. Reviewer and contributor guides." },
  { icon: "settings" as const, title: "Demo mode", text: "Demo scenario and onboarding. Honest about scope and limitations." },
  { icon: "grid_view" as const, title: "Operational provider matrix", text: "Provider matrix and refresh policy documented. Source priority and status semantics explicit." },
];

export function Traction() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="traction">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Traction and proof points
          </h2>
          <p className="mt-4 text-text-secondary">
            Only real proof points. No users, revenue, installs, contracts, pilot customers, or waitlists invented. Technical, product, research, and execution traction.
          </p>
        </motion.div>
        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {PROOF_POINTS.map(({ icon, title, text }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: Math.min(i * 0.03, 0.3) }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-midnight-electric/20 text-accent-luminous">
                  <Icon name={icon} size={24} />
                </span>
                <h3 className="text-base font-medium text-text-primary">{title}</h3>
              </div>
              <p className="mt-2 text-sm text-text-secondary">{text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
