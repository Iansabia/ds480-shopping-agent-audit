"""Fake model for unit tests and dry runs. No network, no cost.

A policy is a function (conv: dict) -> dict, returning one of
  {"buy": "<product_id>"} | {"ask": "<question>"} | {"text": "..."} | {"refuse": True}
The raw "response" is a small dict that normalize() understands. The fake can
also raise a chosen error after N calls, to test resume and the spend guard.
"""
from __future__ import annotations

import itertools
import re
from typing import Any, Callable

from .base import Adapter, Normalized

_ID = re.compile(r"Product ID: (\S+)")


def first_product_policy(conv: dict) -> dict:
    ids = _ID.findall(conv["user"])
    return {"buy": ids[0]}


def ask_then_cheapest_policy(conv: dict) -> dict:
    if not conv.get("history"):
        return {"ask": "Which kind do you need?"}
    prices = re.findall(r"Product ID: (\S+)\n.*?\n.*?\n   Price: \$([\d,.]+)", conv["user"])
    best = min(prices, key=lambda x: float(x[1].replace(",", "")))
    return {"buy": best[0]}


class FakeAdapter(Adapter):
    provider = "fake"
    supports_batch = True

    def __init__(self, model_key="fake", settings=None, policy: Callable[[dict], dict] = first_product_policy,
                 fail_after: int | None = None, fail_with: Exception | None = None, **kw):
        settings = settings or {"model": "fake-model-1", "std": (1.0, 2.0), "batch": (0.5, 1.0), "token_factor": 1.0}
        super().__init__(model_key, settings, **kw)
        self.policy = policy
        self.calls = 0
        self.fail_after = fail_after
        self.fail_with = fail_with
        self._batches: dict[str, dict] = {}
        self._ids = itertools.count(1)
        self.seen_payloads: list[dict] = []

    def request_settings(self) -> dict:
        return {"fake": True, "tool_choice": self.tool_choice}

    def build_request(self, conv: dict) -> dict:
        return {"model": self.model, "conv": conv}

    def _maybe_fail(self):
        if self.fail_after is not None and self.calls >= self.fail_after:
            raise self.fail_with or RuntimeError("fake failure")

    def _respond(self, payload: dict) -> dict:
        self.seen_payloads.append(payload)
        act = self.policy(payload["conv"])
        n = next(self._ids)
        return {"model": self.model + "-served", "action": act, "call_id": f"fc_{n}",
                "usage": {"input_tokens": 1000, "output_tokens": 50}}

    def call(self, payload: dict) -> dict:
        self._maybe_fail()
        self.calls += 1
        return self._respond(payload)

    def submit_batch(self, items: list[tuple[str, dict]], label: str) -> str:
        self._maybe_fail()
        bid = f"fakebatch_{len(self._batches) + 1}"
        self._batches[bid] = {"items": items, "polls": 0}
        return bid

    def poll_batch(self, batch_id: str) -> str:
        b = self._batches[batch_id]
        b["polls"] += 1
        return "ended" if b["polls"] >= 2 else "running"

    def fetch_batch(self, batch_id: str, order: list[str] | None = None) -> dict[str, tuple[str, Any]]:
        out = {}
        for cid, p in self._batches[batch_id]["items"]:
            self.calls += 1
            out[cid] = ("ok", self._respond(p))
        return out

    def normalize(self, raw: dict) -> Normalized:
        a = raw["action"]
        usage = raw.get("usage", {})
        if a.get("refuse"):
            return Normalized(status="refusal", text="I can't help with that.", model_returned=raw["model"], usage=usage)
        if "buy" in a:
            calls = [{"id": raw["call_id"], "name": "buy", "args": {"product_id": a["buy"]}}]
        elif "ask" in a:
            calls = [{"id": raw["call_id"], "name": "ask_user", "args": {"question": a["ask"]}}]
        else:
            calls = []
        native = {"role": "assistant", "calls": calls, "text": a.get("text", "")}
        return Normalized(status="ok", tool_calls=calls, text=a.get("text", ""), model_returned=raw["model"],
                          stop_reason="tool_use" if calls else "end_turn", usage=usage, assistant_native=native)
