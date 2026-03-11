"use client";

import type { EOProvenanceResponse } from "@/lib/api";
import { StatusChip } from "@/components/ui/StatusChip";
import { Icon } from "@/components/ui/Icon";

type EOProvenanceDrawerProps = {
  open: boolean;
  onClose: () => void;
  provenance: EOProvenanceResponse | null;
};

export function EOProvenanceDrawer({ open, onClose, provenance }: EOProvenanceDrawerProps) {
  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex justify-end"
      role="dialog"
      aria-modal="true"
      aria-label="Satellite provenance"
    >
      <div
        className="absolute inset-0 bg-black/30"
        onClick={onClose}
        onKeyDown={(e) => e.key === "Escape" && onClose()}
      />
      <div className="relative w-full max-w-md bg-white shadow-xl border-l border-surface-border overflow-y-auto">
        <div className="sticky top-0 flex items-center justify-between border-b border-surface-border bg-surface-card px-4 py-3">
          <h2 className="text-lg font-medium text-text-primary">Provenance</h2>
          <button
            type="button"
            onClick={onClose}
            className="rounded p-1 text-text-muted hover:bg-surface-deep hover:text-text-primary"
            aria-label="Close"
          >
            <Icon name="close" size={24} />
          </button>
        </div>
        <div className="p-4 space-y-4">
          <p className="text-sm text-text-secondary">
            Source and acquisition metadata for the selected satellite scene. This is earth observation context, not realtime traffic or transit.
          </p>
          {!provenance ? (
            <p className="text-sm text-text-muted">No provenance data available.</p>
          ) : (
            <>
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-medium text-text-primary">Scene</span>
                {provenance.source_status && <StatusChip status={provenance.source_status} />}
              </div>
              <dl className="grid gap-2 text-sm">
                <div>
                  <dt className="text-text-muted">Provider</dt>
                  <dd className="text-text-primary">{provenance.source_provider}</dd>
                </div>
                {provenance.source_family && (
                  <div>
                    <dt className="text-text-muted">Source family</dt>
                    <dd className="text-text-primary">{provenance.source_family}</dd>
                  </div>
                )}
                {provenance.acquired_at && (
                  <div>
                    <dt className="text-text-muted">Acquired (UTC)</dt>
                    <dd className="text-text-primary">{new Date(provenance.acquired_at).toISOString()}</dd>
                  </div>
                )}
                {provenance.processed_at && (
                  <div>
                    <dt className="text-text-muted">Processed</dt>
                    <dd className="text-text-primary">{new Date(provenance.processed_at).toISOString()}</dd>
                  </div>
                )}
                {provenance.cloud_cover != null && (
                  <div>
                    <dt className="text-text-muted">Cloud cover</dt>
                    <dd className="text-text-primary">{provenance.cloud_cover}%</dd>
                  </div>
                )}
                {provenance.confidence_note && (
                  <div>
                    <dt className="text-text-muted">Confidence note</dt>
                    <dd className="text-text-secondary">{provenance.confidence_note}</dd>
                  </div>
                )}
                {provenance.validation_note && (
                  <div>
                    <dt className="text-text-muted">Validation note</dt>
                    <dd className="text-text-secondary">{provenance.validation_note}</dd>
                  </div>
                )}
              </dl>
              {provenance.misuse_warning && (
                <div className="rounded border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">
                  {provenance.misuse_warning}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
