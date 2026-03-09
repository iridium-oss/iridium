import Link from "next/link";
import { SOURCE_LOGOS } from "@/lib/images";
import { FOOTER_PRODUCT_LINKS, FOOTER_RESOURCES_LINKS } from "@/lib/nav";

export function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white">
      <div className="mx-auto max-w-wide px-4 py-14 sm:px-6 lg:px-8">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-slate-900">IRIDIUM</p>
            <p className="mt-3 text-sm leading-relaxed text-slate-600">
              Real-time urban mobility prediction and optimization for Azerbaijani cities. Provenance-aware, real data only—no synthetic substitution.
            </p>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Product</p>
            <ul className="mt-3 space-y-2">
              {FOOTER_PRODUCT_LINKS.map(({ href, label, external }) =>
                external ? (
                  <li key={href}>
                    <a href={href} target="_blank" rel="noopener noreferrer" className="text-sm text-slate-600 hover:text-slate-900">
                      {label}
                    </a>
                  </li>
                ) : (
                  <li key={href}>
                    <Link href={href} className="text-sm text-slate-600 hover:text-slate-900">
                      {label}
                    </Link>
                  </li>
                )
              )}
            </ul>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Resources</p>
            <ul className="mt-3 space-y-2">
              {FOOTER_RESOURCES_LINKS.map(({ href, label, external }) => (
                <li key={href}>
                  {external ? (
                    <a href={href} target="_blank" rel="noopener noreferrer" className="text-sm text-slate-600 hover:text-slate-900">
                      {label}
                    </a>
                  ) : (
                    <Link href={href} className="text-sm text-slate-600 hover:text-slate-900">
                      {label}
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Legal</p>
            <p className="mt-3 text-sm leading-relaxed text-slate-600">
              Open source (EUPL-1.2). Not production-certified. See repository for limitations and data governance.
            </p>
          </div>
        </div>
        <div className="mt-12 border-t border-slate-200 pt-8">
          <p className="text-center text-xs font-medium uppercase tracking-wider text-slate-400">Data sources and context</p>
          <div className="mt-4 flex flex-wrap items-center justify-center gap-8 sm:gap-12">
            {SOURCE_LOGOS.filter((logo) => logo.id !== "wuf").map((logo) => (
              <a
                key={logo.id}
                href={logo.siteUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center opacity-80 transition-opacity hover:opacity-100"
                title={logo.name}
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={logo.imageUrl}
                  alt={logo.alt}
                  className="h-8 w-auto max-w-[120px] object-contain object-center"
                />
              </a>
            ))}
          </div>
        </div>
        <div className="mt-8 border-t border-slate-200 pt-6 text-center text-sm text-slate-500">
          IRIDIUM — Urban mobility digital twin and analytics. Baku, Guba, Azerbaijan.
        </div>
      </div>
    </footer>
  );
}
