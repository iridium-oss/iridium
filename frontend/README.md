# Frontend

This directory contains the IRIDIUM web application: user-facing dashboards, route planning interface, and visualisations for forecasts and the Mobility Equity Score.

## Purpose

- **Route planning**: Origin-destination input and display of multimodal routes (time, cost, carbon) from the routing API.
- **Forecast visualisation**: Display of short-horizon congestion or traffic state from the forecasting API.
- **Equity dashboard**: District-level Mobility Equity Score indicators and accessibility gap visualisation.
- **Operational views**: Optional views for anomaly alerts and system status for operators or administrators.

## Technology

Technology choices (e.g. React, Vue, or other framework; state management; build tooling) will be documented here once adopted. The frontend will consume the APIs defined in `docs/api-spec.md` and will use the data contracts for request and response typing where applicable.

## Structure

Structure will be established with the chosen framework. Typical layout may include:

- `src/`: Application source (components, pages, services, assets).
- `public/`: Static assets.
- Configuration files for the build and dev server.

## Development

- Run the development server and proxy to the backend API as per local setup instructions (to be added).
- Follow the project's coding standards and the CONTRIBUTING guidelines. All user-facing text must be formal and professional; no emojis.

## Testing

Frontend tests (unit or component tests) may live here or in the repository `tests/` directory under a frontend subtree. CI will run the test suite as configured in the root and in `.github/workflows/`.
