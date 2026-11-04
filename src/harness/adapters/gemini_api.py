"""Gemini API adapter (gemini-3.5-flash-lite, free tier only).

Settings: thinking left at the model default ("minimal" per the AI Studio docs,
unverified here; thought tokens are logged so it can be checked); no
temperature sent; automatic function calling off; function calling mode ANY
(forced) or AUTO. 429s are retried with backoff, honoring the server's
retryDelay. Free tier means nothing is billed; the spend guard tracks a
notional cost only and refuses any paid use (Google cap is $0).
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from typing import Any

from .. import prompts
from ..config import MAX_OUTPUT_TOKENS
from .base import (Adapter, BillingError, Normalized, PermanentError, RateLimitError,
                   TransientError, looks_like_billing)


def _tools() -> list[dict]:
    return [{"function_declarations": [
        {"name": t["name"], "description": t["description"], "parameters_json_schema": t["parameters"]}
        for t in prompts.TOOLS]}]


class GeminiAdapter(Adapter):
    provider = "google"
    supports_batch = True

    def __init__(self, *a, min_interval_s: float = 4.5, **kw):
        super().__init__(*a, **kw)
        self._client = None
        self.min_interval_s = min_interval_s  # simple client-side pacing for the free tier
        self._last = 0.0
        self._pace_lock = threading.Lock()

    @property
    def client(self):
        if self._client is None:
            from google import genai
            key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if not key:
                raise PermanentError("GEMINI_API_KEY is not set (check .env)")
            self._client = genai.Client(api_key=key)
        return self._client

    def request_settings(self) -> dict:
        return {"thinking": "model default", "temperature": "not sent", "tool_choice": self.tool_choice,
                "automatic_function_calling": "disabled", "max_output_tokens": MAX_OUTPUT_TOKENS,
                "tier": "free"}

    def _config(self, system: str) -> dict:
        return {
            "system_instruction": system,
            "tools": _tools(),
            "tool_config": {"function_calling_config": {"mode": "ANY" if self.tool_choice == "required" else "AUTO"}},
            "automatic_function_calling": {"disable": True},
            "max_output_tokens": MAX_OUTPUT_TOKENS,
        }

    def build_request(self, conv: dict) -> dict:
        contents: list[dict] = [{"role": "user", "parts": [{"text": conv["user"]}]}]
        for h in conv.get("history", []):
            contents.append(h["assistant_native"])
            fr = {"name": h["tool_call"]["name"], "response": {"result": h["tool_reply"]}}
            if h["tool_call"].get("id"):
                fr["id"] = h["tool_call"]["id"]
            contents.append({"role": "user", "parts": [{"function_response": fr}]})
        return {"model": self.model, "contents": contents, "config": self._config(conv["system"])}

    @staticmethod
    def _typed(payload: dict):
        from google.genai import types
        contents = [types.Content.model_validate_json(json.dumps(c)) for c in payload["contents"]]
        config = types.GenerateContentConfig.model_validate(payload["config"])
        return contents, config

    def _map_error(self, e: Exception) -> Exception:
        from google.genai import errors
        msg = str(e)
        if looks_like_billing(msg) and "free" not in msg.lower():
            return BillingError(msg)
        if isinstance(e, errors.APIError):
            code = getattr(e, "code", None)
            if code == 429:
                m = re.search(r"retry(?:Delay| in)['\"]?\s*[:=]?\s*['\"]?([\d.]+)s", msg)
                return RateLimitError(msg, float(m.group(1)) if m else None)
            if code in (402,):
                return BillingError(msg)
            if code and code >= 500:
                return TransientError(msg)
            return PermanentError(msg)
        return TransientError(msg)

    def _pace(self):
        with self._pace_lock:  # shared across worker threads
            wait = self.min_interval_s - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()

    def call(self, payload: dict) -> dict:
        contents, config = self._typed(payload)
        self._pace()
        try:
            r = self.client.models.generate_content(model=payload["model"], contents=contents, config=config)
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        return r.model_dump(mode="json", exclude_none=True, exclude={"sdk_http_response"})

    # ---- batch (inline requests) ----
    def submit_batch(self, items: list[tuple[str, dict]], label: str) -> str:
        from google.genai import types
        reqs = []
        for cid, p in items:
            contents, config = self._typed(p)
            reqs.append(types.InlinedRequest(contents=contents, config=config, metadata={"custom_id": cid}))
        try:
            job = self.client.batches.create(model=items[0][1]["model"], src=reqs,
                                             config={"display_name": label[:120]})
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        return job.name

    def poll_batch(self, batch_id: str) -> str:
        try:
            job = self.client.batches.get(name=batch_id)
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        st = str(job.state.name if hasattr(job.state, "name") else job.state)
        if st in ("JOB_STATE_SUCCEEDED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"):
            return "ended"
        if st == "JOB_STATE_FAILED":
            if job.error and looks_like_billing(str(job.error)):
                raise BillingError(str(job.error))
            return "failed"
        return "running"

    def fetch_batch(self, batch_id: str, order: list[str] | None = None) -> dict[str, tuple[str, Any]]:
        try:
            job = self.client.batches.get(name=batch_id)
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        out: dict[str, tuple[str, Any]] = {}
        resps = (job.dest.inlined_responses if job.dest else None) or []
        for i, r in enumerate(resps):
            cid = (r.metadata or {}).get("custom_id") if r.metadata else None
            if cid is None and order and i < len(order):
                cid = order[i]
            if cid is None:
                continue
            if r.error:
                err = str(r.error)
                if looks_like_billing(err):
                    raise BillingError(err)
                out[cid] = ("error", err)
            else:
                out[cid] = ("ok", r.response.model_dump(mode="json", exclude_none=True,
                                                        exclude={"sdk_http_response"}))
        return out

    # ---- response ----
    def normalize(self, raw: dict) -> Normalized:
        cands = raw.get("candidates") or []
        pf = raw.get("prompt_feedback") or {}
        u = raw.get("usage_metadata") or {}
        usage = {"input_tokens": u.get("prompt_token_count", 0) or 0,
                 "output_tokens": (u.get("candidates_token_count", 0) or 0) + (u.get("thoughts_token_count", 0) or 0),
                 "thinking_tokens": u.get("thoughts_token_count", 0) or 0}
        model_ret = raw.get("model_version")
        if not cands:
            st = "refusal" if pf.get("block_reason") else "error"
            return Normalized(status=st, model_returned=model_ret, stop_reason=pf.get("block_reason"),
                              usage=usage, error=None if st == "refusal" else "no candidates")
        c = cands[0]
        content = c.get("content") or {"role": "model", "parts": []}
        calls, texts = [], []
        for part in content.get("parts") or []:
            if part.get("function_call"):
                fc = part["function_call"]
                calls.append({"id": fc.get("id"), "name": fc.get("name"), "args": fc.get("args") or {}})
            elif part.get("text") and not part.get("thought"):
                texts.append(part["text"])
        fr = c.get("finish_reason")
        status = "ok"
        if fr in ("SAFETY", "PROHIBITED_CONTENT", "BLOCKLIST", "SPII", "RECITATION") and not calls:
            status = "refusal"
        elif fr == "MAX_TOKENS" and not calls:
            status = "truncated"
        if "role" not in content:
            content = dict(content, role="model")
        return Normalized(status=status, tool_calls=calls, text="\n".join(texts).strip(),
                          model_returned=model_ret, stop_reason=fr, usage=usage, assistant_native=content)
