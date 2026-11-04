"""Anthropic Messages API adapter (claude-haiku-5-5).

Settings (design 5.5): thinking disabled, which Haiku 5.5 accepts at effort
high or below; effort set explicitly to its default "medium"; no temperature
(the API rejects sampling parameters on this model). Parallel tool use off.
"""
from __future__ import annotations

import os
from typing import Any

from .. import prompts
from ..config import MAX_OUTPUT_TOKENS
from .base import (Adapter, BillingError, Normalized, PermanentError, RateLimitError,
                   TransientError, looks_like_billing)

EFFORT = "medium"


def _tools() -> list[dict]:
    return [{"name": t["name"], "description": t["description"], "input_schema": t["parameters"]}
            for t in prompts.TOOLS]


class AnthropicAdapter(Adapter):
    provider = "anthropic"
    supports_batch = True

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import anthropic
            key = os.environ.get("ANTHROPIC_API_KEY")
            if not key:
                raise PermanentError("ANTHROPIC_API_KEY is not set (check .env)")
            self._client = anthropic.Anthropic(api_key=key, max_retries=2, timeout=120)
        return self._client

    def request_settings(self) -> dict:
        return {"thinking": "disabled", "effort": EFFORT, "temperature": "not sent",
                "tool_choice": self.tool_choice, "parallel_tool_use": False,
                "max_tokens": MAX_OUTPUT_TOKENS}

    def build_request(self, conv: dict) -> dict:
        messages: list[dict] = [{"role": "user", "content": conv["user"]}]
        for h in conv.get("history", []):
            messages.append({"role": "assistant", "content": h["assistant_native"]})
            messages.append({"role": "user", "content": [{
                "type": "tool_result", "tool_use_id": h["tool_call"]["id"], "content": h["tool_reply"]}]})
        tc = {"type": "any" if self.tool_choice == "required" else "auto", "disable_parallel_tool_use": True}
        return {
            "model": self.model,
            "max_tokens": MAX_OUTPUT_TOKENS,
            "system": conv["system"],
            "messages": messages,
            "tools": _tools(),
            "tool_choice": tc,
            "thinking": {"type": "disabled"},
            "output_config": {"effort": EFFORT},
        }

    # ---- errors ----
    def _map_error(self, e: Exception) -> Exception:
        import anthropic
        msg = str(e)
        if looks_like_billing(msg):
            return BillingError(msg)
        if isinstance(e, anthropic.RateLimitError):
            ra = None
            try:
                ra = float(e.response.headers.get("retry-after"))
            except Exception:
                pass
            return RateLimitError(msg, ra)
        if isinstance(e, (anthropic.APIConnectionError, anthropic.APITimeoutError, anthropic.InternalServerError)):
            return TransientError(msg)
        if isinstance(e, anthropic.APIStatusError):
            if e.status_code in (402,):
                return BillingError(msg)
            if e.status_code >= 500 or e.status_code == 529:
                return TransientError(msg)
            return PermanentError(msg)
        return TransientError(msg)

    def call(self, payload: dict) -> dict:
        try:
            msg = self.client.messages.create(**payload)
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        return msg.model_dump(mode="json")

    # ---- batch ----
    def submit_batch(self, items: list[tuple[str, dict]], label: str) -> str:
        try:
            b = self.client.messages.batches.create(
                requests=[{"custom_id": cid, "params": p} for cid, p in items])
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        return b.id

    def poll_batch(self, batch_id: str) -> str:
        try:
            b = self.client.messages.batches.retrieve(batch_id)
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        return "ended" if b.processing_status == "ended" else "running"

    def fetch_batch(self, batch_id: str, order: list[str] | None = None) -> dict[str, tuple[str, Any]]:
        out: dict[str, tuple[str, Any]] = {}
        try:
            for r in self.client.messages.batches.results(batch_id):
                t = r.result.type
                if t == "succeeded":
                    out[r.custom_id] = ("ok", r.result.message.model_dump(mode="json"))
                elif t == "errored":
                    err = r.result.error.model_dump(mode="json") if hasattr(r.result.error, "model_dump") else str(r.result.error)
                    if looks_like_billing(str(err)):
                        raise BillingError(str(err))
                    out[r.custom_id] = ("error", str(err))
                else:
                    out[r.custom_id] = ("error", t)  # canceled / expired: resubmitted on resume
        except BillingError:
            raise
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        return out

    # ---- response ----
    def normalize(self, raw: dict) -> Normalized:
        content = raw.get("content") or []
        calls, texts = [], []
        for b in content:
            if b.get("type") == "tool_use":
                calls.append({"id": b.get("id"), "name": b.get("name"), "args": b.get("input") or {}})
            elif b.get("type") == "text":
                texts.append(b.get("text") or "")
        stop = raw.get("stop_reason")
        status = "ok"
        if stop == "refusal":
            status = "refusal"
        elif stop == "max_tokens" and not calls:
            status = "truncated"
        u = raw.get("usage") or {}
        usage = {"input_tokens": u.get("input_tokens", 0) or 0,
                 "output_tokens": u.get("output_tokens", 0) or 0,
                 "cache_read_input_tokens": u.get("cache_read_input_tokens", 0) or 0}
        native = [_block_param(b) for b in content
                  if b.get("type") == "tool_use" or (b.get("type") == "text" and (b.get("text") or "").strip())]
        return Normalized(status=status, tool_calls=calls, text="\n".join(texts).strip(),
                          model_returned=raw.get("model"), stop_reason=stop, usage=usage,
                          assistant_native=native)


def _block_param(b: dict) -> dict:
    if b["type"] == "text":
        return {"type": "text", "text": b.get("text", "")}
    return {"type": "tool_use", "id": b["id"], "name": b["name"], "input": b.get("input") or {}}
