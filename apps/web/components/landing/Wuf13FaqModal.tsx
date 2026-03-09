"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const FAQ_ITEMS = [
  {
    q: "What is WUF13?",
    a: "The World Urban Forum 13 (WUF13) is the leading global conference on sustainable urban development. It takes place in Baku, Azerbaijan, from 17 to 22 May 2026. The official theme is: Housing the world: Safe and resilient cities and communities. Convened by UN-Habitat and co-organized with the Government of the Republic of Azerbaijan. Registration is free. Source: wuf.unhabitat.org/wuf13.",
  },
  {
    q: "Why is WUF13 relevant to IRIDIUM?",
    a: "WUF13 sets the global agenda for safe and resilient cities. IRIDIUM is a provenance-aware urban mobility intelligence platform built for that context: real-time visibility, source transparency, and operational resilience. Our product aligns with WUF13 themes and the 2026 Baku urban agenda.",
  },
  {
    q: "Is IRIDIUM an official WUF13 product?",
    a: "No. We do not claim official endorsement, partnership, UN affiliation, WUF13 sponsorship, or selection for the Urban Expo unless the project materials explicitly state that. IRIDIUM is positioned as aligned with WUF13 themes and relevant to the dialogue, not as an official product or partner.",
  },
  {
    q: "What part of the WUF13 agenda does IRIDIUM align with?",
    a: "Safe and resilient cities require trustworthy mobility intelligence, integrated systems, and data transparency. IRIDIUM contributes a digital twin, source-status semantics, route planning, equity analytics, and disruption awareness. These support the practical goals implied by the WUF13 theme.",
  },
  {
    q: "Why does mobility intelligence matter for safe and resilient communities?",
    a: "Mobility access, service reliability, and disruption response are central to how communities function. When data is fragmented or opaque, planning and operations suffer. IRIDIUM provides a single, source-labeled layer so cities and operators can see the full picture and respond with trust.",
  },
];

export function Wuf13FaqModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [expanded, setExpanded] = useState<number | null>(null);

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
            onClick={onClose}
            aria-hidden
          />
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 16 }}
            className="fixed left-1/2 top-1/2 z-50 max-h-[85vh] w-full max-w-2xl -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-xl border border-surface-border bg-surface-card p-6 shadow-elevated"
            role="dialog"
            aria-labelledby="wuf13-faq-title"
            aria-modal="true"
          >
            <div className="flex items-start justify-between gap-4">
              <h2 id="wuf13-faq-title" className="text-lg font-medium text-text-primary">
                WUF13 and IRIDIUM: FAQ
              </h2>
              <button
                type="button"
                onClick={onClose}
                className="rounded p-1 text-text-muted hover:bg-surface-elevated hover:text-text-primary"
                aria-label="Close"
              >
                <Icon name="close" size={24} />
              </button>
            </div>
            <p className="mt-2 text-xs text-text-muted">
              Accurate, source-aware answers. No official endorsement implied.
            </p>
            <div className="mt-6 space-y-2">
              {FAQ_ITEMS.map((item, i) => (
                <div
                  key={i}
                  className="rounded-lg border border-surface-border bg-white overflow-hidden"
                >
                  <button
                    type="button"
                    onClick={() => setExpanded(expanded === i ? null : i)}
                    className="flex w-full items-center justify-between gap-4 p-4 text-left text-sm font-medium text-text-primary hover:bg-surface-elevated"
                  >
                    {item.q}
                    <Icon name={expanded === i ? "expand_less" : "expand_more"} size={24} />
                  </button>
                  {expanded === i && (
                    <motion.p
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      className="border-t border-surface-border p-4 text-sm text-text-secondary"
                    >
                      {item.a}
                    </motion.p>
                  )}
                </div>
              ))}
            </div>
            <a
              href="https://wuf.unhabitat.org/wuf13"
              target="_blank"
              rel="noopener noreferrer"
              className="mt-6 inline-flex items-center gap-2 text-sm text-accent-muted hover:text-accent-luminous"
            >
              UN-Habitat WUF13
              <Icon name="open_in_new" size={18} />
            </a>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
