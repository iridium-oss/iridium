"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getWuf13FactById } from "@/lib/wuf13-facts";
import { getPitchImage } from "@/lib/images";

const TIMELINE = [
  { id: "campaign", label: "Azerbaijan Urban Campaign 2026", detail: "Launched in preparation for WUF13; mobility among focus areas.", factId: "azerbaijan_urban_campaign" },
  { id: "year", label: "Year of Urban Planning and Architecture", detail: "2026 framed in Azerbaijan as the Year of Urban Planning and Architecture.", factId: "year_urban_planning" },
  { id: "wuf13", label: "WUF13 in Baku", detail: "17 to 22 May 2026. Theme: Housing the world: Safe and resilient cities and communities.", factId: "wuf13_dates" },
  { id: "iridium", label: "IRIDIUM in this context", detail: "A mobility intelligence layer aligned with safe and resilient city objectives; relevant for dialogue, demo, and urban innovation discussion.", factId: null },
];

export function RoadToWuf13() {
  const busImg = getPitchImage("baku_bus");

  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="road-to-wuf13">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        {busImg && (
          <motion.a
            href={busImg.pageUrl}
            target="_blank"
            rel="noopener noreferrer"
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12 block rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur"
          >
            <div className="relative aspect-[3/1] w-full bg-surface-dark">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={busImg.imageUrl} alt={busImg.alt} className="w-full h-full object-cover" />
            </div>
            <p className="p-2 text-center text-xs text-text-muted">Baku transport. Source: Wikimedia Commons</p>
          </motion.a>
        )}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Road to WUF13
          </h2>
          <p className="mt-4 text-text-secondary">
            Baku 2026 and the urban agenda. A concise timeline of context and relevance.
          </p>
        </motion.div>
        <div className="mt-14 space-y-4">
          {TIMELINE.map(({ id, label, detail, factId }, i) => {
            const fact = factId ? getWuf13FactById(factId) : null;
            return (
              <motion.div
                key={id}
                initial={{ opacity: 0, x: -12 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.06 }}
                className="flex gap-6 rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur sm:gap-8"
              >
                <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-midnight-electric/20 text-lg font-medium text-accent-luminous">
                  {i + 1}
                </span>
                <div className="min-w-0">
                  <h3 className="font-medium text-text-primary">{label}</h3>
                  <p className="mt-2 text-sm text-text-secondary">{detail}</p>
                  {fact && (
                    <a href={fact.sourceUrl} target="_blank" rel="noopener noreferrer" className="mt-2 inline-block text-xs text-accent-muted hover:text-accent-luminous">
                      Source: {fact.sourceName}
                    </a>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
