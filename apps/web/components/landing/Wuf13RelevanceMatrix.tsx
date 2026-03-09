"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const ROWS = [
  { priority: "Resilient urban operations", why: "Cities need visibility into network state and disruptions.", capability: "Digital twin, anomaly detection, source-status semantics.", maturity: "Implemented.", source: "Repository and docs." },
  { priority: "Mobility access", why: "Equitable access depends on service visibility and planning.", capability: "Route planning, equity analytics, fare awareness.", maturity: "Baseline implemented.", source: "Real-data integrations." },
  { priority: "Service transparency", why: "Stakeholders must know what data is live and what is not.", capability: "Provenance on every boundary; no synthetic substitution.", maturity: "Implemented.", source: "API and provider matrix." },
  { priority: "Transport disruption awareness", why: "Rapid response requires alerts and operational context.", capability: "Anomaly pipeline, provider alerts, degraded-mode semantics.", maturity: "Implemented.", source: "Transit and alert providers." },
  { priority: "Urban data integration", why: "Fragmented systems undermine safe and resilient cities.", capability: "Unified metro, bus, weather; optional traffic.", maturity: "Baku Metro and BakuBus integrated.", source: "Official and public APIs." },
  { priority: "Inclusive city intelligence", why: "Policy needs district-level and equity-aware metrics.", capability: "Mobility Equity Score, configurable indicators.", maturity: "Implemented when data path set.", source: "Methodology docs." },
  { priority: "Public-interest digital infrastructure", why: "WUF13 theme implies trustworthy, auditable systems.", capability: "Open-source, source-labeled, deployment flexibility.", maturity: "Repository and documentation.", source: "EUPL-1.2; docs." },
];

export function Wuf13RelevanceMatrix() {
  return (
    <section className="border-t border-surface-border bg-midnight-prussian/50 py-20 sm:py-28" id="wuf13-relevance-matrix">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            WUF13 relevance matrix
          </h2>
          <p className="mt-4 text-text-secondary">
            How WUF13 urban priorities map to IRIDIUM capabilities. Source-linked where applicable; maturity stated honestly.
          </p>
        </motion.div>
        <div className="mt-14 overflow-x-auto">
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="min-w-[700px] rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur"
          >
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-surface-border bg-surface-dark/80">
                  <th className="p-4 font-medium text-text-primary">WUF13 urban priority</th>
                  <th className="p-4 font-medium text-text-primary">Why it matters</th>
                  <th className="p-4 font-medium text-text-primary">IRIDIUM capability</th>
                  <th className="p-4 font-medium text-text-primary">Current maturity</th>
                  <th className="p-4 font-medium text-text-primary">Source or proof point</th>
                </tr>
              </thead>
              <tbody>
                {ROWS.map((row, i) => (
                  <tr key={row.priority} className="border-b border-surface-border last:border-0">
                    <td className="p-4 text-text-primary">{row.priority}</td>
                    <td className="p-4 text-text-secondary">{row.why}</td>
                    <td className="p-4 text-text-secondary">{row.capability}</td>
                    <td className="p-4 text-text-muted">{row.maturity}</td>
                    <td className="p-4 text-text-muted">{row.source}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
