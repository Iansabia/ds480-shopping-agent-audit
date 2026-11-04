"""Ollama adapter for OLMo 3 7B Instruct (olmo-3:7b-instruct), local.

Settings (design 5.5): temperature 0, fixed seed, 16K context. Ollama cannot
force a tool call, so tool_choice is effectively "auto"; a call written as JSON
text is recovered by parse_action and flagged. No batch API.

Heavy local compute: the runner refuses to use this adapter outside the
allowed window (7 pm to 7 am US Eastern) unless explicitly overridden.
"""
from __future__ import annotations

import json
from typing import Any

from .. import prompts
from ..config import MAX_OUTPUT_TOKENS, OLLAMA_OPTIONS, OLLAMA_URL
from .base import Adapter, Normalized, PermanentError, TransientError


def _tools() -> list[dict]:
    return [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                              "parameters": t["parameters"]}} for t in prompts.TOOLS]


class OllamaAdapter(Adapter):
    provider = "ollama"
    supports_batch = False

    def request_settings(self) -> dict:
        return {"options": dict(OLLAMA_OPTIONS, num_predict=MAX_OUTPUT_TOKENS),
                "tool_choice": "auto (Ollama cannot force tools)"}

    def build_request(self, conv: dict) -> dict:
        msgs: list[dict] = [{"role": "system", "content": conv["system"]},
                            {"role": "user", "content": conv["user"]}]
        for h in conv.get("history", []):
            msgs.append(h["assistant_native"])
            msgs.append({"role": "tool", "content": h["tool_reply"], "tool_name": h["tool_call"]["name"]})
        return {"model": self.model, "messages": msgs, "tools": _tools(), "stream": False,
                "options": dict(OLLAMA_OPTIONS, num_predict=MAX_OUTPUT_TOKENS)}

    def call(self, payload: dict) -> dict:
        import requests
        try:
            r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=600)
        except requests.RequestException as e:
            raise TransientError(str(e)) from None
        if r.status_code >= 500:
            raise TransientError(r.text[:500])
        if r.status_code != 200:
            raise PermanentError(r.text[:500])
        return r.json()

    def normalize(self, raw: dict) -> Normalized:
        m = raw.get("message") or {}
        calls = []
        for i, tc in enumerate(m.get("tool_calls") or []):
            fn = tc.get("function") or {}
            args = fn.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {"_raw": args}
            calls.append({"id": tc.get("id") or f"call_{i}", "name": fn.get("name"), "args": args})
        status = "ok"
        if raw.get("done_reason") == "length" and not calls:
            status = "truncated"
        usage = {"input_tokens": raw.get("prompt_eval_count", 0) or 0,
                 "output_tokens": raw.get("eval_count", 0) or 0}
        native: dict[str, Any] = {"role": "assistant", "content": m.get("content") or ""}
        if m.get("tool_calls"):
            native["tool_calls"] = m["tool_calls"]
        return Normalized(status=status, tool_calls=calls, text=(m.get("content") or "").strip(),
                          model_returned=raw.get("model"), stop_reason=raw.get("done_reason"),
                          usage=usage, assistant_native=native)
