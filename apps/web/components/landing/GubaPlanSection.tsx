"use client";
import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getSourceLogo } from "@/lib/images";

const GUBA_PLAN_PDF = "https://arxkom.gov.az/storage/media/1569/a48d75cf-ef78-4004-9a13-ccf98c5e9893.pdf";

export function GubaPlanSection() {
  const arxkomLogo = getSourceLogo("arxkom");

  return (
    <section className="border-t border-surface-border bg-white py-20 sm:py-28" id="guba-plan">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-xl border border-surface-border bg-white overflow-hidden"
        >
          <div className="p-6 sm:p-8">
            <div className="flex flex-wrap items-center gap-3 mb-4">
              <h2 className="text-2xl font-medium tracking-tight text-text-primary sm:text-3xl">
                Guba city master plan
              </h2>
              {arxkomLogo && (
                <a href={arxkomLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="shrink-0">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={arxkomLogo.imageUrl} alt={arxkomLogo.alt} className="h-8 w-auto object-contain" />
                </a>
              )}
            </div>
            <p className="text-text-secondary max-w-2xl">
              Official master plan (baş plan) of Guba city from the State Committee on Urban Planning and Architecture (Arxkom). The plan is in portrait format; open the PDF and rotate in your viewer for landscape viewing.
            </p>
            <a
              href={GUBA_PLAN_PDF}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-6 inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-3 text-sm font-medium text-white transition-colors hover:bg-indigo-700"
            >
              <Icon name="open_in_new" size={20} />
              Open Guba city plan (PDF)
            </a>
            <p className="mt-3 text-xs text-text-muted">
              Source: <a href="https://arxkom.gov.az" target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">State Committee on Urban Planning and Architecture (Arxkom)</a>. <a href={GUBA_PLAN_PDF} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">Quba şəhərinin baş planı</a>
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
