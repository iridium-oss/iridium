"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getWuf13FactById } from "@/lib/wuf13-facts";
import { getPitchImage, getSourceLogo } from "@/lib/images";

export function WhyNowForBaku() {
  const host = getWuf13FactById("wuf13_host");
  const dates = getWuf13FactById("wuf13_dates");
  const yearTheme = getWuf13FactById("year_urban_planning");
  const campaign = getWuf13FactById("azerbaijan_urban_campaign");
  const wuf13Img = getPitchImage("wuf13_small");
  const metroImg = getPitchImage("baku_metro");
  const wuf13Logo = getSourceLogo("wuf13");
  const metroLogo = getSourceLogo("metro");
  const bakubusLogo = getSourceLogo("bakubus");
  const arxkomLogo = getSourceLogo("arxkom");

  return (
    <section className="border-t border-surface-border py-20 sm:py-28" id="why-now-baku">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-2xl mx-auto"
        >
          <h2 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Why now for Baku
          </h2>
          <p className="mt-4 text-text-secondary">
            Baku is hosting WUF13 in 2026. Urban mobility is central to how safe and resilient cities function. IRIDIUM is especially relevant in Baku as a city-scale mobility intelligence platform aligned with this moment.
          </p>
        </motion.div>
        {(metroLogo || bakubusLogo) && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mt-10 flex flex-wrap items-center justify-center gap-8"
          >
            {metroLogo && (
              <a href={metroLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="opacity-80 hover:opacity-100 transition-opacity">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={metroLogo.imageUrl} alt={metroLogo.alt} className="h-10 w-auto max-w-[100px] object-contain" />
              </a>
            )}
            {bakubusLogo && (
              <a href={bakubusLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="opacity-80 hover:opacity-100 transition-opacity">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={bakubusLogo.imageUrl} alt={bakubusLogo.alt} className="h-10 w-auto max-w-[100px] object-contain" />
              </a>
            )}
          </motion.div>
        )}
        <div className="mt-14 grid gap-8 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, x: -12 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur"
          >
            {wuf13Img && (
              <a href={wuf13Img.pageUrl} target="_blank" rel="noopener noreferrer" className="block relative aspect-video w-full bg-surface-dark">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={wuf13Img.imageUrl} alt={wuf13Img.alt} className="w-full h-full object-cover" />
              </a>
            )}
            <div className="p-8">
              <div className="flex items-center gap-3 flex-wrap">
                <h3 className="font-medium text-text-primary flex items-center gap-2">
                  <Icon name="event" size={24} />
                  WUF13 in Baku
                </h3>
                {wuf13Logo && (
                  <a href={wuf13Logo.siteUrl} target="_blank" rel="noopener noreferrer" className="h-8 shrink-0">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={wuf13Logo.imageUrl} alt={wuf13Logo.alt} className="h-8 w-auto object-contain" />
                  </a>
                )}
              </div>
              <p className="mt-4 text-sm text-text-secondary">
                {host?.value ?? "Baku, Azerbaijan"} hosts the World Urban Forum 13 from {dates?.value ?? "17 to 22 May 2026"}. The global urban agenda is set here. Cities, governments, and innovators will focus on safe and resilient communities, housing, and integrated urban systems. Mobility is a core enabler.
              </p>
              <a href={dates?.sourceUrl ?? "https://wuf.unhabitat.org/wuf13"} target="_blank" rel="noopener noreferrer" className="mt-4 inline-block text-xs text-accent-muted hover:text-accent-luminous">Source: UN-Habitat WUF13</a>
              {wuf13Img && <p className="mt-2 text-xs text-text-muted">Image: <a href={wuf13Img.pageUrl} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">UN-Habitat WUF13</a></p>}
            </div>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, x: 12 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur"
          >
            {metroImg && (
              <a href={metroImg.pageUrl} target="_blank" rel="noopener noreferrer" className="block relative aspect-video w-full bg-surface-dark">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={metroImg.imageUrl} alt={metroImg.alt} className="w-full h-full object-cover" />
              </a>
            )}
            <div className="p-8">
              <div className="flex items-center gap-3 flex-wrap">
                <h3 className="font-medium text-text-primary flex items-center gap-2">
                  <Icon name="today" size={24} />
                  2026: Urban planning and mobility
                </h3>
                {metroLogo && (
                  <a href={metroLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="h-8 shrink-0">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={metroLogo.imageUrl} alt={metroLogo.alt} className="h-8 w-auto object-contain" />
                  </a>
                )}
                {arxkomLogo && (
                  <a href={arxkomLogo.siteUrl} target="_blank" rel="noopener noreferrer" className="h-8 shrink-0">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={arxkomLogo.imageUrl} alt={arxkomLogo.alt} className="h-8 w-auto object-contain" />
                  </a>
                )}
              </div>
              <p className="mt-4 text-sm text-text-secondary">
                Azerbaijan has elevated urban planning and architecture as a national strategic theme in 2026 ({yearTheme?.value ?? "Year of Urban Planning and Architecture"}). {campaign?.value ?? "Azerbaijan Urban Campaign 2026 was launched in preparation for WUF13 and explicitly includes mobility among its focus areas."} IRIDIUM fits this context as a mobility intelligence layer. We do not claim city adoption or official selection; we position the product as strategically relevant and timely.
              </p>
              <a href={campaign?.sourceUrl ?? "https://wuf.unhabitat.org/wuf13"} target="_blank" rel="noopener noreferrer" className="mt-4 inline-block text-xs text-accent-muted hover:text-accent-luminous">Source: WUF13 preparation</a>
              {metroImg && <p className="mt-2 text-xs text-text-muted">Image: <a href={metroImg.pageUrl} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">Baku Metro</a></p>}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
