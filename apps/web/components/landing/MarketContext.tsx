"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getFactsByCategory } from "@/lib/facts";
import { getPitchImage } from "@/lib/images";
const BAKU_URBAN_MAP_PAGE = "https://arxkom.gov.az";

const TAM_SAM_SOM = {
  tam: {
    label: "TAM (Total Addressable Market)",
    value: "Urban mobility software and intelligence in Azerbaijan and adjacent region",
    basis: "58.7% urban population (World Bank); ~1.2M daily public transport riders in Baku (AZCON 2025). Extended to all cities and mobility stakeholders.",
    sourceNote: "Ridership and urban share from docs/baku-transit-statistics-baseline.md.",
  },
  sam: {
    label: "SAM (Serviceable Addressable Market)",
    value: "Baku and major Azerbaijani cities (e.g. Sumgait, Ganja, Guba)",
    basis: "Baku first; then cities where IRIDIUM can deploy with real data and operator context. Public-sector and operator software opportunity.",
    sourceNote: "Serviceable = where we can realistically offer the platform.",
  },
  som: {
    label: "SOM (Serviceable Obtainable Market)",
    value: "Pilot and first deployments in Baku; then 2 to 3 additional cities",
    basis: "Initial focus: Baku pilot narrative and operator/municipal value demonstration. Obtainable in 24 to 36 months with current go-to-market plan.",
    sourceNote: "Internal estimate; no signed contracts or revenue claimed.",
  },
};

export function MarketContext() {
  const ridership = getFactsByCategory("ridership");
  const context = getFactsByCategory("context");
  const bakuUrbanMap = getPitchImage("baku_urban_map");

  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="market-context">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Market context
          </h2>
          <p className="mt-6 text-text-secondary">
            IRIDIUM is designed for Baku and Azerbaijani cities first. Public-sector and enterprise value are distinguished from consumer app value. TAM, SAM, and SOM are framed with source-backed base numbers and clear assumptions.
          </p>
        </motion.div>
        <div className="mt-12 grid gap-8 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, x: -12 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur"
          >
            <h3 className="font-medium text-text-primary flex items-center gap-2 p-6 pb-0">
              <Icon name="location_city" size={24} />
              Baku urban mobility context
            </h3>
            {bakuUrbanMap && (
              <a
                href={BAKU_URBAN_MAP_PAGE}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 block relative aspect-video w-full bg-surface-dark"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={bakuUrbanMap.imageUrl}
                  alt={bakuUrbanMap.alt}
                  className="w-full h-full object-cover"
                />
              </a>
            )}
            <div className="p-6">
              <p className="text-sm text-text-secondary">
                Baku Metro and BakuBus form the backbone of public transport. Scale of daily usage and network size are source-backed; see Urban mobility by the numbers for exact figures.
              </p>
              <ul className="mt-6 space-y-2 text-sm text-text-secondary">
                {ridership.slice(0, 3).map((f) => (
                  <li key={f.id} className="flex justify-between gap-4">
                    <span>{f.label}</span>
                    <a href={f.sourceUrl} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous shrink-0">
                      {f.value}
                    </a>
                  </li>
                ))}
              </ul>
              {bakuUrbanMap && (
                <p className="mt-3 text-xs text-text-muted">
                  Baku urban map: <a href={BAKU_URBAN_MAP_PAGE} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">State Committee on Urban Planning (Arxkom)</a>
                </p>
              )}
            </div>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: 12 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="rounded-xl border border-surface-border bg-surface-card/80 p-8 backdrop-blur"
          >
            <h3 className="font-medium text-text-primary flex items-center gap-2">
              <Icon name="business_center" size={24} />
              Future commercial scope
            </h3>
            <p className="mt-4 text-sm text-text-secondary">
              Software platform value: subscriptions and analytics for municipalities and operators. Public-sector deployment pathway first; enterprise and partner integrations as the platform matures. We do not claim current revenue or signed pilots.
            </p>
            {context.length > 0 && (
              <p className="mt-4 text-sm text-text-secondary">
                Azerbaijan urban population share (World Bank context): {context[0].value}. See source for methodology.
              </p>
            )}
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-14 rounded-xl border border-surface-border bg-surface-card/80 p-8 backdrop-blur"
        >
          <h3 className="text-xl font-medium text-text-primary flex items-center gap-2">
            <Icon name="pie_chart" size={28} />
            Market size: TAM, SAM, SOM
          </h3>
          <p className="mt-2 text-sm text-text-muted">
            Total Addressable Market, Serviceable Addressable Market, and Serviceable Obtainable Market. Base numbers from ridership and urban share; assumptions stated.
          </p>
          <div className="mt-8 grid gap-8 sm:grid-cols-3">
            <div className="rounded-lg border border-surface-border bg-white p-6">
              <h4 className="font-medium text-accent-luminous text-sm uppercase tracking-wider">TAM</h4>
              <p className="mt-2 font-medium text-text-primary">{TAM_SAM_SOM.tam.value}</p>
              <p className="mt-2 text-sm text-text-secondary">{TAM_SAM_SOM.tam.basis}</p>
              <p className="mt-2 text-xs text-text-muted">{TAM_SAM_SOM.tam.sourceNote}</p>
            </div>
            <div className="rounded-lg border border-surface-border bg-white p-6">
              <h4 className="font-medium text-accent-luminous text-sm uppercase tracking-wider">SAM</h4>
              <p className="mt-2 font-medium text-text-primary">{TAM_SAM_SOM.sam.value}</p>
              <p className="mt-2 text-sm text-text-secondary">{TAM_SAM_SOM.sam.basis}</p>
              <p className="mt-2 text-xs text-text-muted">{TAM_SAM_SOM.sam.sourceNote}</p>
            </div>
            <div className="rounded-lg border border-surface-border bg-white p-6">
              <h4 className="font-medium text-accent-luminous text-sm uppercase tracking-wider">SOM</h4>
              <p className="mt-2 font-medium text-text-primary">{TAM_SAM_SOM.som.value}</p>
              <p className="mt-2 text-sm text-text-secondary">{TAM_SAM_SOM.som.basis}</p>
              <p className="mt-2 text-xs text-text-muted">{TAM_SAM_SOM.som.sourceNote}</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
