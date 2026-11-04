"""Paths, model registry, prices and spend caps for the agent harness.

Prices are per million tokens, copied from the research notes
(DS480/notes/Paper 2 research (11-3)/models_cost.md, checked 11/3/2026).
They are used only for the running cost estimate in logs/spend.json.
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
LOGS = ROOT / "logs"
ENV_FILE = ROOT / ".env"
SPEND_FILE = LOGS / "spend.json"

SEED = 480

# Hard caps in US dollars, per provider (Ian's rules, 11/4).
CAPS_USD = {"anthropic": 15.0, "openai": 10.0, "google": 0.0, "ollama": 0.0}

# key -> provider settings. "std" and "batch" are (input, output) $/MTok.
MODELS = {
    "haiku": {
        "provider": "anthropic",
        "model": "claude-haiku-5-5",
        "std": (0.10, 0.50),
        "batch": (0.05, 0.25),
        # Claude 4.7+ tokenizers count about 30% more tokens for the same text.
        "token_factor": 1.3,
        "batch_api": True,
    },
    "luna": {
        "provider": "openai",
        "model": "gpt-6-luna",
        "std": (0.10, 0.50),
        "batch": (0.05, 0.25),  # Batch and Flex
        "token_factor": 1.0,
        "batch_api": True,
    },
    "flashlite": {
        "provider": "google",
        "model": "gemini-3.5-flash-lite",
        "std": (0.30, 2.50),
        "batch": (0.15, 1.25),
        "token_factor": 1.0,
        "batch_api": True,
        # Free tier: nothing is billed. Notional cost is still tracked.
        "free_tier": True,
    },
    "olmo": {
        "provider": "ollama",
        "model": "olmo-3:7b-instruct",
        "std": (0.0, 0.0),
        "batch": (0.0, 0.0),
        "token_factor": 1.0,
        "batch_api": False,
        "local": True,
    },
}

MAX_OUTPUT_TOKENS = 512

# Ollama settings (design 5.5): temperature 0, fixed seed, 16K context.
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_OPTIONS = {"temperature": 0, "seed": SEED, "num_ctx": 16384}

# Local heavy compute is allowed only in this window, US Eastern time
# (Ian's rule: no loud fan while he is in class).
LOCAL_ALLOWED_START_HOUR = 19  # 7 pm ET
LOCAL_ALLOWED_END_HOUR = 7     # 7 am ET


def load_env() -> None:
    """Load API keys from .env into os.environ without printing anything."""
    try:
        from dotenv import load_dotenv
    except ImportError:  # pragma: no cover
        return
    if ENV_FILE.exists():
        load_dotenv(ENV_FILE, override=False)


def secret_values() -> list[str]:
    """The key values currently in the environment, for redaction checks."""
    out = []
    for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
        v = os.environ.get(k)
        if v and len(v) > 8:
            out.append(v)
    return out
