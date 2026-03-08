"use client";

import { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

type Props = { onClose: () => void };

const MODES = [
  { id: "live", title: "Live data mode", desc: "API uses configured sources. Network, weather, and optional traffic/transit when available." },
  { id: "snapshot", title: "Recorded real snapshot", desc: "When supported, a pre-recorded real snapshot can be loaded for reproducible demos." },
  { id: "public", title: "Public demo mode", desc: "Open-Meteo and OSM-based network (when imported) are public. Other sources show configuration or permission status." },
];

export function DemoModeModal({ onClose }: Props) {
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
        aria-labelledby="demo-mode-title"
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.96 }}
          className="w-full max-w-lg rounded-2xl border border-surface-border bg-midnight-prussian p-6 shadow-elevated"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex items-start justify-between gap-4">
            <h2 id="demo-mode-title" className="text-xl font-medium text-text-primary">
              Mode and scenario
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
            The current session uses the API in its default configuration. Below is how modes are defined in the system.
          </p>
          <ul className="mt-6 space-y-4">
            {MODES.map((m) => (
              <li key={m.id} className="rounded-xl border border-surface-border bg-surface-card/60 p-4">
                <h3 className="font-medium text-text-primary">{m.title}</h3>
                <p className="mt-1 text-sm text-text-secondary">{m.desc}</p>
              </li>
            ))}
          </ul>
          <div className="mt-6 flex justify-end">
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg bg-midnight-electric px-4 py-2.5 text-sm font-medium text-white hover:opacity-90"
            >
              Close
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
