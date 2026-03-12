# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 08:48:03 2025

@author: david
"""

from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Dict
import yaml

LOGGER_NAME = "agri_etl"

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler()
        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def project_paths() -> dict[str, Path]:
    root = Path.cwd()
    return {"root": root, "input": root / "input", "outputs": root / "outputs", "cache": root / "cache", "schema": root / "schema"}


def data_year(period_or_vintage: int, model_periods: list[int]) -> int:
    """Return the representative data year for a model period/vintage.

    End-of-period convention: each model period uses data from the **start of
    the next** model period (i.e. the end of the current period).  For the
    last model period the step size is inferred from the two preceding entries.

    Pre-existing vintages (before the first model period) return the same year.
    """
    if period_or_vintage < model_periods[0]:
        return period_or_vintage
    try:
        idx = model_periods.index(period_or_vintage)
    except ValueError:
        return period_or_vintage
    if idx < len(model_periods) - 1:
        return model_periods[idx + 1]
    # Last period: infer step from the preceding gap
    step = (model_periods[-1] - model_periods[-2]) if len(model_periods) > 1 else 5
    return model_periods[-1] + step