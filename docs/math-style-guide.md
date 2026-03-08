# Mathematical Style Guide

Consistent notation is used across IRIDIUM documentation and, when applicable, in a future preprint. Use this guide when adding or editing formulas.

## Typesetting

- In Markdown, use inline math with `$...$` and display math with `$$...$$`.
- Symbols must match the [symbol glossary](symbol-glossary.md). The same symbol should not denote different things in different documents.

## Conventions

| Concept | Notation | Notes |
|---------|----------|--------|
| Graph | $G = (V, E)$ or $G = (V, E, W)$ | $V$ nodes, $E$ edges, $W$ optional weights. |
| Node set size | $|V|$ or $N$ | Number of nodes. |
| Feature matrix (time $t$) | $X_t \in \mathbb{R}^{N \times F}$ | $F$ features per node. |
| Time index | $t$, $t+1$, $t-T+1:t$ | Subscript or range; avoid reusing $t$ for other meanings in the same section. |
| Forecast horizon | $H$ | Number of future steps. |
| District index | $d$ or $k$ | For equity; $m$ for indicator index. |
| Route | $r$ | A path or itinerary. |
| Model parameters | $\theta$ | Global or local model weights. |
| Loss | $\mathcal{L}$, $\mathcal{L}_k$ | $k$ for client or district. |
| Weights (routing/equity) | $\alpha, \beta, \gamma, \delta$ or $w_m$ | Defined in context. |

## Federated Learning

- Local objective: $\min_\theta \sum_{k=1}^{K} p_k \mathcal{L}_k(\theta)$.
- Client update: $\theta_k^{(t)}$; aggregation: $\theta^{(t+1)} = \sum_k \frac{n_k}{\sum_j n_j} \theta_k^{(t)}$ (FedAvg-style). Use $n_k$ for local sample count, $p_k$ for weight.

## Forecasting

- Graph: $G = (V, E, W)$. Input window: $X_{t-T+1:t}$. Forecast: $\hat{Y}_{t+1:t+H} = f_\theta(X_{t-T+1:t}, G)$. Loss: MAE, RMSE, or MAPE as defined in symbol-glossary.

## Routing

- Route utility: $J(r) = \alpha T(r) + \beta C(r) + \gamma E(r) + \delta P(r)$ with $T$ travel time, $C$ cost, $E$ emissions proxy, $P$ penalty. Define symbols on first use.

## Equity

- District $d$, indicators $m$. Normalised value: $z_{d,m}$. Composite: $MES_d = \sum_m w_m z_{d,m}$. State that MES is a derived analytic index, not an official statistic.

## Anomaly

- Deviation: $z_t = (x_t - \mu_{t,w}) / \sigma_{t,w}$ (rolling window $w$). Severity or score: $S_t$ with defined components. Define $\mu_{t,w}$, $\sigma_{t,w}$ in text.

## Avoid

- Em dash or en dash in math or text (use hyphen).
- Conflicting use of $k$ (e.g. both client index and time step).
- Undefined symbols. When in doubt, add a short phrase: "where $N$ is the number of nodes."
