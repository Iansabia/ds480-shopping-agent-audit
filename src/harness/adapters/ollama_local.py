"""Ollama adapter for OLMo 3 7B Instruct (olmo-3:7b-instruct), local.

Settings (design 5.5): temperature 0, fixed seed, 16K context, 512 output
tokens. No batch API.

One action per turn (PLAN D4). Ollama has no tool_choice, and in the pilot
(logs/pilot_olmo.*) OLMo never called a tool: all 1,152 episodes ended as
no_tool_call (prose that recommends a product and asks "Would you like me to
proceed?"). So every request also sends `format`, a JSON schema built from
prompts.TOOLS that admits exactly one action object:
  {"name": "buy", "arguments": {"product_id": "<string>"}}
  {"name": "ask_user", "arguments": {"question": "<string>"}}
Ollama constrains decoding to that schema (structured outputs). This is the
local equivalent of tool_choice "required" for the API models. product_id is a
free string, as in the API tool definition, so an id that is not on the page
is still possible and is scored invalid_product.

normalize() turns the JSON content into the same tool call the other adapters
return. Content that does not parse (empty, or cut off at the token limit)
gives no tool call, so parse_action scores it like any other adapter's missing
call (no_tool_call or truncated). The tools are still sent, so OLMo's chat
template lists them. After an ask, OLMo's own JSON reply is replayed as its
turn and the scripted reply comes back as a tool message; the next request is
constrained the same way. No text is added to the prompts: the system and user
messages are exactly the runner's, and the schema is the same for every
episode and name.

Heavy local compute: the runner refuses to use this adapter outside the
allowed window (7 pm to 7 am US Eastern) unless explicitly overridden.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from .. import prompts
from ..config import MAX_OUTPUT_TOKENS, OLLAMA_OPTIONS, OLLAMA_URL
from .base import Adapter, Normalized, PermanentError, TransientError

FORMAT_LABEL = "one_action_json_schema_v1"


def _tools() -> list[dict]:
    return [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                              "parameters": t["parameters"]}} for t in prompts.TOOLS]


def action_schema() -> dict:
    """JSON schema for one action: a call of exactly one tool in prompts.TOOLS,
    with that tool's own parameter schema. product_id stays a free string."""
    return {"anyOf": [{"type": "object",
                       "properties": {"name": {"type": "string", "enum": [t["name"]]},
                                      "arguments": t["parameters"]},
                       "required": ["name", "arguments"],
                       "additionalProperties": False} for t in prompts.TOOLS]}


def format_sha256() -> str:
    return hashlib.sha256(json.dumps(action_schema(), sort_keys=True).encode()).hexdigest()


def call_from_content(content: str | None) -> dict | None:
    """The tool call in a format-constrained reply: the whole content must be
    one JSON object with a string "name" and an object (or no) "arguments".
    Anything else (empty, cut off, not JSON, other shapes) returns None."""
    if not content or not content.strip():
        return None
    try:
        obj = json.loads(content)
    except ValueError:
        return None
    if not isinstance(obj, dict) or not isinstance(obj.get("name"), str):
        return None
    args = obj.get("arguments", {})
    if not isinstance(args, dict):
        return None
    return {"id": "call_0", "name": obj["name"], "args": args}


class OllamaAdapter(Adapter):
    provider = "ollama"
    supports_batch = False

    def request_settings(self) -> dict:
        return {"options": dict(OLLAMA_OPTIONS, num_predict=MAX_OUTPUT_TOKENS),
                "tool_choice": "required, via format (Ollama has no tool_choice)",
                "format": FORMAT_LABEL, "format_sha256": format_sha256()}

    def build_request(self, conv: dict) -> dict:
        msgs: list[dict] = [{"role": "system", "content": conv["system"]},
                            {"role": "user", "content": conv["user"]}]
        for h in conv.get("history", []):
            msgs.append(h["assistant_native"])
            msgs.append({"role": "tool", "content": h["tool_reply"], "tool_name": h["tool_call"]["name"]})
        return {"model": self.model, "messages": msgs, "tools": _tools(), "format": action_schema(),
                "stream": False, "options": dict(OLLAMA_OPTIONS, num_predict=MAX_OUTPUT_TOKENS)}

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
        content = m.get("content") or ""
        text = content.strip()
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
        if not calls:
            # The usual path: the constrained JSON content is the call itself.
            c = call_from_content(content)
            if c is not None:
                calls = [c]
                text = ""
        status = "ok"
        if raw.get("done_reason") == "length" and not calls:
            status = "truncated"
        usage = {"input_tokens": raw.get("prompt_eval_count", 0) or 0,
                 "output_tokens": raw.get("eval_count", 0) or 0}
        # Replayed as is after an ask, so OLMo sees exactly what it wrote.
        native: dict[str, Any] = {"role": "assistant", "content": content}
        if m.get("tool_calls"):
            native["tool_calls"] = m["tool_calls"]
        return Normalized(status=status, tool_calls=calls, text=text,
                          model_returned=raw.get("model"), stop_reason=raw.get("done_reason"),
                          usage=usage, assistant_native=native)
