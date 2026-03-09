"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const TEAM = [
  { name: "Olaf Yunus Laitinen Imanov", role: "AI Engineer", focus: "Digital twin, forecasting, and ML pipeline." },
  { name: "Amina Sadiqzade", role: "Frontend Developer", focus: "Web dashboard, landing, and UX." },
  { name: "Malahat Ismayilova", role: "AI Engineer", focus: "Anomaly detection and data pipelines." },
  { name: "Aslan Ibadullayev", role: "Fullstack Developer", focus: "API, transit ingestion, and backend." },
  { name: "Fidan Bagirova", role: "AI Engineer", focus: "Equity analytics and methodology." },
];

export function Team() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="team">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Team
          </h2>
          <p className="mt-4 text-text-secondary">
            Founding team. Roles and contribution focus. Elegant and serious presentation.
          </p>
        </motion.div>
        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {TEAM.map(({ name, role, focus }, i) => (
            <motion.div
              key={name}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6 backdrop-blur"
            >
              <div className="flex items-center gap-3">
                <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-midnight-electric/20 text-accent-luminous">
                  <Icon name="person" size={28} />
                </span>
                <div>
                  <h3 className="font-medium text-text-primary">{name}</h3>
                  <p className="text-sm text-text-muted">{role}</p>
                </div>
              </div>
              <p className="mt-4 text-sm text-text-secondary">{focus}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
