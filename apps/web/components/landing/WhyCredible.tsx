"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const REASONS = [
  {
    title: "Cities already buy white-label mobility platforms",
    text: "Trafi, OpenMove, O-CITY, and MyTransit offer white-label MaaS apps, back office, journey planners, and transit data APIs to cities. IRIDIUM's white-label and institutional deployment options align with this established pattern.",
  },
  {
    title: "Analytics and API access are standard monetizable layers",
    text: "Urban Sharing exposes an Analytics API and a MaaS API; MyTransit offers a Transit Data API. A modular product strategy with dashboards, analytics, and integration APIs as separate revenue surfaces is consistent with the market.",
  },
  {
    title: "On-premises and sovereign deployment are used in city technology",
    text: "Snap4City is offered both as a service and installed on site; TwinCity3D emphasizes open-source plus installation, support, training, and customization. Sovereign deployment is a real option for municipalities and regulated environments.",
  },
  {
    title: "Services revenue is common in municipal technology rollout",
    text: "Implementation, integration, training, and support are standard in public-sector software adoption. The proposed services layer reflects this; no claim is made about current delivered engagements.",
  },
  {
    title: "Grant-backed deployments are common in digital twin and mobility",
    text: "The Digital Twin Cities Centre is publicly funded by Vinnova and focuses on municipal digital twin adoption; Horizon Europe mobility projects demonstrate city mobility technologies in real urban contexts. Research and grant-supported deployment is a credible strategic pathway.",
  },
];

export function WhyCredible() {
  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="why-credible">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Why this commercial model is credible
          </h2>
          <p className="mt-4 text-text-secondary">
            Market-backed reasoning only. This section does not name revenue, customers, or contracts that IRIDIUM does not have. It explains why the commercial architecture is consistent with how urban mobility and public-sector technology are sold and deployed.
          </p>
        </motion.div>

        <div className="mt-14 space-y-6">
          {REASONS.map((item, i) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.04 }}
              className="rounded-xl border border-surface-border bg-surface-card/80 p-6"
            >
              <div className="flex gap-4">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-midnight-electric/20 text-accent-luminous">
                  <Icon name="verified" size={22} />
                </span>
                <div>
                  <h3 className="font-medium text-text-primary">{item.title}</h3>
                  <p className="mt-2 text-sm text-text-secondary">{item.text}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
