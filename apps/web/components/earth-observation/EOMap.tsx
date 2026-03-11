"use client";

import { useRef, useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

type EOMapProps = {
  center: [number, number];
  zoom: number;
  bbox?: number[];
  sceneId?: string;
  layerType: string;
};

export function EOMap({ center, zoom, bbox, sceneId, layerType }: EOMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const layerRef = useRef<L.Rectangle | null>(null);

  useEffect(() => {
    if (!mapRef.current || typeof window === "undefined") return;

    if (mapInstanceRef.current) {
      mapInstanceRef.current.remove();
      mapInstanceRef.current = null;
    }

    const map = L.map(mapRef.current).setView(center, zoom);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    mapInstanceRef.current = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, [center[0], center[1], zoom]);

  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map || !bbox || bbox.length < 4) return;

    if (layerRef.current) {
      map.removeLayer(layerRef.current);
      layerRef.current = null;
    }

    const bounds: L.LatLngBoundsLiteral = [
      [bbox[1], bbox[0]],
      [bbox[3], bbox[2]],
    ];
    const rect = L.rectangle(bounds, {
      color: "#4f46e5",
      weight: 2,
      fillOpacity: 0.05,
    });
    rect.addTo(map);
    layerRef.current = rect;
    map.fitBounds(bounds, { padding: [20, 20] });

    return () => {
      if (layerRef.current) {
        map.removeLayer(layerRef.current);
        layerRef.current = null;
      }
    };
  }, [bbox]);

  return (
    <div
      ref={mapRef}
      className="h-[400px] w-full"
      data-scene-id={sceneId}
      data-layer-type={layerType}
      aria-label="Satellite context map. AOI bounds shown. Imagery layer requires tile service."
    />
  );
}
