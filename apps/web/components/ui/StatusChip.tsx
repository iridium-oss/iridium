type StatusChipProps = { status: string; label?: string; className?: string };

const STATUS_STYLES: Record<string, string> = {
  live: "border-green-500/40 bg-green-500/15 text-green-300",
  cached: "border-sky-500/40 bg-sky-500/15 text-sky-300",
  unavailable: "border-red-500/40 bg-red-500/15 text-red-300",
  configuration_required: "border-amber-500/40 bg-amber-500/15 text-amber-300",
  permission_required: "border-blue-500/40 bg-blue-500/15 text-blue-300",
  stale: "border-amber-500/40 bg-amber-500/15 text-amber-300",
};

export function StatusChip({ status, label, className = "" }: StatusChipProps) {
  const style = STATUS_STYLES[status] ?? "border-surface-border bg-surface-card text-text-secondary";
  return (
    <span className={`inline-flex items-center rounded-md border px-2.5 py-1 text-xs font-medium ${style} ${className}`}>
      {label ?? status}
    </span>
  );
}
