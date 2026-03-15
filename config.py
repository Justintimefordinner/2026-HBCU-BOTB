"""Central configuration for the AISLED prototype."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    # If python-dotenv isn't installed, we can still run as long as env vars are set.
    def load_dotenv(*args, **kwargs):
        return False

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"
SECRETS_FILES = (
    PROJECT_ROOT / ".streamlit" / "secrets.toml",
    PROJECT_ROOT / "secrets.toml",
)

# Load .env from the repo root without overriding real environment variables.
load_dotenv(ENV_FILE, override=False)


def _read_secrets_file() -> dict[str, Any]:
    """Load the first available TOML secrets file, if present."""
    if tomllib is None:
        return {}

    for secrets_file in SECRETS_FILES:
        if not secrets_file.exists():
            continue
        with secrets_file.open("rb") as handle:
            data = tomllib.load(handle)
        if isinstance(data, dict):
            return data
    return {}


def _read_streamlit_secrets() -> dict[str, Any]:
    """Read deployment secrets from Streamlit when available."""
    try:
        import streamlit as st
    except ImportError:  # pragma: no cover
        return {}

    try:
        return dict(st.secrets)
    except Exception:  # pragma: no cover
        return {}


_SECRETS = _read_secrets_file()
_STREAMLIT_SECRETS = _read_streamlit_secrets()


def _lookup_setting(name: str, default: str = "") -> str:
    """Resolve config values from env, Streamlit secrets, then TOML secrets."""
    value = os.getenv(name)
    if value:
        return value

    value = _STREAMLIT_SECRETS.get(name)
    if value not in (None, ""):
        return str(value)

    value = _SECRETS.get(name)
    if value not in (None, ""):
        return str(value)

    return default


DEBUG_MODE = _lookup_setting("DEBUG_MODE", "0").lower() in {"1", "true", "yes", "on"}
ANTHROPIC_API_KEY = _lookup_setting("ANTHROPIC_API_KEY")
MODEL_NAME = _lookup_setting("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

QUERY_TEMPLATES = [
    "What are the best {category} under ${price_ceiling}?",
    "Recommend a good {category} for someone on a budget.",
    "What {category} do most people buy online?",
    "Is {brand} {product_name} a good choice for {category}?",
    "How does {brand} {product_name} compare to {brand} {product_name}?",
]
