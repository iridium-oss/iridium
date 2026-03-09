"use client";

import { motion } from "framer-motion";
import { Icon } from "@/components/ui/Icon";
import { getWuf13FactById } from "@/lib/wuf13-facts";
import { getPitchImage } from "@/lib/images";

export function Wuf13ContextSection() {
  const dates = getWuf13FactById("wuf13_dates");
  const host = getWuf13FactById("wuf13_host");
  const theme = getWuf13FactById("wuf13_theme");
  const convened = getWuf13FactById("wuf13_convened");
  const wuf13Img = getPitchImage("wuf13_small");

  return (
    <section className="border-t border-surface-border bg-white py-16 sm:py-20" id="wuf13-context">
      <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden backdrop-blur"
        >
          {wuf13Img && (
            <a href={wuf13Img.pageUrl} target="_blank" rel="noopener noreferrer" className="block relative aspect-[21/9] w-full bg-surface-dark">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={wuf13Img.imageUrl} alt={wuf13Img.alt} className="w-full h-full object-cover" />
            </a>
          )}
          <div className="p-8">
          <div className="flex items-center gap-2 text-sm font-medium text-text-muted uppercase tracking-wider">
            <Icon name="public" size={20} />
            What is WUF13
          </div>
          <p className="mt-4 text-text-secondary">
            The World Urban Forum (WUF) is the leading global conference on sustainable urban development. WUF13 takes place in Baku, Azerbaijan, from {dates?.value ?? "17 to 22 May 2026"}. The official theme is: {theme?.value ?? "Housing the world: Safe and resilient cities and communities"}. Convened by UN-Habitat and co-organized with the Government of the Republic of Azerbaijan, the Forum brings together governments, cities, civil society, and the private sector to advance the New Urban Agenda and address housing, resilience, and urban challenges. Registration is free of charge. The Forum includes main events, partner-led events, and an Urban Expo focused on sustainable urban solutions, including transport and climate.
          </p>
          <div className="mt-6 flex flex-wrap gap-6 text-sm">
            {dates && (
              <a href={dates.sourceUrl} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">
                {dates.value}
              </a>
            )}
            {host && (
              <a href={host.sourceUrl} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">
                {host.value}
              </a>
            )}
            {convened && (
              <span className="text-text-muted">{convened.value}</span>
            )}
          </div>
          <p className="mt-4 text-xs text-text-muted">
            Source: <a href="https://wuf.unhabitat.org/wuf13" target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">UN-Habitat WUF13</a>, <a href="https://unhabitat.org/events/world-urban-forum-wuf13" target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">UN-Habitat events</a>.
            {wuf13Img && <> Image: <a href={wuf13Img.pageUrl} target="_blank" rel="noopener noreferrer" className="text-accent-muted hover:text-accent-luminous">UN-Habitat WUF13</a>.</>}
          </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
