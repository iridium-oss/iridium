# Symbol Glossary

Standard symbols used in IRIDIUM documentation and formulas. Use the same meaning everywhere.

## Graph and network

| Symbol | Meaning | Unit or interpretation |
|--------|---------|------------------------|
| $G$ | Mobility graph | Graph object |
| $V$ | Set of nodes (segments, junctions, stops) | |
| $E$ | Set of edges | |
| $W$ | Edge weights (e.g. travel time, cost) | Optional |
| $N$ | Number of nodes, $|V|$ | Dimensionless |
| $F$ | Number of features per node | Dimensionless |

## Time and forecasting

| Symbol | Meaning | Unit or interpretation |
|--------|---------|------------------------|
| $t$ | Current time step or timestamp | Index or datetime |
| $T$ | Input window length (number of past steps) | Steps |
| $H$ | Forecast horizon (number of future steps) | Steps |
| $X_t$ | Feature matrix at time $t$ | $\mathbb{R}^{N \times F}$ |
| $\hat{Y}_{t+1:t+H}$ | Forecast for next $H$ steps | Same as target |
| $y_{i,t+h}$ | Observed value for entity $i$ at $t+h$ | Depends on target |
| $\hat{y}_{i,t+h}$ | Predicted value | Same as $y$ |

## Federated learning

| Symbol | Meaning | Unit or interpretation |
|--------|---------|------------------------|
| $K$ | Number of clients or participants | Dimensionless |
| $k$ | Client index, $k \in \{1,\ldots,K\}$ | |
| $p_k$ | Weight of client $k$ (e.g. $n_k / \sum_j n_j$) | Fraction |
| $n_k$ | Local sample count at client $k$ | Count |
| $\theta$ | Model parameters | Vector |
| $\theta_k^{(t)}$ | Parameters at client $k$ after round $t$ | |
| $\mathcal{L}_k$ | Local loss at client $k$ | Scalar |

## Routing

| Symbol | Meaning | Unit or interpretation |
|--------|---------|------------------------|
| $r$ | A route (path or itinerary) | |
| $J(r)$ | Route utility or cost to minimise | Scalar |
| $T(r)$ | Travel time along $r$ | Minutes or seconds |
| $C(r)$ | Monetary or generalised cost | Currency or dimensionless |
| $E(r)$ | Emissions proxy (e.g. carbon) | kg CO2 or equivalent |
| $P(r)$ | Transfer or accessibility penalty | Dimensionless |
| $\alpha, \beta, \gamma, \delta$ | Weights in $J(r)$ | Non-negative |

## Equity

| Symbol | Meaning | Unit or interpretation |
|--------|---------|------------------------|
| $d$ | District or zone index | |
| $m$ | Indicator index | |
| $x_{d,m}$ | Raw value of indicator $m$ in district $d$ | Depends on indicator |
| $\mu_m, \sigma_m$ | Mean and std of indicator $m$ (e.g. over districts) | Same as $x_{d,m}$ |
| $z_{d,m}$ | Normalised value, e.g. $(x_{d,m} - \mu_m) / \sigma_m$ | Dimensionless |
| $w_m$ | Weight of indicator $m$ | Non-negative, sum to 1 |
| $MES_d$ | Mobility Equity Score for district $d$ | Composite, 0-1 or similar |

## Anomaly detection

| Symbol | Meaning | Unit or interpretation |
|--------|---------|------------------------|
| $x_t$ | Observed signal at time $t$ | Depends on sensor |
| $\mu_{t,w}$ | Rolling mean over window $w$ ending at $t$ | Same as $x_t$ |
| $\sigma_{t,w}$ | Rolling standard deviation | Same as $x_t$ |
| $z_t$ | Z-score or standardised deviation | Dimensionless |
| $S_t$ | Anomaly severity or score | Dimensionless |

## Evaluation metrics

| Symbol | Meaning | Formula or interpretation |
|--------|---------|----------------------------|
| MAE | Mean Absolute Error | $\frac{1}{n}\sum_i |y_i - \hat{y}_i|$ |
| RMSE | Root Mean Square Error | $\sqrt{\frac{1}{n}\sum_i (y_i - \hat{y}_i)^2}$ |
| MAPE | Mean Absolute Percentage Error | $\frac{100}{n}\sum_i \left|\frac{y_i - \hat{y}_i}{y_i}\right|$ (when $y_i \neq 0$) |
