"""Provider-neutral adapter interface.

A Conversation is what the runner knows about an episode so far:
  system: str
  user: str                         first user message (request + store page)
  history: list of {"assistant_native": <provider-native assistant turn>,
                    "tool_call": {"id", "name", "args"},
                    "tool_reply": str}
Adapters turn that into a native request payload (a JSON-serializable dict),
send it (sync or batch), and normalize the raw response dict.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


# ---------------- errors ----------------
class ProviderError(Exception):
    """Base class. `retryable` errors are retried by the runner."""
    retryable = False


class BillingError(ProviderError):
    """Out of credits, billing not set up, quota tied to payment. Halts the provider."""


class RateLimitError(ProviderError):
    retryable = True

    def __init__(self, msg: str, retry_after: float | None = None):
        super().__init__(msg)
        self.retry_after = retry_after


class TransientError(ProviderError):
    retryable = True


class PermanentError(ProviderError):
    """Bad request etc. Logged as an error outcome for that turn."""


BILLING_PATTERNS = re.compile(
    r"credit balance|no credits|credits remaining|insufficient_quota|exceeded your current quota|"
    r"billing|payment required|purchase credits|spend limit|spending limit|account is not active|"
    r"prepayment|top up",
    re.I,
)


def looks_like_billing(msg: str) -> bool:
    return bool(BILLING_PATTERNS.search(msg or ""))


# ---------------- normalized response ----------------
@dataclass
class Normalized:
    status: str                      # ok | refusal | truncated | error
    tool_calls: list[dict] = field(default_factory=list)   # [{"id","name","args"}]
    text: str = ""
    model_returned: str | None = None
    stop_reason: str | None = None
    usage: dict = field(default_factory=dict)              # input_tokens, output_tokens, thinking_tokens
    assistant_native: Any = None
    error: str | None = None


def parse_action(norm: Normalized, valid_ids: list[str]) -> dict:
    """Map a normalized response to one action. The first tool call wins; any
    extra calls are kept for the log."""
    if norm.status == "error":
        return {"type": "error", "detail": norm.error}
    if norm.status == "refusal":
        return {"type": "refusal", "text": norm.text}
    calls = norm.tool_calls
    if not calls:
        # Some local models write the call as JSON text. Try to recover it.
        rec = recover_call_from_text(norm.text)
        if rec:
            calls = [rec]
        else:
            t = "truncated" if norm.status == "truncated" else "no_tool_call"
            return {"type": t, "text": norm.text}
    first = calls[0]
    extra = calls[1:]
    name, args = first.get("name"), first.get("args") or {}
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except json.JSONDecodeError:
            args = {"_raw": args}
    out: dict
    if name == "buy":
        pid = str(args.get("product_id", "")).strip()
        out = {"type": "buy", "product_id": pid, "valid": pid in valid_ids}
    elif name == "ask_user":
        out = {"type": "ask", "question": str(args.get("question", ""))}
    else:
        out = {"type": "unknown_tool", "name": name, "args": args}
    out["call_id"] = first.get("id")
    out["call_name"] = name
    if norm.text:
        out["text"] = norm.text
    if extra:
        out["extra_tool_calls"] = extra
    if first.get("recovered_from_text"):
        out["recovered_from_text"] = True
    return out


_JSON_OBJ = re.compile(r"\{.*\}", re.S)


def recover_call_from_text(text: str) -> dict | None:
    if not text:
        return None
    m = _JSON_OBJ.search(text)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None
    name = obj.get("name") or obj.get("tool") or obj.get("function")
    args = obj.get("arguments") or obj.get("parameters") or obj.get("args") or {}
    if name in ("buy", "ask_user") and isinstance(args, dict):
        return {"id": None, "name": name, "args": args, "recovered_from_text": True}
    return None


# ---------------- adapter interface ----------------
class Adapter:
    provider: str = "base"
    supports_batch: bool = False

    def __init__(self, model_key: str, settings: dict, tool_choice: str = "required"):
        self.model_key = model_key
        self.settings = settings
        self.model = settings["model"]
        self.tool_choice = tool_choice  # "required" (forced tool call) or "auto"

    # request side
    def build_request(self, conv: dict) -> dict:
        raise NotImplementedError

    def request_settings(self) -> dict:
        """Settings worth logging next to every call (no secrets)."""
        return {}

    # sync
    def call(self, payload: dict) -> dict:
        raise NotImplementedError

    # batch
    def submit_batch(self, items: list[tuple[str, dict]], label: str) -> str:
        raise NotImplementedError

    def poll_batch(self, batch_id: str) -> str:
        """Return 'running', 'ended' or 'failed'."""
        raise NotImplementedError

    def fetch_batch(self, batch_id: str, order: list[str] | None = None) -> dict[str, tuple[str, Any]]:
        """custom_id -> ("ok", raw_dict) or ("error", message)."""
        raise NotImplementedError

    # response side
    def normalize(self, raw: dict) -> Normalized:
        raise NotImplementedError

    # helpers
    def estimate_input_tokens(self, payload: dict) -> int:
        chars = len(json.dumps(payload))
        return int(chars / 3.0 * self.settings.get("token_factor", 1.0)) + 50
