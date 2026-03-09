"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getPitchImage } from "@/lib/images";

export function Vision() {
  const skylineAlt = getPitchImage("baku_skyline_alt");

  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="vision">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-5 lg:gap-16">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="lg:col-span-3"
          >
            <span className="inline-flex items-center gap-2 rounded-full border border-surface-border bg-surface-card/80 px-4 py-1.5 text-sm text-text-secondary backdrop-blur">
              <Icon name="visibility" size={18} />
              Vision
            </span>
            <h2 className="mt-6 text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
              The operating intelligence layer for urban mobility
            </h2>
            <p className="mt-6 text-text-secondary">
              IRIDIUM is built to become the real-time, provenance-aware intelligence layer that cities and operators use to see the full picture of mobility: digital twin assembly, trustworthy analytics, and public-interest mobility intelligence. Every source is labeled; every response carries a data status.
            </p>
            <p className="mt-4 text-text-secondary">
              The long-term vision starts with Azerbaijani cities: Baku and Guba as the first deployment context, with expansion to other cities as the platform proves value. Baku hosts the World Urban Forum 13 (WUF13) in May 2026; the global agenda for safe and resilient cities makes this moment especially relevant. The same architecture supports regional and institutional deployment where data sovereignty and source transparency are non-negotiable.
            </p>
            <div className="mt-8 rounded-xl border border-surface-border bg-surface-card/60 p-6">
              <h3 className="font-medium text-text-primary">What we mean by operating intelligence</h3>
              <ul className="mt-4 space-y-2 text-sm text-text-secondary">
                <li className="flex items-start gap-2">
                  <Icon name="account_tree" size={20} className="shrink-0 text-accent-luminous mt-0.5" />
                  Digital twin assembled only from configured, real sources
                </li>
                <li className="flex items-start gap-2">
                  <Icon name="verified" size={20} className="shrink-0 text-accent-luminous mt-0.5" />
                  Transparent source-status semantics so stakeholders know what is live, partial, or unavailable
                </li>
                <li className="flex items-start gap-2">
                  <Icon name="public" size={20} className="shrink-0 text-accent-luminous mt-0.5" />
                  Public-interest mobility intelligence suitable for planners and operators
                </li>
              </ul>
            </div>
          </motion.div>
          {skylineAlt && (
            <motion.div
              initial={{ opacity: 0, x: 24 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="lg:col-span-2"
            >
              <a
                href={skylineAlt.pageUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="block rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur hover:border-accent-muted/50 transition-colors"
              >
                <div className="relative aspect-[4/3] w-full bg-surface-dark">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={skylineAlt.imageUrl}
                    alt={skylineAlt.alt}
                    className="w-full h-full object-cover"
                  />
                </div>
                <p className="p-3 text-xs text-text-muted">
                  Baku. Source: <a href={skylineAlt.pageUrl} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">Wikimedia Commons</a>
                </p>
              </a>
            </motion.div>
          )}
        </div>
      </div>
    </section>
  );
}
