# IRIDIUM frontend design system

The web app uses a single design system aligned with a premium, Google-caliber product experience. Dark mode is the default.

## Typography

- **Font family:** Google Sans only. Loaded via `@fontsource-variable/google-sans`; CSS variable `--font-google-sans` and Tailwind `font-sans`.
- **Scale:** Display (hero), section titles, body, labels, data values, captions. All use the same family; weight and size create hierarchy.
- **Line length:** Constrained for readability (e.g. max-w-2xl, max-w-3xl for body).

## Color system (Midnight Magic)

- **Black:** `#02010a` (deepest background)
- **Prussian Blue:** `#04052e` (dark surfaces)
- **Deep Twilight:** `#140152` (card/surface tint)
- **Navy:** `#22007c` (primary interaction)
- **Navy Electric:** `#0d00a4` (focus, accent)

Surfaces are defined as CSS variables and Tailwind tokens:

- `--surface-deepest`, `--surface-dark`, `--surface-card`, `--surface-elevated`, `--surface-border`
- Accent: `--accent-luminous`, `--accent-focus`, `--accent-muted`, `--accent-glow`
- Text: `--text-primary`, `--text-secondary`, `--text-muted`

Success, warning, error use palette-calibrated values (e.g. green-400, amber-300, red-200) for status chips and alerts.

## Icons

- **Source:** Material Symbols Outlined from Google Fonts (`fonts.googleapis.com/css2?family=Material+Symbols+Outlined`).
- **Usage:** `<span class="material-symbols-outlined">icon_name</span>` or the shared `Icon` component with `name` prop. Icon names use snake_case (e.g. `arrow_forward`, `check_circle`).
- **Sizing:** 18, 20, 24, 36, 48 via the Icon component or direct class (e.g. `text-2xl`).

## Radius and spacing

- Radius: `--radius-xs` (4px) through `--radius-xl` (24px). Tailwind: `rounded-xs`, `rounded-sm`, `rounded-md`, `rounded-lg`, `rounded-xl`.
- Spacing: Tailwind default scale; additional tokens 4.5, 18, 22 where needed.

## Motion

- Framer Motion for modals and section reveal. Subtle, short duration (0.2–0.35s). Respect `prefers-reduced-motion` in future enhancement.
- Keyframes: `fadeIn`, `slideUp` in Tailwind for lightweight use.

## Components

- **Layout:** Navbar, Footer, DashboardNav.
- **UI:** Icon, StatusChip (live, unavailable, configuration_required, permission_required).
- **Landing:** Hero, WhatIridium, WhyUrbanMobility, CoreModules, RealDataTwin, FederatedPrivacy, MultimodalRouting, EquityAnalytics, AnomalyDetection, LiveDemoCta, TechnicalCredibility, ResearchPublication, OpenSourceInfra.
- **Demo:** DemoOnboardingModal, DemoModeModal.

## Constraints

- No em dash or en dash; use hyphen only.
- No emojis.
- Google Sans only for font; Material Symbols only for icons.
