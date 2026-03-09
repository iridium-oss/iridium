"use client";

import { useState, useEffect } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import Link from "next/link";
import { Icon } from "@/components/ui/Icon";
import { DemoOnboardingModal } from "@/components/demo/DemoOnboardingModal";
import { DemoModeModal } from "@/components/demo/DemoModeModal";

const DEMO_LINKS = [
  { href: "/dashboard/routing", label: "Route planning", icon: "route" as const },
  { href: "/dashboard/forecast", label: "Forecast", icon: "trending_up" as const },
  { href: "/dashboard/anomalies", label: "Anomalies", icon: "warning" as const },
  { href: "/dashboard/equity", label: "Equity", icon: "balance" as const },
  { href: "/dashboard/network", label: "Digital twin", icon: "hub" as const },
];

export default function DemoPage() {
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [showModeModal, setShowModeModal] = useState(false);

  useEffect(() => {
    const seen = sessionStorage.getItem("iridium-demo-seen");
    if (!seen) setShowOnboarding(true);
  }, []);

  const closeOnboarding = () => {
    sessionStorage.setItem("iridium-demo-seen", "1");
    setShowOnboarding(false);
  };

  return (
    <div className="min-h-screen bg-white pt-14">
      <Navbar />
      <main id="main-content" className="pb-20" tabIndex={-1}>
        <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-medium tracking-tight text-text-primary">
            Try IRIDIUM
          </h1>
          <p className="mt-4 max-w-2xl text-text-secondary">
            Explore the product with real API behavior. Choose a mode and then open any module below. Data status and provenance are visible throughout; no synthetic substitution.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <button
              type="button"
              onClick={() => setShowModeModal(true)}
              className="inline-flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card px-4 py-2.5 text-sm font-medium text-text-primary hover:bg-surface-elevated"
            >
              <Icon name="tune" size={20} />
              Mode and scenario
            </button>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 rounded-lg bg-midnight-electric px-4 py-2.5 text-sm font-medium text-white hover:opacity-90"
            >
              Open full dashboard
              <Icon name="arrow_forward" size={20} />
            </Link>
          </div>

          <div className="mt-12">
            <h2 className="font-medium text-text-primary">Explore modules</h2>
            <p className="mt-1 text-sm text-text-secondary">
              Each link opens the live dashboard view. Start with route planning or the digital twin.
            </p>
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {DEMO_LINKS.map(({ href, label, icon }) => (
                <Link
                  key={href}
                  href={href}
                  className="flex items-center gap-4 rounded-xl border border-surface-border bg-surface-card/80 p-5 transition-colors hover:bg-surface-elevated"
                >
                  <span className="flex h-11 w-11 items-center justify-center rounded-lg bg-midnight-electric/20 text-accent-luminous">
                    <Icon name={icon} size={24} />
                  </span>
                  <span className="font-medium text-text-primary">{label}</span>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </main>
      <Footer />

      {showOnboarding && (
        <DemoOnboardingModal onClose={closeOnboarding} />
      )}
      {showModeModal && (
        <DemoModeModal onClose={() => setShowModeModal(false)} />
      )}
    </div>
  );
}
