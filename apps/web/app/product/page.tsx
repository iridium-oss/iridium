import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import Link from "next/link";
import { Icon } from "@/components/ui/Icon";

export default function ProductPage() {
  return (
    <div className="min-h-screen bg-white pt-14">
      <Navbar />
      <main id="main-content" className="pb-20" tabIndex={-1}>
        <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Product overview
          </h1>
          <p className="mt-4 max-w-2xl text-text-secondary">
            IRIDIUM is a real-time urban mobility prediction and optimization platform for Azerbaijani cities. It combines a provenance-aware digital twin, real external data sources, and modular analytics for forecasting, multimodal routing, equity, and anomaly detection.
          </p>
          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {[
              { href: "/dashboard", label: "Overview dashboard", desc: "System status and quick links.", icon: "dashboard" as const },
              { href: "/dashboard/network", label: "Digital twin", desc: "Network graph and snapshot.", icon: "hub" as const },
              { href: "/dashboard/forecast", label: "Congestion forecast", desc: "Short-horizon segments.", icon: "trending_up" as const },
              { href: "/dashboard/routing", label: "Route planning", desc: "Origin, destination, optimize.", icon: "route" as const },
              { href: "/dashboard/equity", label: "Equity analytics", desc: "District-level MES.", icon: "balance" as const },
              { href: "/dashboard/anomalies", label: "Anomalies", desc: "Detected incidents.", icon: "warning" as const },
            ].map(({ href, label, desc, icon }) => (
              <Link
                key={href}
                href={href}
                className="block rounded-xl border border-surface-border bg-white p-6 transition-colors hover:border-indigo-200"
              >
                <span className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-midnight-electric/20 text-accent-luminous">
                  <Icon name={icon} size={24} />
                </span>
                <h2 className="mt-4 font-medium text-text-primary">{label}</h2>
                <p className="mt-2 text-sm text-text-secondary">{desc}</p>
              </Link>
            ))}
          </div>
          <div className="mt-12">
            <Link href="/demo" className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-700">
              Try IRIDIUM
              <Icon name="arrow_forward" size={20} />
            </Link>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
