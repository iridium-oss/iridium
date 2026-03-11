"use client";

import dynamic from "next/dynamic";
import type { EOSceneItem } from "@/lib/api";

const EOMap = dynamic(
  () => import("./EOMap").then((m) => m.EOMap),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-[400px] items-center justify-center bg-surface-deep text-text-muted">
        <span className="material-symbols-outlined animate-pulse">map</span>
        <span className="ml-2">Loading map...</span>
      </div>
    ),
  }
);

type EOMapContainerProps = {
  presetBbox?: number[];
  scene: EOSceneItem | null;
  layerType: "true-color" | "ndvi" | "ndwi" | "ndbi";
};

export function EOMapContainer({ presetBbox, scene, layerType }: EOMapContainerProps) {
  const bbox = scene?.metadata?.bbox ?? presetBbox;
  const center: [number, number] = bbox && bbox.length >= 4
    ? [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
    : [49.87, 40.38];
  const zoom = bbox && bbox.length >= 4 ? 11 : 10;

  return (
    <EOMap
      center={center}
      zoom={zoom}
      bbox={bbox && bbox.length >= 4 ? bbox : undefined}
      sceneId={scene?.scene_id}
      layerType={layerType}
    />
  );
}
