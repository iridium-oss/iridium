"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";

const LINKS = [
  { href: "https://github.com/iridium-oss/iridium", label: "Repository", icon: "code" as const },
  { href: "https://doi.org/10.5281/zenodo.18915211", label: "Zenodo DOI", icon: "tag" as const },
  { href: "https://arxiv.org/abs/submit/7340933", label: "arXiv preprint", icon: "menu_book" as const },
];

export function ResearchPublicationReadiness() {
  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="research-publication">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-3xl"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Research and publication readiness
          </h2>
          <p className="mt-6 text-text-secondary">
            Open-source repository, paper and preprint readiness, Zenodo DOI, documentation quality, and reproducibility orientation. System-paper positioning helps judges and technically minded stakeholders trust the project. Relevant to urban innovation dialogue and public-interest technology discussion in the WUF13 context.
          </p>
          <ul className="mt-6 space-y-2 text-sm text-text-secondary">
            <li className="flex items-center gap-2">
              <Icon name="check_circle" size={20} className="shrink-0 text-accent-luminous" />
              Academic manuscript (IEEE-style) framing IRIDIUM as provenance-aware real-data baseline
            </li>
            <li className="flex items-center gap-2">
              <Icon name="check_circle" size={20} className="shrink-0 text-accent-luminous" />
              Preprint packaging and citation metadata in repository; CITATION.cff
            </li>
            <li className="flex items-center gap-2">
              <Icon name="check_circle" size={20} className="shrink-0 text-accent-luminous" />
              Documentation: architecture, data provenance, operator integration, real-data mode
            </li>
            <li className="flex items-center gap-2">
              <Icon name="check_circle" size={20} className="shrink-0 text-accent-luminous" />
              Reproducibility: code version, environment, and data sources documented
            </li>
          </ul>
          <div className="mt-8 flex flex-wrap gap-4">
            {LINKS.map(({ href, label, icon }) => (
              <a
                key={href}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card px-4 py-2.5 text-sm font-medium text-text-primary hover:bg-surface-elevated"
              >
                <Icon name={icon} size={20} />
                {label}
              </a>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
