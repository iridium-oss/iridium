"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getWuf13FactById } from "@/lib/wuf13-facts";
import { getPitchImage } from "@/lib/images";

export function Wuf13WhyIridiumSection() {
  const theme = getWuf13FactById("wuf13_theme");
  const themeImage = getPitchImage("wuf13_theme_image");

  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="wuf13-why-iridium">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        {themeImage && (
          <motion.a
            href={themeImage.pageUrl}
            target="_blank"
            rel="noopener noreferrer"
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12 block rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur"
          >
            <div className="relative aspect-[3/1] w-full bg-surface-dark">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={themeImage.imageUrl} alt={themeImage.alt} className="w-full h-full object-cover" />
            </div>
            <p className="p-2 text-center text-xs text-text-muted">IRIDIUM and the WUF13 theme. Source: UN-Habitat WUF13</p>
          </motion.a>
        )}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-3xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Why IRIDIUM matters for WUF13
          </h2>
          <p className="mt-4 text-text-secondary">
            The WUF13 theme, {theme?.value ?? "Housing the world: Safe and resilient cities and communities"}, implies practical goals that mobility intelligence can support. IRIDIUM contributes a provenance-aware urban mobility layer aligned with these priorities.
          </p>
        </motion.div>
        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {[
            { icon: "shield" as const, title: "Safe cities", text: "Safe cities require trustworthy operational mobility intelligence. IRIDIUM provides source-labeled data and explicit status so operators and planners know what is live and what is not." },
            { icon: "refresh" as const, title: "Resilient operations", text: "Resilient cities require real-time visibility, source transparency, and adaptive response. The digital twin and anomaly awareness support disruption response and service continuity." },
            { icon: "home" as const, title: "Housing and mobility", text: "Housing and communities are inseparable from mobility access, transport resilience, and urban services. IRIDIUM supports route planning, equity analytics, and service visibility." },
            { icon: "hub" as const, title: "Integrated systems", text: "Cities need integrated systems, not fragmented dashboards. IRIDIUM unifies metro, bus, weather, and network state with one provenance-aware layer." },
            { icon: "verified" as const, title: "Provenance-aware layer", text: "IRIDIUM contributes a provenance-aware urban mobility intelligence layer for safe and resilient city objectives. No synthetic substitution; every source is labeled." },
          ].map(({ icon, title, text }, i) => (
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
        <p className="mt-8 text-center text-xs text-text-muted">
          IRIDIUM is aligned with the WUF13 agenda. This is not an official endorsement or partnership with UN-Habitat or WUF13.
        </p>
      </div>
    </section>
  );
}
