"use client";

import { motion } from "framer-motion";

const ROWS = [
  {
    offering: "Platform subscription",
    buyer: "Municipalities, transport authorities",
    delivery: "Cloud or on-premises",
    revenueType: "Recurring",
    maturity: "Proposed",
    why: "Core access to digital twin and dashboards; standard in municipal mobility platforms.",
  },
  {
    offering: "Analytics module",
    buyer: "Planning departments, policy units",
    delivery: "Included or add-on",
    revenueType: "Subscription or module fee",
    maturity: "Proposed",
    why: "Equity, forecasting, planning; analytics APIs are standard monetizable layers.",
  },
  {
    offering: "API access",
    buyer: "Integrators, city IT, partners",
    delivery: "API tier",
    revenueType: "Usage or tier-based",
    maturity: "Proposed",
    why: "Urban Sharing and MyTransit monetize APIs; supports modular product strategy.",
  },
  {
    offering: "White-label deployment",
    buyer: "Municipalities, operators",
    delivery: "Institution-hosted or managed",
    revenueType: "License or subscription",
    maturity: "Proposed",
    why: "Trafi, OpenMove, O-CITY offer white-label; cities already buy such solutions.",
  },
  {
    offering: "On-premises deployment",
    buyer: "Public-sector with sovereignty requirements",
    delivery: "Customer environment",
    revenueType: "License, implementation, support",
    maturity: "Proposed",
    why: "Snap4City, TwinCity3D use on-prem; standard for sensitive or regulated contexts.",
  },
  {
    offering: "Implementation services",
    buyer: "Buying institution",
    delivery: "Project-based",
    revenueType: "Professional services",
    maturity: "Proposed",
    why: "Common in municipal technology rollout and integration.",
  },
  {
    offering: "Support and training",
    buyer: "Subscribing institutions",
    delivery: "Ongoing",
    revenueType: "Support package",
    maturity: "Proposed",
    why: "TwinCity3D and similar offer support and training as part of deployment.",
  },
  {
    offering: "Partner integrations",
    buyer: "Mobility apps, city platforms",
    delivery: "API and integration",
    revenueType: "Partnership or usage",
    maturity: "Strategic",
    why: "Trafi and Urban Sharing style expansion path; standard in MaaS ecosystems.",
  },
  {
    offering: "Research deployment",
    buyer: "Grant-funded projects, research consortia",
    delivery: "Pilot or project",
    revenueType: "Grant or project funding",
    maturity: "Strategic",
    why: "Digital Twin Cities Centre, Horizon Europe mobility projects show precedent.",
  },
  {
    offering: "Federated learning readiness",
    buyer: "Institutions requiring privacy-preserving AI",
    delivery: "Architecture and optional modules",
    revenueType: "Differentiator or future module",
    maturity: "Strategic",
    why: "Smart-city and ITS literature positions FL as future-ready institutional differentiator.",
  },
];

const COLUMNS = ["Offering", "Buyer", "Delivery model", "Revenue type", "Maturity", "Why it matters"] as const;

export function CommercialMatrix() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="commercial-matrix">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-4xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Commercial architecture matrix
          </h2>
          <p className="mt-4 text-text-secondary text-sm max-w-2xl">
            Strategic product-commercialization matrix. All items are proposed or strategic; none imply current revenue or signed contracts.
          </p>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-10 overflow-x-auto rounded-xl border border-surface-border bg-white"
        >
          <table className="w-full min-w-[720px] text-left text-sm">
            <thead>
              <tr className="border-b border-surface-border bg-surface-elevated/50">
                {COLUMNS.map((col) => (
                  <th key={col} className="px-4 py-3 font-medium text-text-primary whitespace-nowrap">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {ROWS.map((row, i) => (
                <tr
                  key={row.offering}
                  className="border-b border-surface-border last:border-b-0 hover:bg-surface-elevated/30 transition-colors"
                >
                  <td className="px-4 py-3 font-medium text-text-primary">{row.offering}</td>
                  <td className="px-4 py-3 text-text-secondary">{row.buyer}</td>
                  <td className="px-4 py-3 text-text-secondary">{row.delivery}</td>
                  <td className="px-4 py-3 text-text-secondary">{row.revenueType}</td>
                  <td className="px-4 py-3">
                    <span className="inline-flex rounded-full bg-accent-muted/20 px-2.5 py-0.5 text-xs font-medium text-text-secondary">
                      {row.maturity}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-text-secondary max-w-[240px]">{row.why}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      </div>
    </section>
  );
}
