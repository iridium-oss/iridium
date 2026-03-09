"use client";

import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getFactById } from "@/lib/facts";
import { getPitchImage, getSourceLogo } from "@/lib/images";

export function Hero() {
  const combined = getFactById("combined_daily_2025");
  const stations = getFactById("metro_stations");
  const km = getFactById("metro_network_km");
  const skyline = getPitchImage("baku_skyline");
  const metroLogo = getSourceLogo("metro");
  const bakubusLogo = getSourceLogo("bakubus");
  const wuf13Logo = getSourceLogo("wuf13");
  const arxkomLogo = getSourceLogo("arxkom");

  return (
    <section className="relative overflow-hidden pt-12 pb-24 sm:pt-16 sm:pb-32" id="hero">
      <div className="absolute inset-0 bg-gradient-to-b from-midnight-electric/10 via-transparent to-transparent" aria-hidden />
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-accent-luminous/30 to-transparent" aria-hidden />
      <div className="relative mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-5 lg:gap-16">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="lg:col-span-3"
          >
            <h1 className="text-4xl font-medium tracking-tight text-text-primary sm:text-5xl lg:text-6xl">
              The operating intelligence layer for urban mobility
            </h1>
            <p className="mt-6 text-lg text-text-secondary sm:text-xl max-w-xl">
              IRIDIUM is a provenance-aware digital twin platform for Azerbaijani cities. Real-time, source-labeled city intelligence for transport operators, municipalities, and residents. No synthetic substitution. In 2026 Baku hosts WUF13; IRIDIUM is aligned with the agenda for safe and resilient cities.
            </p>
            <div className="mt-10 flex flex-col items-start gap-4 sm:flex-row">
              <Link
                href="/demo"
                className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm transition-colors hover:bg-indigo-700"
              >
                Try the demo
                <Icon name="arrow_forward" size={20} />
              </Link>
              <Link
                href="/dashboard"
                className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-6 py-3 text-base font-medium text-slate-700 transition-colors hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700"
              >
                Open dashboard
                <Icon name="dashboard" size={20} />
              </Link>
            </div>
            <div className="mt-12 flex flex-wrap gap-6 text-sm">
              {combined && (
                <div>
                  <span className="block font-medium text-text-primary">{combined.value}</span>
                  <span className="text-text-muted">daily passengers (2025)</span>
                </div>
              )}
              {stations && (
                <div>
                  <span className="block font-medium text-text-primary">{stations.value} stations</span>
                  <span className="text-text-muted">Baku Metro</span>
                </div>
              )}
              {km && (
                <div>
                  <span className="block font-medium text-text-primary">{km.value} km</span>
                  <span className="text-text-muted">metro network</span>
                </div>
              )}
            </div>
            {(wuf13Logo || arxkomLogo || bakubusLogo || metroLogo) && (
              <div className="mt-6 flex flex-wrap items-center justify-start gap-6">
                {wuf13Logo && (
                  <a href={wuf13Logo.siteUrl} target="_blank" rel="noopener noreferrer" className="opacity-80 hover:opacity-100 transition-opacity shrink-0">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={wuf13Logo.imageUrl} alt={wuf13Logo.alt} className="h-8 w-auto object-contain max-w-[100px]" />
                  </a>
                )}
                {arxkomLogo && (
                  <a href={arxkomLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="opacity-80 hover:opacity-100 transition-opacity shrink-0">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={arxkomLogo.imageUrl} alt={arxkomLogo.alt} className="h-8 w-auto object-contain max-w-[100px]" />
                  </a>
                )}
                {bakubusLogo && (
                  <a href={bakubusLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="opacity-80 hover:opacity-100 transition-opacity shrink-0">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={bakubusLogo.imageUrl} alt={bakubusLogo.alt} className="h-8 w-auto object-contain" />
                  </a>
                )}
                {metroLogo && (
                  <a href={metroLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="opacity-80 hover:opacity-100 transition-opacity shrink-0 ml-auto">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={metroLogo.imageUrl} alt={metroLogo.alt} className="h-8 w-auto object-contain" />
                  </a>
                )}
              </div>
            )}
            <div className="mt-8 flex flex-wrap items-center gap-4 text-xs text-text-muted">
              <span className="flex items-center gap-1.5">
                <Icon name="verified" size={18} className="text-accent-luminous" />
                Real data only
              </span>
              <span className="flex items-center gap-1.5">
                <Icon name="source" size={18} className="text-accent-luminous" />
                Source-backed stats
              </span>
              <a
                href={combined?.sourceUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-accent-muted hover:text-accent-luminous"
              >
                AZCON 2025 indicators
              </a>
            </div>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: 24 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.15 }}
            className="lg:col-span-2 flex flex-col rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur"
          >
            {skyline && (
              <a
                href={skyline.pageUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="block relative aspect-[4/3] w-full shrink-0 bg-surface-dark"
              >
                <Image
                  src={skyline.imageUrl}
                  alt={skyline.alt}
                  fill
                  className="object-cover"
                  sizes="(max-width: 1024px) 100vw, 40vw"
                />
              </a>
            )}
            <div className="p-6">
              <h3 className="font-medium text-text-primary">Why this matters now</h3>
              <p className="mt-2 text-sm text-text-secondary">
                Baku and Guba already rely on real-time weather and transit-aware data. Cities need a single, trustworthy layer that unifies operators and surfaces every source with explicit provenance.
              </p>
              <ul className="mt-4 space-y-2 text-sm text-text-secondary">
                <li className="flex items-center gap-2">
                  <Icon name="check_circle" size={18} className="shrink-0 text-accent-luminous" />
                  Digital twin from real sources only
                </li>
                <li className="flex items-center gap-2">
                  <Icon name="check_circle" size={18} className="shrink-0 text-accent-luminous" />
                  Explicit data status per provider
                </li>
                <li className="flex items-center gap-2">
                  <Icon name="check_circle" size={18} className="shrink-0 text-accent-luminous" />
                  No fabricated feeds or benchmarks
                </li>
              </ul>
              {skyline && (
                <p className="mt-3 text-xs text-text-muted">
                  Image: <a href={skyline.pageUrl} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">Wikimedia Commons</a>
                </p>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
