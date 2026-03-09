"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getPitchImage } from "@/lib/images";

export function Wuf13CtaSection() {
  const skylineAlt = getPitchImage("baku_skyline_alt");

  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="wuf13-cta">
      <div className="mx-auto max-w-wide px-4 text-center sm:px-6 lg:px-8">
        {skylineAlt && (
          <motion.a
            href={skylineAlt.pageUrl}
            target="_blank"
            rel="noopener noreferrer"
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12 block rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur max-w-4xl mx-auto"
          >
            <div className="relative aspect-[2/1] w-full bg-surface-dark">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={skylineAlt.imageUrl} alt={skylineAlt.alt} className="w-full h-full object-cover" />
            </div>
            <p className="p-2 text-xs text-text-muted">Baku. Source: <a href={skylineAlt.pageUrl} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">Wikimedia Commons</a></p>
          </motion.a>
        )}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            For dialogue, demo, and showcase
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-text-secondary">
            IRIDIUM is designed for the urban challenges highlighted by WUF13. Relevant to the policy and systems questions raised by the Forum. Suitable for discussion, demonstration, and collaboration in the WUF13 context. We do not claim selection for WUF13 or the Urban Expo unless explicitly stated.
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/demo"
              className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm transition-colors hover:bg-indigo-700"
            >
              Try the demo
              <Icon name="arrow_forward" size={20} />
            </Link>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card px-6 py-3 text-base font-medium text-text-primary hover:bg-surface-elevated"
            >
              Explore the platform
              <Icon name="dashboard" size={20} />
            </Link>
          </div>
          <p className="mt-6 text-sm text-text-muted">
            Urban innovation dialogue, public-interest technology, academic and technical presentation. Aligned with WUF13 themes; no official endorsement implied.
          </p>
        </motion.div>
      </div>
    </section>
  );
}
