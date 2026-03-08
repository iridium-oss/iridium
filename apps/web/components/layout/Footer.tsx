import Link from "next/link";

const FOOTER_LINKS = [
  { href: "/product", label: "Product" },
  { href: "/architecture", label: "Architecture" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/demo", label: "Try IRIDIUM" },
];

const EXTERNAL = [
  { href: "https://github.com/iridium-oss/iridium", label: "GitHub" },
];

export function Footer() {
  return (
    <footer className="border-t border-surface-border bg-midnight-black">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <p className="text-sm font-medium text-text-primary">IRIDIUM</p>
            <p className="mt-2 text-sm text-text-muted">
              Real-time urban mobility prediction and optimization for Azerbaijani cities. Real data, provenance-aware, no synthetic substitution.
            </p>
          </div>
          <div>
            <p className="text-sm font-medium text-text-primary">Product</p>
            <ul className="mt-2 space-y-2">
              {FOOTER_LINKS.map(({ href, label }) => (
                <li key={href}>
                  <Link href={href} className="text-sm text-text-secondary hover:text-text-primary">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="text-sm font-medium text-text-primary">Resources</p>
            <ul className="mt-2 space-y-2">
              {EXTERNAL.map(({ href, label }) => (
                <li key={href}>
                  <a href={href} target="_blank" rel="noopener noreferrer" className="text-sm text-text-secondary hover:text-text-primary">
                    {label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="text-sm font-medium text-text-primary">Legal</p>
            <p className="mt-2 text-sm text-text-muted">
              Open source (EUPL-1.2). Not production-certified. See repository for limitations and data governance.
            </p>
          </div>
        </div>
        <div className="mt-10 border-t border-surface-border pt-8 text-center text-sm text-text-muted">
          IRIDIUM. Urban mobility digital twin and analytics. Baku, Quba, Azerbaijan.
        </div>
      </div>
    </footer>
  );
}
