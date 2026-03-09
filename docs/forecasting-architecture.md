# Forecasting Architecture

This document describes the production model path and the role of each component in the IRIDIUM forecasting engine.

## Overview

The forecasting engine provides short-horizon congestion (and related) forecasts for the urban mobility digital twin. The **primary production model** is **Graph WaveNet**. **DCRNN** is a benchmark and comparison baseline. **Simple baselines** (persistence, rolling mean, linear temporal) are first-class for sanity checking and fallback. The **deterministic heuristic** from the current twin state remains the operational fallback when no trained artifact or insufficient history is available.

## Production Model Path

1. **Task definition** (`forecasting/task.py`): Canonical spec for target (e.g. congestion score), horizon, granularity (edge-level), input window, and degraded-mode policy.
2. **Data**: Dataset builder assembles time-aligned series from digital twin snapshots (and optional weather/transit). No synthetic data in the production path.
3. **Graph**: Graph construction from the actual network (nodes, edges) produces adjacency and normalized support matrices. Versioned and reproducible.
4. **Features**: Deterministic, versioned feature pipeline (lags, rolling stats, time encoding). Same logic for training and inference.
5. **Model**: Graph WaveNet is the main model; DCRNN and simple baselines are used for comparison and fallback.
6. **Training**: Config-driven training with temporal train/val/test split, checkpoints, and early stopping. Fails gracefully when data is insufficient.
7. **Inference**: Production-safe wrapper returns predictions with model/dataset/feature version, coverage note, and degraded flag. Never returns fake forecasts when the artifact is missing.
8. **Registry**: Every artifact has metadata (family, version, dataset/feature/graph version, maturity). Serving does not load without validation.

## Why Graph WaveNet

Graph WaveNet combines (1) **adaptive adjacency** learned from data, so hidden spatial dependencies are captured beyond the physical graph, and (2) **dilated temporal convolutions** for long-range temporal context without RNN overhead. It is a strong open-source foundation for spatio-temporal traffic forecasting and aligns with IRIDIUM's need for edge-level, short-horizon predictions.

## Why DCRNN and Simple Baselines

DCRNN provides a recurrent baseline with diffusion convolution; it uses the same inputs and outputs as Graph WaveNet for fair comparison. Simple baselines (persistence, rolling mean, linear trend) are mandatory for sanity checks and for explicit fallback when the learned model is unavailable or coverage is low.

## Degraded Mode

When the trained artifact is missing, coverage is below the configured minimum, or labels are insufficient, the system does not return learned predictions. The API returns **deterministic_baseline** (heuristic from twin) or an explicit **unavailable** status. No silent substitution of fake intelligence.

## Active vs Experimental

- **Active production path**: Graph WaveNet (when artifact and history are available), deterministic heuristic baseline, simple statistical baselines in evaluation.
- **Benchmark only**: DCRNN (not used for serving unless explicitly promoted).
- **Experimental**: Federated learning (Flower) in `services/forecasting/federated/`; not in the default runtime path.
