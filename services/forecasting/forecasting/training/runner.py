"""
Config-driven training pipeline. Checkpoints, metadata, temporal splits, early stopping.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import numpy as np
import torch

from ..models.dcrnn import DCRNN
from ..models.graph_wavenet import GraphWaveNet
from ..task import ForecastingTaskSpec

logger = logging.getLogger(__name__)


def _temporal_split(
    n: int,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> tuple[slice, slice, slice]:
    t = train_ratio + val_ratio + test_ratio
    train_ratio, val_ratio, test_ratio = train_ratio / t, val_ratio / t, test_ratio / t
    t1 = int(n * train_ratio)
    t2 = int(n * (train_ratio + val_ratio))
    return slice(0, t1), slice(t1, t2), slice(t2, n)


def run_training(
    data_array: np.ndarray,
    support: np.ndarray,
    entity_order: list[str],
    task_spec: ForecastingTaskSpec | None = None,
    config: dict[str, Any] | None = None,
    model_family: str = "graph_wavenet",
    artifact_dir: Path | None = None,
) -> dict[str, Any]:
    """
    Train model on real data. Saves checkpoint and metadata. Returns training summary.
    If data is insufficient (e.g. too few steps), returns error summary and does not save artifact.
    """
    task_spec = task_spec or ForecastingTaskSpec()
    config = config or {}
    model_cfg = config.get("model", {})
    train_cfg = config.get("training", {})
    batch_size = train_cfg.get("batch_size", 32)
    epochs = train_cfg.get("epochs", 100)
    lr = train_cfg.get("learning_rate", 0.001)
    seed = train_cfg.get("seed", 42)
    train_ratio = train_cfg.get("train_ratio", 0.7)
    val_ratio = train_cfg.get("val_ratio", 0.15)
    test_ratio = train_cfg.get("test_ratio", 0.15)
    patience = train_cfg.get("early_stopping_patience", 10)

    torch.manual_seed(seed)
    np.random.seed(seed)

    T, N = data_array.shape
    input_len = task_spec.input_window_steps
    horizon = task_spec.horizon_steps
    if input_len + horizon + 10 > T:
        logger.warning("Insufficient timesteps for training; T=%s", T)
        return {"status": "insufficient_data", "T": T, "required": input_len + horizon + 10}
    if support.shape[0] != N:
        return {"status": "mismatch", "message": "support shape does not match data"}

    train_sl, val_sl, test_sl = _temporal_split(T, train_ratio, val_ratio, test_ratio)
    num_nodes = model_cfg.get("num_nodes", N)
    if num_nodes != N:
        return {"status": "mismatch", "message": "config num_nodes does not match data"}

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    support_t = torch.from_numpy(support.astype(np.float32)).to(device)

    if model_family == "graph_wavenet":
        model = GraphWaveNet(
            num_nodes=N,
            input_len=input_len,
            horizon=horizon,
            hidden_dim=model_cfg.get("hidden_dim", 32),
            num_layers=model_cfg.get("num_layers", 4),
            dropout=model_cfg.get("dropout", 0.3),
        ).to(device)
    elif model_family == "dcrnn":
        model = DCRNN(
            num_nodes=N,
            input_len=input_len,
            horizon=horizon,
            hidden_dim=model_cfg.get("hidden_dim", 32),
            num_layers=model_cfg.get("num_layers", 2),
            dropout=model_cfg.get("dropout", 0.3),
        ).to(device)
    else:
        return {"status": "unknown_model", "model_family": model_family}

    opt = torch.optim.Adam(model.parameters(), lr=lr)
    best_val = float("inf")
    best_epoch = 0
    history: list[float] = []
    last_epoch = 0

    for epoch in range(epochs):
        last_epoch = epoch
        model.train()
        train_loss = 0.0
        count = 0
        for start in range(train_sl.start, train_sl.stop - input_len - horizon):
            end = start + input_len
            x = data_array[start:end]
            y = data_array[end : end + horizon]
            if np.any(np.isnan(x)) or np.any(np.isnan(y)):
                continue
            x_t = torch.from_numpy(x.astype(np.float32)).unsqueeze(0).to(device)
            y_t = torch.from_numpy(y.astype(np.float32)).unsqueeze(0).to(device)
            pred = model(x_t, support=support_t)
            loss = torch.nn.functional.mse_loss(pred, y_t)
            opt.zero_grad()
            loss.backward()
            opt.step()
            train_loss += loss.item()
            count += 1
        if count:
            train_loss /= count
        history.append(train_loss)

        model.eval()
        val_loss = 0.0
        vc = 0
        with torch.no_grad():
            for start in range(val_sl.start, val_sl.stop - input_len - horizon):
                end = start + input_len
                x = data_array[start:end]
                y = data_array[end : end + horizon]
                if np.any(np.isnan(x)) or np.any(np.isnan(y)):
                    continue
                x_t = torch.from_numpy(x.astype(np.float32)).unsqueeze(0).to(device)
                y_t = torch.from_numpy(y.astype(np.float32)).unsqueeze(0).to(device)
                pred = model(x_t, support=support_t)
                val_loss += torch.nn.functional.mse_loss(pred, y_t).item()
                vc += 1
        if vc:
            val_loss /= vc
        if val_loss < best_val:
            best_val = val_loss
            best_epoch = epoch
            if artifact_dir:
                artifact_dir = Path(artifact_dir)
                artifact_dir.mkdir(parents=True, exist_ok=True)
                torch.save(
                    {
                        "model_state": model.state_dict(),
                        "config": config,
                        "model_family": model_family,
                        "num_nodes": N,
                        "input_len": input_len,
                        "horizon": horizon,
                    },
                    artifact_dir / "checkpoint.pt",
                )
        if patience and (epoch - best_epoch) >= patience:
            logger.info("Early stopping at epoch %s", epoch)
            break

    summary = {
        "status": "completed",
        "model_family": model_family,
        "best_val_mse": best_val,
        "best_epoch": best_epoch,
        "epochs_run": last_epoch + 1,
        "train_history": history,
    }
    if artifact_dir:
        meta_path = Path(artifact_dir) / "training_metadata.json"
        with open(meta_path, "w") as f:
            json.dump(summary, f, indent=2)
    return summary
