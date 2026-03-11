"use client";

import { useCallback, useEffect, useState } from "react";
import { apiGet } from "@/lib/api";
import type {
  EOStatusResponse,
  EOAreaPreset,
  EOSceneSearchResponse,
  EOSceneItem,
  EOLayerDescriptor,
  EOProvenanceResponse,
} from "@/lib/api";
import { StatusChip } from "@/components/ui/StatusChip";
import { Icon } from "@/components/ui/Icon";
import { EOLayerControls } from "@/components/earth-observation/EOLayerControls";
import { EOProvenanceDrawer } from "@/components/earth-observation/EOProvenanceDrawer";
import { EOMapContainer } from "@/components/earth-observation/EOMapContainer";

export default function SatelliteContextPage() {
  const [eoStatus, setEoStatus] = useState<EOStatusResponse | null>(null);
  const [areas, setAreas] = useState<EOAreaPreset[]>([]);
  const [searchResult, setSearchResult] = useState<EOSceneSearchResponse | null>(null);
  const [selectedScene, setSelectedScene] = useState<EOSceneItem | null>(null);
  const [layerType, setLayerType] = useState<"true-color" | "ndvi" | "ndwi" | "ndbi">("true-color");
  const [provenance, setProvenance] = useState<EOProvenanceResponse | null>(null);
  const [provenanceOpen, setProvenanceOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const presetId = "baku";
  const dateEnd = new Date();
  const dateStart = new Date(dateEnd);
  dateStart.setMonth(dateStart.getMonth() - 3);

  const loadStatusAndAreas = useCallback(async () => {
    try {
      const [statusRes, areasRes] = await Promise.all([
        apiGet<EOStatusResponse>("/api/v1/eo/status"),
        apiGet<{ areas: EOAreaPreset[] }>("/api/v1/eo/areas"),
      ]);
      setEoStatus(statusRes);
      setAreas(areasRes.areas ?? []);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load EO status");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadStatusAndAreas();
  }, [loadStatusAndAreas]);

  const runSearch = useCallback(async () => {
    if (!eoStatus?.enabled) return;
    setSearching(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.set("preset", presetId);
      params.set("date_start", dateStart.toISOString());
      params.set("date_end", dateEnd.toISOString());
      params.set("cloud_cover_max", "30");
      params.set("limit", "15");
      const res = await apiGet<EOSceneSearchResponse>(`/api/v1/eo/scenes/search?${params.toString()}`);
      setSearchResult(res);
      if (res.scenes?.length) setSelectedScene(res.scenes[0]);
      else setSelectedScene(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Search failed");
      setSearchResult(null);
      setSelectedScene(null);
    } finally {
      setSearching(false);
    }
  }, [eoStatus?.enabled]);

  useEffect(() => {
    if (eoStatus?.enabled && areas.length) runSearch();
  }, [eoStatus?.enabled, areas.length, runSearch]);

  const openProvenance = useCallback(async (scene: EOSceneItem) => {
    try {
      const res = await apiGet<EOProvenanceResponse>(
        `/api/v1/eo/provenance?scene_id=${encodeURIComponent(scene.scene_id)}`
      );
      setProvenance(res);
      setProvenanceOpen(true);
    } catch {
      setProvenance(null);
      setProvenanceOpen(true);
    }
  }, []);

  if (loading) {
    return (
      <div className="flex items-center gap-2 rounded-lg border border-surface-border bg-surface-card/80 px-4 py-6 text-text-secondary">
        <span className="material-symbols-outlined animate-pulse">progress_activity</span>
        Loading...
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-medium tracking-tight text-text-primary">
        Satellite context
      </h1>
      <p className="mt-1 text-sm text-text-secondary">
        Sentinel-2 earth observation layer for environmental context. Not realtime traffic or transit data.
      </p>

      {eoStatus && (
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <StatusChip status={eoStatus.data_status} />
          {eoStatus.providers_available?.length ? (
            <span className="text-xs text-text-muted">
              Providers: {eoStatus.providers_available.join(", ")}
            </span>
          ) : null}
          {eoStatus.note && (
            <span className="text-xs text-text-muted">{eoStatus.note}</span>
          )}
        </div>
      )}

      {error && (
        <div className="mt-4 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          {error}
        </div>
      )}

      {!eoStatus?.enabled && !loading && (
        <div className="mt-6 rounded-xl border border-surface-border bg-surface-card/80 p-6 text-center text-text-secondary">
          Earth observation is disabled or unavailable. Check API configuration.
        </div>
      )}

      {eoStatus?.enabled && (
        <>
          <div className="mt-6 grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-1 space-y-4">
              <section className="rounded-xl border border-surface-border bg-surface-card/80 p-4">
                <h2 className="text-sm font-medium text-text-primary">Area</h2>
                <p className="mt-1 text-xs text-text-muted">
                  Preset: {presetId}. Change in code or extend API for selector.
                </p>
              </section>
              <section className="rounded-xl border border-surface-border bg-surface-card/80 p-4">
                <h2 className="text-sm font-medium text-text-primary">Scenes</h2>
                {searching ? (
                  <p className="mt-2 text-xs text-text-muted">Searching...</p>
                ) : searchResult?.scenes?.length ? (
                  <ul className="mt-2 space-y-2">
                    {searchResult.scenes.slice(0, 10).map((s) => (
                      <li key={s.scene_id}>
                        <button
                          type="button"
                          onClick={() => setSelectedScene(s)}
                          className={`w-full rounded border px-3 py-2 text-left text-sm ${
                            selectedScene?.scene_id === s.scene_id
                              ? "border-indigo-500 bg-indigo-50 text-indigo-800"
                              : "border-surface-border bg-white text-text-primary hover:bg-surface-deep"
                          }`}
                        >
                          <span className="font-mono text-xs">{s.scene_id.slice(0, 28)}...</span>
                          <br />
                          <span className="text-xs text-text-muted">
                            {s.metadata?.acquired_at
                              ? new Date(s.metadata.acquired_at).toLocaleDateString()
                              : "No date"}
                            {s.metadata?.cloud_cover != null
                              ? ` | Cloud: ${s.metadata.cloud_cover}%`
                              : ""}
                          </span>
                        </button>
                        <button
                          type="button"
                          onClick={() => openProvenance(s)}
                          className="mt-1 text-xs text-indigo-600 hover:underline"
                        >
                          Provenance
                        </button>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="mt-2 text-xs text-text-muted">No scenes. Try another area or date.</p>
                )}
              </section>
              {selectedScene && (
                <EOLayerControls
                  sceneId={selectedScene.scene_id}
                  layerType={layerType}
                  onLayerChange={setLayerType}
                />
              )}
            </div>
            <div className="lg:col-span-2">
              <div className="rounded-xl border border-surface-border bg-surface-card/80 overflow-hidden">
                <EOMapContainer
                  presetBbox={areas.find((a) => a.preset_id === presetId)?.bbox}
                  scene={selectedScene}
                  layerType={layerType}
                />
                {selectedScene && (
                  <div className="border-t border-surface-border bg-surface-deepest px-4 py-2 text-xs text-text-muted">
                    {selectedScene.metadata?.acquired_at && (
                      <span>Acquired: {new Date(selectedScene.metadata.acquired_at).toISOString()}</span>
                    )}
                    {selectedScene.metadata?.cloud_cover != null && (
                      <span className="ml-4">Cloud: {selectedScene.metadata.cloud_cover}%</span>
                    )}
                    <span className="ml-4">Source: {selectedScene.metadata?.source_provider}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
          <EOProvenanceDrawer
            open={provenanceOpen}
            onClose={() => setProvenanceOpen(false)}
            provenance={provenance}
          />
        </>
      )}
    </div>
  );
}
