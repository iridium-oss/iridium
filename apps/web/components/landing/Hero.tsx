"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-28 pb-24 sm:pt-36 sm:pb-32">
      <div className="absolute inset-0 bg-gradient-to-b from-midnight-electric/10 via-transparent to-transparent" aria-hidden />
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-accent-luminous/30 to-transparent" aria-hidden />
      <div className="relative mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mx-auto max-w-4xl"
        >
          <h1 className="text-4xl font-medium tracking-tight text-text-primary sm:text-5xl lg:text-6xl">
            Real-time urban mobility, built on real data
          </h1>
          <p className="mt-6 text-lg text-text-secondary sm:text-xl max-w-2xl mx-auto">
            IRIDIUM is a provenance-aware platform for Azerbaijani cities. Digital twin assembly, multimodal routing, congestion forecasting, equity analytics, and anomaly detection without synthetic substitution.
          </p>
          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              href="/demo"
              className="inline-flex items-center gap-2 rounded-lg bg-midnight-electric px-6 py-3 text-base font-medium text-white shadow-glow transition-opacity hover:opacity-90"
            >
              Try IRIDIUM
              <Icon name="arrow_forward" size={20} />
            </Link>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card px-6 py-3 text-base font-medium text-text-primary backdrop-blur transition-colors hover:bg-surface-elevated"
            >
              Open dashboard
              <Icon name="dashboard" size={20} />
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
