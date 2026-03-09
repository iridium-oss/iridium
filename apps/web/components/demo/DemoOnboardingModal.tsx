"use client";

import { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

type Props = { onClose: () => void };

export function DemoOnboardingModal({ onClose }: Props) {
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-sm"
        onClick={onClose}
        role="dialog"
        aria-modal="true"
        aria-labelledby="demo-onboarding-title"
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.96 }}
          transition={{ type: "tween", duration: 0.2 }}
          className="w-full max-w-lg rounded-2xl border border-surface-border bg-midnight-prussian p-6 shadow-elevated"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex items-start justify-between gap-4">
            <h2 id="demo-onboarding-title" className="text-xl font-medium text-text-primary">
              Try IRIDIUM
            </h2>
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg p-1 text-text-muted hover:bg-surface-card hover:text-text-primary"
              aria-label="Close"
            >
              <Icon name="close" size={24} />
            </button>
          </div>
          <p className="mt-4 text-sm text-text-secondary">
            This demo uses the live API when available. You can explore route planning, congestion forecast, anomalies, equity, and the digital twin. Data status (live, unavailable, configuration required) is shown per source. No synthetic data is substituted.
          </p>
          <p className="mt-3 text-sm text-text-secondary">
            Use "Mode and scenario" to read about live, snapshot, and public demo options. Then open any module to start.
          </p>
          <div className="mt-6 flex justify-end">
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-700"
            >
              Get started
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
