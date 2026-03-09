import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Icon } from "@/components/ui/Icon";

export default function ArchitecturePage() {
  return (
    <div className="min-h-screen bg-white pt-14">
      <Navbar />
      <main id="main-content" className="pb-20" tabIndex={-1}>
        <div className="mx-auto max-w-wide px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-medium tracking-tight text-text-primary sm:text-4xl">
            Architecture and methodology
          </h1>
          <p className="mt-4 max-w-2xl text-text-secondary">
            IRIDIUM is designed around a real-data stack: each source is documented, each API response carries a data status, and the digital twin is built only from sources that are actually configured and reachable.
          </p>
          <div className="mt-12 space-y-10">
            <section className="rounded-xl border border-surface-border bg-surface-card/60 p-6">
              <h2 className="flex items-center gap-2 text-xl font-medium text-text-primary">
                <Icon name="account_tree" size={24} />
                System layers
              </h2>
              <ul className="mt-4 list-inside list-disc space-y-2 text-text-secondary">
                <li>Network ingestion (OSM PBF, PostGIS, manifest with provenance)</li>
                <li>Weather ingestion (Open-Meteo; Baku, Guba)</li>
                <li>Traffic and transit provider abstraction (configuration or permission required when not set)</li>
                <li>Digital twin state assembler (merges real sources only; no synthetic graph)</li>
                <li>Forecasting, routing, equity, anomaly modules consuming the twin</li>
              </ul>
            </section>
            <section className="rounded-xl border border-surface-border bg-surface-card/60 p-6">
              <h2 className="flex items-center gap-2 text-xl font-medium text-text-primary">
                <Icon name="fact_check" size={24} />
                Data status semantics
              </h2>
              <p className="mt-2 text-text-secondary">
                Every response exposes status per source: live, unavailable, configuration required, permission required, or stale. This allows honest evaluation and incremental deployment as operator agreements and data access become available.
              </p>
            </section>
            <section className="rounded-xl border border-surface-border bg-surface-card/60 p-6">
              <h2 className="flex items-center gap-2 text-xl font-medium text-text-primary">
                <Icon name="psychology" size={24} />
                Federated learning path
              </h2>
              <p className="mt-2 text-text-secondary">
                FedAvg-style aggregation is specified in documentation; client nodes and secure aggregation are planned. No federated training or aggregation experiments are reported in the current baseline.
              </p>
            </section>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
