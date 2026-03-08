"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Icon } from "@/components/ui/Icon";

const LINKS = [
  { href: "/dashboard", label: "Overview", icon: "dashboard" as const },
  { href: "/dashboard/network", label: "Digital twin", icon: "hub" as const },
  { href: "/dashboard/forecast", label: "Forecast", icon: "trending_up" as const },
  { href: "/dashboard/routing", label: "Routing", icon: "route" as const },
  { href: "/dashboard/transit", label: "Transit", icon: "directions_bus" as const },
  { href: "/dashboard/equity", label: "Equity", icon: "balance" as const },
  { href: "/dashboard/anomalies", label: "Anomalies", icon: "warning" as const },
  { href: "/dashboard/provenance", label: "Provenance", icon: "source" as const },
  { href: "/dashboard/status", label: "System status", icon: "monitor_heart" as const },
  { href: "/dashboard/methodology", label: "Methodology", icon: "menu_book" as const },
];

export function DashboardNav() {
  const pathname = usePathname();

  return (
    <nav className="flex flex-col gap-1 p-4" aria-label="Dashboard">
      {LINKS.map(({ href, label, icon }) => {
        const active = pathname === href;
        return (
          <Link
            key={href}
            href={href}
            className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
              active
                ? "bg-surface-elevated text-text-primary"
                : "text-text-secondary hover:bg-surface-card hover:text-text-primary"
            }`}
          >
            <Icon name={icon} size={20} />
            {label}
          </Link>
        );
      })}
    </nav>
  );
}
