# IRIDIUM frontend architecture

The frontend is a Next.js 14 App Router application in `apps/web`. It serves both the public website and the authenticated-style product (dashboard) experience.

## Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS with design tokens (Midnight Magic palette)
- **Font:** Google Sans Variable via @fontsource-variable/google-sans
- **Icons:** Material Symbols Outlined (Google Fonts)
- **Motion:** Framer Motion for modals and scroll-linked animation
- **API:** Fetch to same origin; Next.js rewrites proxy `/api`, `/health`, `/version` to the backend (default localhost:8000)

## Route structure

- `/` – Landing page (hero, product sections, footer)
- `/product` – Product overview and links to dashboard modules
- `/architecture` – Architecture and methodology summary
- `/demo` – Try-it entry point with onboarding and mode modal
- `/dashboard` – App shell (sidebar nav, main content)
  - `/dashboard` – Overview (health, version, quick links)
  - `/dashboard/network` – Digital twin graph (nodes, edges, provenance)
  - `/dashboard/forecast` – Congestion forecast
  - `/dashboard/routing` – Route planning form and result
  - `/dashboard/equity` – Equity score (districts)
  - `/dashboard/anomalies` – Anomaly list
  - `/dashboard/provenance` – Source provenance from twin
  - `/dashboard/status` – System status (health, version)
  - `/dashboard/methodology` – Methodology and limitations

## Data flow

- Dashboard pages are client components that call `lib/api.ts`: `apiGet`, `apiPost`. Types (Health, Version, NetworkGraph, CongestionForecast, RouteResponse, EquityScore, AnomaliesResponse) match backend schemas.
- No global state library; local useState/useEffect per page. Session storage used for demo onboarding (iridium-demo-seen).

## Proxy

In `next.config.js`, rewrites send `/api/*`, `/health`, `/version` to the backend. For production, set the backend URL via env or change the rewrite destination.

## Build and run

- `npm install` in `apps/web`
- `npm run dev` – dev server on port 3000
- `npm run build` then `npm run start` – production

The monorepo may use `dev:web` from root to run the frontend; ensure it runs `next dev -p 3000` (or the script defined in apps/web/package.json).
