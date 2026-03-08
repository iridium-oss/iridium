# IRIDIUM Web

Next.js 14 frontend for the IRIDIUM urban mobility platform. Dark-mode default, Google Sans, Material Symbols, Midnight Magic palette.

## Run

- Install: `npm install`
- Dev: `npm run dev` (port 3000)
- Build: `npm run build`
- Start: `npm run start`

API is proxied to `http://localhost:8000` via Next.js rewrites. Start the backend (e.g. `make run-api` or `uvicorn` from `apps/api`) for full dashboard and demo.

## Structure

- `app/` – App Router: landing (`/`), product, architecture, demo, dashboard
- `components/` – Layout (Navbar, Footer, DisclaimerBanner, DashboardNav), landing sections, demo modals, UI (Icon, StatusChip)
- `lib/api.ts` – API client and types

See `docs/frontend-design-system.md` and `docs/frontend-architecture.md` for design and architecture.
