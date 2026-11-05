"""OpenAI Responses API adapter (gpt-6-luna).

Settings (design 5.5): reasoning effort "none"; no temperature sent (left at
the default so it matches the other API models); parallel tool calls off;
store=False. Sync calls can use the Flex tier (batch prices); big grids use the
Batch API on /v1/responses.

The OpenAI account had $0 loaded on 11/4. Any billing or credit error raises
BillingError, which halts the provider in logs/spend.json.
"""
from __future__ import annotations

import io
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
    return [{"type": "function", "name": t["name"], "description": t["description"],
             "parameters": t["parameters"], "strict": True} for t in prompts.TOOLS]


class OpenAIAdapter(Adapter):
    provider = "openai"
    supports_batch = True

    def __init__(self, *a, service_tier: str | None = None, **kw):
        super().__init__(*a, **kw)
        self.service_tier = service_tier  # None or "flex"
        self._client = None
        # Client-side pacing for sync calls. The account's free access is 10 requests
        # per minute on gpt-6-luna (429 message, 11/4), so 6.5 s between calls.
        self.min_interval_s = float(self.settings.get("min_interval_s", 0.0))
        self._last = 0.0
        self._pace_lock = threading.Lock()

    def _pace(self):
        if self.min_interval_s <= 0:
            return
        with self._pace_lock:
            wait = self.min_interval_s - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()

    @property
    def client(self):
        if self._client is None:
            import openai
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                raise PermanentError("OPENAI_API_KEY is not set (check .env)")
            self._client = openai.OpenAI(api_key=key, max_retries=2,
                                         timeout=900 if self.service_tier == "flex" else 120)
        return self._client

    def request_settings(self) -> dict:
        return {"reasoning_effort": "none", "temperature": "not sent", "tool_choice": self.tool_choice,
                "parallel_tool_calls": False, "store": False, "service_tier": self.service_tier,
                "max_output_tokens": MAX_OUTPUT_TOKENS}

    def build_request(self, conv: dict) -> dict:
        items: list[dict] = [{"role": "user", "content": conv["user"]}]
        for h in conv.get("history", []):
            items.extend(h["assistant_native"])
            items.append({"type": "function_call_output", "call_id": h["tool_call"]["id"],
                          "output": h["tool_reply"]})
        body = {
            "model": self.model,
            "instructions": conv["system"],
            "input": items,
            "tools": _tools(),
            "tool_choice": "required" if self.tool_choice == "required" else "auto",
            "parallel_tool_calls": False,
            "reasoning": {"effort": "none"},
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "store": False,
        }
        if self.service_tier:
            body["service_tier"] = self.service_tier
        return body

    def _map_error(self, e: Exception) -> Exception:
        import openai
        msg = str(e)
        code = getattr(e, "code", None) or ""
        if code in ("insufficient_quota", "billing_hard_limit_reached", "billing_not_active"):
            return BillingError(msg)
        # A plain 429 rate limit message also says "add a payment method ... /account/billing",
        # so check for a rate limit before the billing word match (fixed 11/4 after the name check
        # halted OpenAI on a 10 RPM free-tier rate limit).
        if isinstance(e, openai.RateLimitError) and "quota" not in msg.lower() and "hard limit" not in msg.lower():
            m = re.search(r"try again in ([\d.]+)(ms|s)", msg)
            ra = (float(m.group(1)) / (1000 if m.group(2) == "ms" else 1)) + 1 if m else None
            return RateLimitError(msg, ra)
        if looks_like_billing(msg):
            return BillingError(msg)
        if isinstance(e, openai.RateLimitError):
            return RateLimitError(msg)
        if isinstance(e, (openai.APIConnectionError, openai.APITimeoutError, openai.InternalServerError)):
            return TransientError(msg)
        if isinstance(e, openai.APIStatusError):
            if e.status_code == 402:
                return BillingError(msg)
            if e.status_code >= 500:
                return TransientError(msg)
            return PermanentError(msg)
        return TransientError(msg)

    def call(self, payload: dict) -> dict:
        self._pace()
        try:
            r = self.client.responses.create(**payload)
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        return r.model_dump(mode="json")

    # ---- batch ----
    def submit_batch(self, items: list[tuple[str, dict]], label: str) -> str:
        lines = [json.dumps({"custom_id": cid, "method": "POST", "url": "/v1/responses", "body": body})
                 for cid, body in items]
        buf = io.BytesIO(("\n".join(lines) + "\n").encode())
        buf.name = f"{label}.jsonl"
        try:
            f = self.client.files.create(file=buf, purpose="batch")
            b = self.client.batches.create(input_file_id=f.id, endpoint="/v1/responses",
                                           completion_window="24h", metadata={"label": label[:60]})
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        return b.id

    def poll_batch(self, batch_id: str) -> str:
        try:
            b = self.client.batches.retrieve(batch_id)
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        if b.status in ("completed", "expired", "cancelled"):
            return "ended"
        if b.status == "failed":
            errs = getattr(b, "errors", None)
            if errs and looks_like_billing(str(errs)):
                raise BillingError(str(errs))
            return "failed"
        return "running"

    def cancel_batch(self, batch_id: str) -> None:
        try:
            if self.client.batches.retrieve(batch_id).status in ("cancelling", "cancelled", "completed",
                                                                 "expired", "failed"):
                return  # already stopping or stopped
            self.client.batches.cancel(batch_id)
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None

    def fetch_batch(self, batch_id: str, order: list[str] | None = None) -> dict[str, tuple[str, Any]]:
        out: dict[str, tuple[str, Any]] = {}
        try:
            b = self.client.batches.retrieve(batch_id)
            for fid in (b.output_file_id, b.error_file_id):
                if not fid:
                    continue
                text = self.client.files.content(fid).text
                for line in text.splitlines():
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    cid = rec.get("custom_id")
                    resp = rec.get("response") or {}
                    if resp.get("status_code") == 200:
                        out[cid] = ("ok", resp.get("body"))
                    else:
                        err = json.dumps(rec.get("error") or resp.get("body"))
                        if looks_like_billing(err):
                            raise BillingError(err)
                        out[cid] = ("error", err)
        except BillingError:
            raise
        except Exception as e:  # noqa: BLE001
            raise self._map_error(e) from None
        return out

    # ---- response ----
    def normalize(self, raw: dict) -> Normalized:
        calls, texts, native, refusal = [], [], [], False
        for it in raw.get("output") or []:
            t = it.get("type")
            if t == "function_call":
                args = it.get("arguments") or "{}"
                try:
                    pargs = json.loads(args) if isinstance(args, str) else args
                except json.JSONDecodeError:
                    pargs = {"_raw": args}
                calls.append({"id": it.get("call_id"), "name": it.get("name"), "args": pargs})
                native.append({"type": "function_call", "call_id": it.get("call_id"),
                               "name": it.get("name"), "arguments": args if isinstance(args, str) else json.dumps(args)})
            elif t == "message":
                parts = []
                for c in it.get("content") or []:
                    if c.get("type") == "output_text":
                        parts.append(c.get("text") or "")
                    elif c.get("type") == "refusal":
                        refusal = True
                        parts.append(c.get("refusal") or "")
                txt = "".join(parts)
                texts.append(txt)
                if txt.strip() and not refusal:
                    native.append({"role": "assistant", "content": txt})
            elif t == "reasoning" and it.get("encrypted_content"):
                native.append({k: it[k] for k in ("type", "id", "summary", "encrypted_content") if k in it})
        status = "ok"
        if refusal and not calls:
            status = "refusal"
        elif raw.get("status") == "incomplete" and not calls:
            status = "truncated"
        u = raw.get("usage") or {}
        usage = {"input_tokens": u.get("input_tokens", 0) or 0,
                 "output_tokens": u.get("output_tokens", 0) or 0,
                 "thinking_tokens": ((u.get("output_tokens_details") or {}).get("reasoning_tokens") or 0)}
        return Normalized(status=status, tool_calls=calls, text="\n".join(texts).strip(),
                          model_returned=raw.get("model"), stop_reason=raw.get("status"),
                          usage=usage, assistant_native=native)
