"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const DIMENSIONS = [
  "Provenance-aware source labeling",
  "Real-data-first architecture",
  "Modular digital twin",
  "Public transport + urban operations view",
  "Equity-aware analytics",
  "Transparent degraded-mode behavior",
  "Open-source posture",
  "Deployment flexibility",
];

const CATEGORIES = [
  { name: "Municipal dashboards", note: "Often single-operator or single-vendor. Source labeling and multi-source unification vary." },
  { name: "Generic map and routing products", note: "Consumer-focused. May not expose source status or partial-data behavior. Compared with typical category behavior." },
  { name: "Operator-specific systems", note: "Deep for one operator; less unified across metro, bus, and city. Compared with typical category behavior." },
  { name: "Research prototypes", note: "Often synthetic or offline datasets; less emphasis on production source semantics. Compared with typical category behavior." },
  { name: "IRIDIUM", note: "Provenance-aware, real-data-first, modular twin, public transport and urban view, equity analytics, explicit degradation, open-source, flexible deployment." },
];

export function CompetitiveLandscape() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="competitive-landscape">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Competitive landscape
          </h2>
          <p className="mt-4 text-text-secondary">
            Framed as categories, not hostile comparisons. We do not make unsupported claims about competitors. Where exact proof is unavailable, we use compared with typical category behavior.
          </p>
        </motion.div>
        <div className="mt-14 overflow-x-auto">
          <div className="min-w-[600px] rounded-xl border border-surface-border bg-surface-card/60 p-6">
            <h3 className="font-medium text-text-primary mb-4">Comparison dimensions</h3>
            <ul className="space-y-2 text-sm text-text-secondary">
              {DIMENSIONS.map((d) => (
                <li key={d} className="flex items-center gap-2">
                  <Icon name="check_circle" size={18} className="shrink-0 text-accent-luminous" />
                  {d}
                </li>
              ))}
            </ul>
            <h3 className="font-medium text-text-primary mt-8 mb-4">Categories</h3>
            <div className="space-y-4">
              {CATEGORIES.map(({ name, note }) => (
                <div key={name} className="rounded-lg border border-surface-border bg-white p-4">
                  <span className="font-medium text-text-primary">{name}</span>
                  <p className="mt-1 text-sm text-text-muted">{note}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
