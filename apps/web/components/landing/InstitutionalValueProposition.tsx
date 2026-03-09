"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const POINTS = [
  { icon: "visibility" as const, title: "Operational visibility", text: "Single pane for network state, transit status, and alerts. Source per provider so institutions know what is live and what is not." },
  { icon: "map" as const, title: "Planning support", text: "Equity analytics and network metrics support long-term planning. Methodology is documented; no synthetic scores." },
  { icon: "source" as const, title: "Source transparency", text: "Every figure and status can be traced to a documented source. Suitable for audit and accountability." },
  { icon: "verified" as const, title: "Trust and accountability", text: "When data is partial or unavailable, the system says so. No fabricated feeds that could mislead decisions." },
  { icon: "trending_up" as const, title: "Mobility service improvement", text: "Routing, forecasting, and anomaly intelligence support service quality. Degradation behavior is explicit." },
  { icon: "help" as const, title: "Decision support under partial data", text: "Institutions can use the platform even when some sources are permission_required or unavailable. Status semantics make gaps clear." },
];

export function InstitutionalValueProposition() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="institutional-value">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Institutional value proposition
          </h2>
          <p className="mt-4 text-text-secondary">
            For public institutions and operator stakeholders: operational visibility, planning support, source transparency, and trust under partial data availability. Useful for city and public-transport stakeholders operating in the context of WUF13 themes (safe and resilient cities). Aligned with safe and resilient city objectives; relevant to housing, access, and service reliability discussions and to public-sector digital coordination. The commercial architecture (platform subscriptions, deployment options, services) is set out in the Business model and Deployment model sections. We do not imply official institutional procurement or deployment unless proven.
          </p>
        </motion.div>
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {POINTS.map(({ icon, title, text }, i) => (
            <motion.div
              key={title}
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
                <h3 className="text-lg font-medium text-text-primary">{title}</h3>
              </div>
              <p className="mt-3 text-sm text-text-secondary">{text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
