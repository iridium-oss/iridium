"use client";

import { useState, useEffect } from "react";
import { apiGet } from "@/lib/api";
import type { EOLayerDescriptor } from "@/lib/api";
import { StatusChip } from "@/components/ui/StatusChip";

type LayerType = "true-color" | "ndvi" | "ndwi" | "ndbi";

const LAYER_OPTIONS: { id: LayerType; label: string }[] = [
  { id: "true-color", label: "True color" },
  { id: "ndvi", label: "NDVI (vegetation)" },
  { id: "ndwi", label: "NDWI (water)" },
  { id: "ndbi", label: "NDBI (built-up)" },
];

type EOLayerControlsProps = {
  sceneId: string;
  layerType: LayerType;
  onLayerChange: (t: LayerType) => void;
};

export function EOLayerControls({ sceneId, layerType, onLayerChange }: EOLayerControlsProps) {
  const [descriptor, setDescriptor] = useState<EOLayerDescriptor | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (layerType === "true-color") {
      setLoading(true);
      apiGet<Record<string, unknown>>(`/api/v1/eo/layers/true-color?scene_id=${encodeURIComponent(sceneId)}`)
        .then((r) => {
          setDescriptor(r as EOLayerDescriptor);
        })
        .catch(() => setDescriptor(null))
        .finally(() => setLoading(false));
    } else {
      setLoading(true);
      apiGet<EOLayerDescriptor>(`/api/v1/eo/layers/${layerType}?scene_id=${encodeURIComponent(sceneId)}`)
        .then(setDescriptor)
        .catch(() => setDescriptor(null))
        .finally(() => setLoading(false));
    }
  }, [sceneId, layerType]);

  return (
    <section className="rounded-xl border border-surface-border bg-surface-card/80 p-4">
      <h2 className="text-sm font-medium text-text-primary">Layer</h2>
      <p className="mt-1 text-xs text-text-muted">
        Satellite context is not realtime transport data.
      </p>
      <div className="mt-3 flex flex-wrap gap-2">
        {LAYER_OPTIONS.map((opt) => (
          <button
            key={opt.id}
            type="button"
            onClick={() => onLayerChange(opt.id)}
            className={`rounded border px-3 py-1.5 text-sm ${
              layerType === opt.id
                ? "border-indigo-500 bg-indigo-50 text-indigo-800"
                : "border-surface-border bg-white text-text-primary hover:bg-surface-deep"
            }`}
          >
            {opt.label}
          </button>
        ))}
      </div>
      {loading && (
        <p className="mt-2 text-xs text-text-muted">Loading descriptor...</p>
      )}
      {descriptor && !loading && (
        <div className="mt-3 border-t border-surface-border pt-3">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm font-medium text-text-primary">{descriptor.name}</span>
            {descriptor.source_status && <StatusChip status={descriptor.source_status} />}
          </div>
          <p className="mt-1 text-xs text-text-secondary">{descriptor.description}</p>
          {descriptor.formula_note && (
            <p className="mt-1 text-xs text-text-muted">{descriptor.formula_note}</p>
          )}
          {descriptor.misuse_warning && (
            <p className="mt-2 text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded p-2">
              {descriptor.misuse_warning}
            </p>
          )}
        </div>
      )}
    </section>
  );
}
