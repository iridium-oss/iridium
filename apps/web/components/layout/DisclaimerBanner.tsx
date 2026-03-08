/**
 * Site-wide disclaimer: data status is shown per panel (live, recorded snapshot, unavailable, configuration required).
 */

export function DisclaimerBanner() {
  return (
    <div
      className="mt-16 border-b border-amber-500/30 bg-amber-500/10 px-4 py-2.5 text-center text-sm text-amber-200"
      role="status"
    >
      Data shown is from real or recorded sources when configured. Each panel shows data status and provenance. Unconfigured sources are marked as unavailable or configuration required.
    </div>
  );
}
