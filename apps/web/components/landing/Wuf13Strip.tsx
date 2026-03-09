"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getWuf13FactById } from "@/lib/wuf13-facts";
import { getSourceLogo } from "@/lib/images";
import { Wuf13FaqModal } from "@/components/landing/Wuf13FaqModal";

const WUF13_SOURCE = "https://wuf.unhabitat.org/wuf13";

export function Wuf13Strip() {
  const [modalOpen, setModalOpen] = useState(false);
  const [faqOpen, setFaqOpen] = useState(false);
  const dates = getWuf13FactById("wuf13_dates");
  const theme = getWuf13FactById("wuf13_theme");
  const host = getWuf13FactById("wuf13_host");
  const wuf13Logo = getSourceLogo("wuf13");

  return (
    <>
      <section className="border-b border-surface-border bg-white" aria-label="WUF13 alignment">
        <div className="mx-auto max-w-wide px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex flex-wrap items-center gap-6 text-sm">
              {wuf13Logo && (
                <a href={wuf13Logo.siteUrl} target="_blank" rel="noopener noreferrer" className="shrink-0">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={wuf13Logo.imageUrl} alt={wuf13Logo.alt} className="h-10 w-auto object-contain" />
                </a>
              )}
              {host && (
                <span className="text-text-secondary">
                  {host.value}
                </span>
              )}
              {dates && (
                <span className="text-text-secondary">
                  {dates.value}
                </span>
              )}
              {theme && (
                <span className="max-w-xl text-text-muted italic">
                  {theme.value}
                </span>
              )}
            </div>
            <div className="flex items-center gap-3">
              <a
                href={WUF13_SOURCE}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-accent-muted hover:text-accent-luminous"
              >
                Source: UN-Habitat WUF13
              </a>
              <button
                type="button"
                onClick={() => setModalOpen(true)}
                className="inline-flex items-center gap-1.5 rounded-lg border border-surface-border bg-surface-card/80 px-3 py-1.5 text-xs font-medium text-text-secondary hover:bg-surface-elevated hover:text-text-primary"
                aria-label="Why this matters"
              >
                <Icon name="info" size={18} />
                Why this matters
              </button>
              <button
                type="button"
                onClick={() => setFaqOpen(true)}
                className="inline-flex items-center gap-1.5 rounded-lg border border-surface-border bg-surface-card/80 px-3 py-1.5 text-xs font-medium text-text-secondary hover:bg-surface-elevated hover:text-text-primary"
                aria-label="WUF13 FAQ"
              >
                <Icon name="help" size={18} />
                WUF13 FAQ
              </button>
            </div>
          </div>
          <p className="mt-2 text-xs text-text-muted">
            IRIDIUM is aligned with the WUF13 agenda and urban mobility priorities. This is not an official endorsement or partnership.
          </p>
        </div>
      </section>

      <AnimatePresence>
        {modalOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
              onClick={() => setModalOpen(false)}
              aria-hidden
            />
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 16 }}
              className="fixed left-1/2 top-1/2 z-50 w-full max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-xl border border-surface-border bg-surface-card p-6 shadow-elevated"
              role="dialog"
              aria-labelledby="wuf13-modal-title"
              aria-modal="true"
            >
              <div className="flex items-start justify-between gap-4">
                <h2 id="wuf13-modal-title" className="text-lg font-medium text-text-primary">
                  Why WUF13 matters for IRIDIUM
                </h2>
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="rounded p-1 text-text-muted hover:bg-surface-elevated hover:text-text-primary"
                  aria-label="Close"
                >
                  <Icon name="close" size={24} />
                </button>
              </div>
              <p className="mt-4 text-sm text-text-secondary">
                The World Urban Forum 13 in Baku (17 to 22 May 2026) sets the global agenda for safe and resilient cities. IRIDIUM is built for exactly that context: urban mobility intelligence, source transparency, and operational resilience. We position our work as aligned with WUF13 themes and the 2026 Baku urban agenda. We do not claim official UN or WUF13 endorsement, selection, or partnership unless explicitly stated in project materials.
              </p>
              <a
                href={WUF13_SOURCE}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 inline-flex items-center gap-2 text-sm text-accent-muted hover:text-accent-luminous"
              >
                UN-Habitat WUF13
                <Icon name="open_in_new" size={18} />
              </a>
            </motion.div>
          </>
        )}
      </AnimatePresence>
      <Wuf13FaqModal open={faqOpen} onClose={() => setFaqOpen(false)} />
    </>
  );
}
