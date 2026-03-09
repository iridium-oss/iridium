"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MAIN_NAV, CTA_NAV } from "@/lib/nav";
import type { NavGroup, NavItem } from "@/lib/nav";

function isNavGroup(item: NavGroup | NavItem): item is NavGroup {
  return "items" in item && Array.isArray((item as NavGroup).items);
}

function NavDropdown({
  group,
  isOpen,
  onOpen,
  onClose,
  pathname,
}: {
  group: NavGroup;
  isOpen: boolean;
  onOpen: () => void;
  onClose: () => void;
  pathname: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const href = group.href ?? "#";
  const hasSubpages = group.items && group.items.length > 0;
  const isActive = pathname === href || (group.items?.some((i) => !i.external && i.href === pathname));

  useEffect(() => {
    if (!isOpen) return;
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose();
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isOpen, onClose]);

  return (
    <div
      ref={ref}
      className="relative"
      onMouseEnter={onOpen}
      onMouseLeave={onClose}
    >
      {hasSubpages ? (
        <>
          <button
            type="button"
            onClick={() => (isOpen ? onClose() : onOpen())}
            className={`flex items-center gap-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
              isActive ? "bg-slate-100 text-slate-900" : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
            }`}
            aria-expanded={isOpen}
            aria-haspopup="true"
          >
            {group.label}
            <span className="material-symbols-outlined text-base transition-transform" style={{ transform: isOpen ? "rotate(180deg)" : "none" }}>
              expand_more
            </span>
          </button>
          <AnimatePresence>
            {isOpen && (
              <motion.div
                initial={{ opacity: 0, y: -4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -4 }}
                transition={{ duration: 0.15 }}
                className="absolute left-0 top-full z-50 mt-1 min-w-[200px] rounded-lg border border-slate-200 bg-white py-1 shadow-lg"
              >
                <Link
                  href={href}
                  className="block border-b border-slate-100 px-4 py-2.5 text-sm font-medium text-slate-900 hover:bg-slate-50"
                  onClick={onClose}
                >
                  {group.label}
                </Link>
                {group.items?.map((sub) =>
                  sub.external ? (
                    <a
                      key={sub.href}
                      href={sub.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                      onClick={onClose}
                    >
                      {sub.label}
                    </a>
                  ) : (
                    <Link
                      key={sub.href}
                      href={sub.href}
                      className={`block px-4 py-2 text-sm ${pathname === sub.href ? "bg-indigo-50 font-medium text-indigo-700" : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"}`}
                      onClick={onClose}
                    >
                      {sub.label}
                    </Link>
                  )
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </>
      ) : (
        <Link
          href={href}
          className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
            isActive ? "bg-slate-100 text-slate-900" : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
          }`}
        >
          {group.label}
        </Link>
      )}
    </div>
  );
}

export function Navbar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

  const closeMobile = () => setMobileOpen(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-slate-200/80 bg-white shadow-sm">
      <nav className="mx-auto flex h-14 max-w-wide items-center justify-between px-4 sm:px-6 lg:px-8" aria-label="Main">
        <Link href="/" className="flex items-center gap-3">
          <span className="text-xl font-semibold tracking-tight text-slate-900">IRIDIUM</span>
          <span className="hidden border-l border-slate-200 pl-3 text-xs font-medium uppercase tracking-wider text-slate-500 sm:block">
            Urban Mobility Intelligence
          </span>
        </Link>

        <div className="hidden items-center gap-0.5 md:flex">
          {MAIN_NAV.map((item) => {
            if (isNavGroup(item)) {
              return (
                <NavDropdown
                  key={item.label}
                  group={item}
                  isOpen={openDropdown === item.label}
                  onOpen={() => setOpenDropdown(item.label)}
                  onClose={() => setOpenDropdown(null)}
                  pathname={pathname}
                />
              );
            }
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                  active ? "bg-slate-100 text-slate-900" : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </div>

        <div className="flex items-center gap-2">
          <Link
            href={CTA_NAV.href}
            className="hidden rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-indigo-700 sm:inline-flex"
          >
            {CTA_NAV.label}
          </Link>
          <button
            type="button"
            className="rounded-md p-2 text-slate-600 hover:bg-slate-100 md:hidden"
            onClick={() => setMobileOpen((o) => !o)}
            aria-expanded={mobileOpen}
            aria-label="Toggle menu"
          >
            <span className="material-symbols-outlined text-xl">{mobileOpen ? "close" : "menu"}</span>
          </button>
        </div>
      </nav>

      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t border-slate-200 bg-white md:hidden"
          >
            <div className="flex flex-col gap-0.5 px-4 py-3">
              {MAIN_NAV.map((item) => {
                if (isNavGroup(item)) {
                  const hasItems = item.items && item.items.length > 0;
                  return (
                    <div key={item.label} className="flex flex-col gap-0.5">
                      <Link
                        href={item.href ?? "#"}
                        className={`rounded-md px-3 py-2.5 text-sm font-medium ${pathname === item.href ? "bg-indigo-50 text-indigo-700" : "text-slate-700"}`}
                        onClick={closeMobile}
                      >
                        {item.label}
                      </Link>
                      {hasItems &&
                        item.items?.map((sub) =>
                          sub.external ? (
                            <a
                              key={sub.href}
                              href={sub.href}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="rounded-md px-5 py-2 text-sm text-slate-600"
                              onClick={closeMobile}
                            >
                              {sub.label}
                            </a>
                          ) : (
                            <Link
                              key={sub.href}
                              href={sub.href}
                              className={`rounded-md px-5 py-2 text-sm ${pathname === sub.href ? "font-medium text-indigo-600" : "text-slate-600"}`}
                              onClick={closeMobile}
                            >
                              {sub.label}
                            </Link>
                          )
                        )}
                    </div>
                  );
                }
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`rounded-md px-3 py-2.5 text-sm font-medium ${pathname === item.href ? "bg-indigo-50 text-indigo-700" : "text-slate-700"}`}
                    onClick={closeMobile}
                  >
                    {item.label}
                  </Link>
                );
              })}
              <Link
                href={CTA_NAV.href}
                className="mt-3 rounded-md bg-indigo-600 py-2.5 text-center text-sm font-semibold text-white md:hidden"
                onClick={closeMobile}
              >
                {CTA_NAV.label}
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
