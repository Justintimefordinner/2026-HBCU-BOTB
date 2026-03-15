"""Compatibility shim so Streamlit can import config from the dashboard directory."""

from __future__ import annotations

import importlib.util
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config.py"

if not CONFIG_PATH.exists():  # pragma: no cover
    raise ModuleNotFoundError(f"Could not find project config at {CONFIG_PATH}")

spec = importlib.util.spec_from_file_location("_root_config", CONFIG_PATH)
if spec is None or spec.loader is None:  # pragma: no cover
    raise ImportError(f"Could not load config module from {CONFIG_PATH}")

_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_module)

DEBUG_MODE = _module.DEBUG_MODE
ANTHROPIC_API_KEY = _module.ANTHROPIC_API_KEY
MODEL_NAME = _module.MODEL_NAME
QUERY_TEMPLATES = _module.QUERY_TEMPLATES
