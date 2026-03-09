"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const ACTIONS = [
  { href: "/demo", label: "Try the demo", icon: "play_arrow" as const },
  { href: "/architecture", label: "Explore the architecture", icon: "account_tree" as const },
  { href: "/dashboard/provenance", label: "Inspect data provenance", icon: "source" as const },
  { href: "https://github.com/iridium-oss/iridium/tree/main/docs", label: "Read the documentation", icon: "menu_book" as const },
  { href: "https://github.com/iridium-oss/iridium", label: "Review the repository", icon: "code" as const },
];

export function DemoCta() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="demo-cta">
      <div className="mx-auto max-w-wide px-4 text-center sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Try IRIDIUM
          </h2>
          <p className="mt-4 max-w-2xl mx-auto text-text-secondary">
            Use the live demo to explore the digital twin, run route planning, view forecasts, and inspect data source status. No synthetic substitution; you see real API behavior and provenance.
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/demo"
              className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-8 py-4 text-base font-medium text-white shadow-sm transition-colors hover:bg-indigo-700"
            >
              Launch demo
              <Icon name="play_arrow" size={24} />
            </Link>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-6 py-3 text-base font-medium text-slate-700 transition-colors hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700"
            >
              Open dashboard
              <Icon name="dashboard" size={20} />
            </Link>
          </div>
          <div className="mt-12 flex flex-wrap justify-center gap-4">
            {ACTIONS.filter((a) => a.href.startsWith("/")).map(({ href, label, icon }) => (
              <Link
                key={href}
                href={href}
                className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700"
              >
                <Icon name={icon} size={18} />
                {label}
              </Link>
            ))}
            {ACTIONS.filter((a) => !a.href.startsWith("/")).map(({ href, label, icon }) => (
              <a
                key={href}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 transition-colors hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700"
              >
                <Icon name={icon} size={18} />
                {label}
              </a>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
