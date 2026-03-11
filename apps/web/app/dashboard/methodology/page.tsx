import { Icon } from "@/components/ui/Icon";

export default function MethodologyPage() {
  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Methodology
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        Project approach, formulation, and limitations. See the repository and paper for full detail.
      </p>

      <div className="mt-8 space-y-6">
        <section className="rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="font-medium text-text-primary">Formulation</h2>
          <p className="mt-2 text-sm text-text-secondary">
            Mobility graph (nodes, edges, weights), routing objective (time, cost, carbon, penalty), forecasting target (short-horizon congestion), equity composite (MES), and anomaly score are formalized in the codebase and manuscript. The current implementation uses a heuristic forecast baseline; ST-GNN and federated aggregation are architected for future use.
          </p>
        </section>
        <section className="rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="font-medium text-text-primary">Earth observation (Sentinel-2)</h2>
          <p className="mt-2 text-sm text-text-secondary">
            Sentinel-2 is used as a spatial intelligence layer for urban footprint, green cover, water context, and land-use around mobility corridors. Search uses Copernicus Data Space Ecosystem STAC with Earth Search STAC as fallback. Indices (NDVI, NDWI, NDBI) are derived from standard band math. Every layer exposes source provider, acquisition date, and cloud cover. Satellite context is not realtime traffic or transit data; it is near-recent earth observation for environmental and equity context only. See docs/sentinel2-integration.md and docs/eo-limitations.md.
          </p>
        </section>
        <section className="rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="font-medium text-text-primary">Limitations</h2>
          <p className="mt-2 text-sm text-text-secondary">
            Transit feeds require operator provision; traffic requires a licensed provider. No forecasting accuracy, routing quality, or equity validation is reported where not measured. The platform does not claim production readiness or regulatory compliance. Deployers must conduct their own assessment.
          </p>
        </section>
        <section className="rounded-xl border border-surface-border bg-surface-card/80 p-6">
          <h2 className="font-medium text-text-primary">Paper and citation</h2>
          <p className="mt-2 text-sm text-text-secondary">
            The project includes an academic manuscript (IEEE-style) framing IRIDIUM as a provenance-aware real-data baseline. Preprint and citation metadata are in the repository.
          </p>
          <a
            href="https://github.com/iridium-oss/iridium"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-flex items-center gap-2 rounded-lg border border-surface-border bg-midnight-prussian px-4 py-2 text-sm font-medium text-text-primary hover:bg-surface-card"
          >
            <Icon name="menu_book" size={20} />
            Repository
          </a>
        </section>
      </div>
    </div>
  );
}
