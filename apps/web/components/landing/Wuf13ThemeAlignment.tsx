"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getPitchImage, getSourceLogo } from "@/lib/images";

const BLOCKS = [
  { id: "safe", title: "Safe cities", icon: "shield" as const, contribution: "Digital twin and source-status semantics give operators a single, trustworthy view of network state. No fabricated data; explicit status when sources are unavailable." },
  { id: "resilient", title: "Resilient operations", icon: "refresh" as const, contribution: "Mobility visibility, service alerts, and disruption awareness support rapid response. Anomaly detection and real-time or near-real-time state help maintain service continuity." },
  { id: "inclusive", title: "Inclusive access", icon: "accessibility" as const, contribution: "Equity analytics and district-level indicators make access gaps visible. Route planning and fare awareness support inclusive mobility discussions." },
  { id: "communities", title: "Mobility-aware communities", icon: "groups" as const, contribution: "Communities benefit from integrated transport and urban data. IRIDIUM supports planning and policy dialogue with source-backed, transparent metrics." },
  { id: "transparency", title: "Data transparency and trust", icon: "verified" as const, contribution: "Every source is labeled; every response can carry data status. Public-sector and institutional stakeholders can audit and trust outputs." },
  { id: "infrastructure", title: "Public-interest digital infrastructure", icon: "account_tree" as const, contribution: "Open-source, provenance-aware platform suitable for public-sector deployment. No synthetic substitution; designed for the challenges highlighted by WUF13." },
];

export function Wuf13ThemeAlignment() {
  const themeImg = getPitchImage("wuf13_theme_image");
  const wuf13Logo = getSourceLogo("wuf13");

  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="wuf13-theme-alignment">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        {themeImg && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12 max-w-2xl mx-auto"
          >
            <a
              href={themeImg.pageUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="block rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur"
            >
              <div className="relative aspect-video w-full bg-surface-dark">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={themeImg.imageUrl} alt={themeImg.alt} className="w-full h-full object-cover" />
              </div>
            </a>
            <div className="flex flex-wrap items-center justify-center gap-2 p-2">
              {wuf13Logo && (
                <a href={wuf13Logo.siteUrl} target="_blank" rel="noopener noreferrer" className="shrink-0" aria-label={wuf13Logo.alt}>
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={wuf13Logo.imageUrl} alt={wuf13Logo.alt} className="h-8 w-auto object-contain" />
                </a>
              )}
              <span className="text-xs text-text-muted">IRIDIUM and WUF13 theme. Source: UN-Habitat WUF13</span>
            </div>
          </motion.div>
        )}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            IRIDIUM and the WUF13 theme
          </h2>
          <p className="mt-4 text-text-secondary">
            How IRIDIUM maps to the official WUF13 theme: Housing the world: Safe and resilient cities and communities.
          </p>
        </motion.div>
        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {BLOCKS.map(({ id, title, icon, contribution }, i) => (
            <motion.div
              key={id}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-elevated text-accent-luminous">
                  <Icon name={icon} size={24} />
                </span>
                <h3 className="font-medium text-text-primary">{title}</h3>
              </div>
              <p className="mt-3 text-sm text-text-secondary">{contribution}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
