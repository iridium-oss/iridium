"use client";

import { motion } from "framer-motion";
import { PITCH_FACTS, getFactsByCategory } from "@/lib/facts";
import { getPitchImage, getSourceLogo } from "@/lib/images";

function StatCard({
  value,
  label,
  sourceName,
  sourceUrl,
  isConditional,
}: {
  value: string;
  label: string;
  sourceName: string;
  sourceUrl: string;
  isConditional?: boolean;
}) {
  return (
    <motion.a
      href={sourceUrl}
      target="_blank"
      rel="noopener noreferrer"
      initial={{ opacity: 0, y: 8 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="block rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur hover:border-accent-muted/50 transition-colors"
    >
      <span className="block text-2xl sm:text-3xl font-medium text-text-primary">{value}</span>
      <span className="mt-1 block text-sm text-text-secondary">{label}</span>
      {isConditional && (
        <span className="mt-2 inline-block text-xs text-text-muted">Qualifying routes only; see source.</span>
      )}
      <span className="mt-2 block text-xs text-text-muted">Source: {sourceName}</span>
    </motion.a>
  );
}

export function UrbanMobilityByNumbers() {
  const network = getFactsByCategory("network");
  const fare = getFactsByCategory("fare").filter((f) => !f.isConditional);
  const fareConditional = PITCH_FACTS.filter((f) => f.id === "bus_fare_conditional");
  const ridership = getFactsByCategory("ridership");
  const h1 = PITCH_FACTS.find((f) => f.id === "h1_fare");
  const urban = getFactsByCategory("context");
  const metroImg = getPitchImage("baku_metro");
  const busImg = getPitchImage("baku_bus");
  const metroLogo = getSourceLogo("metro");
  const bakubusLogo = getSourceLogo("bakubus");
  const wuf13Logo = getSourceLogo("wuf13");

  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="urban-mobility-numbers">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Urban mobility by the numbers
          </h2>
          <p className="mt-4 text-text-secondary">
            Source-backed figures for Baku Metro, BakuBus, and Azerbaijan context. Every value links to its official or cited source.
          </p>
        </motion.div>

        {(metroLogo || bakubusLogo || wuf13Logo) && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mt-8 flex flex-wrap items-center justify-center gap-8"
          >
            {metroLogo && (
              <a href={metroLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="opacity-80 hover:opacity-100 transition-opacity">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={metroLogo.imageUrl} alt={metroLogo.alt} className="h-12 w-auto max-w-[120px] object-contain" />
              </a>
            )}
            {bakubusLogo && (
              <a href={bakubusLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="opacity-80 hover:opacity-100 transition-opacity">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={bakubusLogo.imageUrl} alt={bakubusLogo.alt} className="h-12 w-auto max-w-[120px] object-contain" />
              </a>
            )}
            {wuf13Logo && (
              <a href={wuf13Logo.siteUrl} target="_blank" rel="noopener noreferrer" className="opacity-80 hover:opacity-100 transition-opacity">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={wuf13Logo.imageUrl} alt={wuf13Logo.alt} className="h-12 w-auto max-w-[140px] object-contain" />
              </a>
            )}
          </motion.div>
        )}

        {(metroImg || busImg) && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mt-12 grid gap-6 sm:grid-cols-2"
          >
            {metroImg && (
              <a
                href={metroImg.pageUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="block rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur hover:border-accent-muted/50 transition-colors"
              >
                <div className="relative aspect-[16/10] w-full bg-surface-dark">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={metroImg.imageUrl}
                    alt={metroImg.alt}
                    className="w-full h-full object-cover"
                  />
                </div>
                <p className="p-3 text-xs text-text-muted">
                  Baku Metro. Source: <a href="https://metro.gov.az" target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">metro.gov.az</a>
                </p>
              </a>
            )}
            {busImg && (
              <a
                href={busImg.pageUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="block rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur hover:border-accent-muted/50 transition-colors"
              >
                <div className="relative aspect-[16/10] w-full bg-surface-dark">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={busImg.imageUrl}
                    alt={busImg.alt}
                    className="w-full h-full object-cover"
                  />
                </div>
                <p className="p-3 text-xs text-text-muted">
                  Baku bus. Source: <span className="text-accent-muted">Wikimedia Commons</span>
                </p>
              </a>
            )}
          </motion.div>
        )}

        <div className="mt-14 space-y-10">
          <div>
            <h3 className="text-sm font-medium text-text-muted uppercase tracking-wider">Network</h3>
            <div className="mt-4 grid gap-4 sm:grid-cols-3">
              {network.map((f) => (
                <StatCard
                  key={f.id}
                  value={f.value}
                  label={f.label}
                  sourceName={f.sourceName}
                  sourceUrl={f.sourceUrl}
                />
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-text-muted uppercase tracking-wider">Fares</h3>
            <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {fare.map((f) => (
                <StatCard
                  key={f.id}
                  value={f.value}
                  label={f.displayContext}
                  sourceName={f.sourceName}
                  sourceUrl={f.sourceUrl}
                />
              ))}
              {h1 && (
                <StatCard
                  value={h1.value}
                  label={h1.displayContext}
                  sourceName={h1.sourceName}
                  sourceUrl={h1.sourceUrl}
                />
              )}
              {fareConditional.map((f) => (
                <StatCard
                  key={f.id}
                  value={f.value}
                  label="Bus (qualifying cashless modern routes)"
                  sourceName={f.sourceName}
                  sourceUrl={f.sourceUrl}
                  isConditional
                />
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-text-muted uppercase tracking-wider">2025 ridership (AZCON Holding)</h3>
            <div className="mt-4 grid gap-4 sm:grid-cols-3">
              {ridership.map((f) => (
                <StatCard
                  key={f.id}
                  value={f.value}
                  label={f.displayContext}
                  sourceName={f.sourceName}
                  sourceUrl={f.sourceUrl}
                />
              ))}
            </div>
          </div>

          {urban.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-text-muted uppercase tracking-wider">Context</h3>
              <div className="mt-4 grid gap-4 sm:grid-cols-1">
                <StatCard
                  value={urban[0].value}
                  label={urban[0].displayContext}
                  sourceName={urban[0].sourceName}
                  sourceUrl={urban[0].sourceUrl}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
