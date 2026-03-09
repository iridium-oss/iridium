"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

export function MultimodalRouting() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="routing">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <motion.div
            initial={{ opacity: 0, x: -12 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
              Multimodal routing
            </h2>
            <p className="mt-6 text-text-secondary">
              Route utility minimizes a weighted combination of travel time, cost, emissions proxy, and transfer penalty. The routing service accepts origin and destination coordinates and optimization preference (time, cost, carbon). OpenTripPlanner and Valhalla integration is planned once GTFS and network data are available; the API documents that routing quality depends on twin completeness.
            </p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: 12 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="rounded-xl border border-surface-border bg-surface-card/80 p-6"
          >
            <h3 className="font-medium text-text-primary">Optimization objectives</h3>
            <ul className="mt-4 space-y-2 text-sm text-text-secondary">
              <li className="flex items-center gap-2"><Icon name="schedule" size={20} /> Time</li>
              <li className="flex items-center gap-2"><Icon name="payments" size={20} /> Cost</li>
              <li className="flex items-center gap-2"><Icon name="eco" size={20} /> Carbon</li>
              <li className="flex items-center gap-2"><Icon name="swap_horiz" size={20} /> Transfers</li>
            </ul>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
