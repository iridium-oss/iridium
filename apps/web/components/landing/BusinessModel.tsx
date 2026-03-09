"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const CURRENT_ARCHITECTURE = [
  {
    title: "Core municipal mobility intelligence platform subscriptions",
    what: "Subscription access to the digital twin, dashboards, and source-backed analytics.",
    who: "Municipalities, transport authorities, and city agencies.",
    precedent: "White-label and municipal mobility platforms are common (e.g. Trafi, OpenMove, O-CITY, MyTransit offer white-label MaaS and city-facing solutions).",
  },
  {
    title: "Operator and municipality operations dashboards",
    what: "Operational visibility over network state, transit provider status, and alerts.",
    who: "Transit operators and municipal mobility teams.",
    precedent: "Control-room and operations views are standard in urban mobility and ITS deployments.",
  },
  {
    title: "Planning and analytics modules",
    what: "Equity analytics, forecasting, and planning support with documented methodology.",
    who: "Planning departments and policy units.",
    precedent: "Analytics and API monetization are real business lines (e.g. Urban Sharing Analytics API, MyTransit Transit Data API).",
  },
  {
    title: "API and integration access for institutional users",
    what: "Structured API access for integrators and institutional consumers.",
    who: "System integrators, city IT, and partner platforms.",
    precedent: "Modular product strategy with separate monetizable surfaces for dashboards, analytics, and APIs is standard in mobility tech.",
  },
  {
    title: "Deployment and onboarding services",
    what: "Implementation, configuration, and go-live support.",
    who: "Buying institution or operator.",
    precedent: "Services revenue is common in municipal technology rollout.",
  },
  {
    title: "Data normalization and integration services",
    what: "Transit and source normalization, provider onboarding, and data quality setup.",
    who: "Municipalities and operators adopting the platform.",
    precedent: "Integration and data preparation are standard professional services in public-sector software.",
  },
  {
    title: "Training and support packages",
    what: "Training, change management, and ongoing support.",
    who: "Subscribing institutions.",
    precedent: "TwinCity3D and similar platforms offer installation, support, and training as part of deployment.",
  },
  {
    title: "White-label institutional interfaces",
    what: "Institution-branded front ends and reporting.",
    who: "Municipalities and operators requiring their own branding.",
    precedent: "Trafi, OpenMove, O-CITY, and MyTransit offer white-label MaaS and co-branded apps.",
  },
  {
    title: "On-premises and sovereign deployment packages",
    what: "Deployment in the customer environment for sensitive or regulated contexts.",
    who: "Public-sector buyers with data sovereignty or procurement requirements.",
    precedent: "Snap4City is offered as a service or installed on site; sovereign deployment is standard in city technology stacks.",
  },
];

const NEAR_TERM_EXPANSION = [
  "Premium routing and journey intelligence modules.",
  "Anomaly and disruption intelligence modules.",
  "Equity and planning dashboards with policy-ready indicators.",
  "Multi-operator control-room views.",
  "Benchmarking and cross-city comparison modules.",
  "Partner API access for integrators and third-party apps.",
  "Institution-facing reporting exports.",
  "Mobility-data licensing or managed data services where appropriate.",
];

const LONG_TERM_OPTIONALITY = [
  "Research and grant-supported deployments (e.g. Horizon Europe mobility projects, Vinnova-funded digital twin adoption).",
  "Partner integrations with mobility apps and city platforms (Trafi-style and Urban Sharing-style integration paths).",
  "Privacy-preserving institutional AI layers.",
  "Federated learning readiness for regulated data environments (positioned in smart-city and ITS literature as a future-ready architecture).",
  "Regional platform expansion to other cities.",
  "Public-sector digital infrastructure positioning.",
];

export function BusinessModel() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="business-model">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-3xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Business model
          </h2>
          <p className="mt-4 text-text-secondary">
            A modular, public-sector-ready commercial architecture grounded in real market patterns from urban mobility, MaaS, smart-city digital twin, and municipal software. Current commercial model is clearly separated from current traction; future revenue lines are labeled as proposed or strategic.
          </p>
        </motion.div>

        <div className="mt-16">
          <h3 className="text-xl font-medium text-text-primary border-b border-surface-border pb-3 mb-8">
            1. Current monetizable architecture
          </h3>
          <p className="text-sm text-text-secondary mb-8 max-w-3xl">
            Revenue surfaces and commercial model consistent with how urban mobility and public-sector platforms are sold and deployed. No fabricated customers, contracts, or pricing. Market precedent only.
          </p>
          <ul className="space-y-8">
            {CURRENT_ARCHITECTURE.map((item, i) => (
              <motion.li
                key={item.title}
                initial={{ opacity: 0, y: 8 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.03 }}
                className="rounded-xl border border-surface-border bg-white p-6"
              >
                <h4 className="font-medium text-text-primary flex items-center gap-2">
                  <Icon name="account_balance" size={20} className="text-accent-luminous shrink-0" />
                  {item.title}
                </h4>
                <dl className="mt-4 grid gap-2 text-sm sm:grid-cols-1">
                  <div>
                    <dt className="font-medium text-text-primary">What it is</dt>
                    <dd className="text-text-secondary mt-0.5">{item.what}</dd>
                  </div>
                  <div>
                    <dt className="font-medium text-text-primary">Who pays</dt>
                    <dd className="text-text-secondary mt-0.5">{item.who}</dd>
                  </div>
                  <div>
                    <dt className="font-medium text-text-primary">Market precedent</dt>
                    <dd className="text-text-secondary mt-0.5">{item.precedent}</dd>
                  </div>
                </dl>
              </motion.li>
            ))}
          </ul>
        </div>

        <div className="mt-20">
          <h3 className="text-xl font-medium text-text-primary border-b border-surface-border pb-3 mb-6">
            2. Near-term expansion model
          </h3>
          <p className="text-sm text-text-secondary mb-6 max-w-3xl">
            Realistic expansion modules presented as proposed offerings, not current revenue facts.
          </p>
          <ul className="space-y-2 text-sm text-text-secondary">
            {NEAR_TERM_EXPANSION.map((item, i) => (
              <motion.li
                key={item}
                initial={{ opacity: 0, x: -8 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="flex items-start gap-2"
              >
                <span className="shrink-0 mt-1.5 h-1.5 w-1.5 rounded-full bg-accent-muted" />
                {item}
              </motion.li>
            ))}
          </ul>
        </div>

        <div className="mt-20">
          <h3 className="text-xl font-medium text-text-primary border-b border-surface-border pb-3 mb-6">
            3. Long-term strategic optionality
          </h3>
          <p className="text-sm text-text-secondary mb-6 max-w-3xl">
            Strategic pathways backed by market logic and sector trends. Framed as options, not current commitments.
          </p>
          <ul className="space-y-2 text-sm text-text-secondary">
            {LONG_TERM_OPTIONALITY.map((item, i) => (
              <motion.li
                key={item}
                initial={{ opacity: 0, x: -8 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="flex items-start gap-2"
              >
                <span className="shrink-0 mt-1.5 h-1.5 w-1.5 rounded-full bg-text-muted" />
                {item}
              </motion.li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
