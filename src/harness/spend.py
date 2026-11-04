"""Running cost estimate and hard spend caps, kept in logs/spend.json.

- Every call is priced from its logged token usage (config.MODELS prices;
  batch/flex prices when that mode was used). These are estimates; the
  provider consoles are the source of truth.
- Before any call or batch the runner asks for a reservation sized at the
  worst case (estimated input + full max_tokens output). If spent + open
  reservations + the new one would pass the provider cap, it refuses.
- A billing or credit error halts the provider: halted=true is written to
  spend.json and every later call for that provider is refused until a human
  clears it (python src/run_agents.py spend --clear-halt PROVIDER).
- Google is free tier only: billed cost is recorded as $0 and notional cost
  (what it would cost on the paid tier) is tracked separately. The Google cap
  is $0 paid, so a model configured as paid would be refused outright.
The file is updated under an exclusive lock so parallel runs share one ledger.
"""
from __future__ import annotations

import fcntl
import json
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

from .config import CAPS_USD, MODELS, SPEND_FILE


class SpendCapExceeded(Exception):
    pass


class ProviderHalted(Exception):
    pass


def price_call(model_key: str, usage: dict, mode: str, settings: dict | None = None) -> tuple[float, float]:
    """Return (billed_usd, notional_usd) for one call."""
    s = settings or MODELS[model_key]
    pin, pout = s["batch"] if mode in ("batch", "flex") else s["std"]
    notional = (usage.get("input_tokens", 0) * pin + usage.get("output_tokens", 0) * pout) / 1e6
    billed = 0.0 if s.get("free_tier") or s.get("local") else notional
    return billed, notional


def worst_case(model_key: str, est_in: int, max_out: int, mode: str, settings: dict | None = None) -> float:
    s = settings or MODELS[model_key]
    if s.get("free_tier") or s.get("local"):
        return 0.0
    pin, pout = s["batch"] if mode in ("batch", "flex") else s["std"]
    return (est_in * pin + max_out * pout) / 1e6


class SpendGuard:
    def __init__(self, path: Path = SPEND_FILE, caps: dict | None = None):
        self.path = Path(path)
        self.caps = dict(CAPS_USD if caps is None else caps)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lockpath = self.path.with_suffix(".lock")

    @contextmanager
    def _locked(self):
        with open(self._lockpath, "a+") as lf:
            fcntl.flock(lf, fcntl.LOCK_EX)
            try:
                data = json.loads(self.path.read_text()) if self.path.exists() else {}
                data.setdefault("providers", {})
                data["note"] = ("Running ESTIMATE from logged token usage x list prices. "
                                "Provider consoles are the source of truth.")
                yield data
                data["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
                tmp = self.path.with_suffix(".tmp")
                tmp.write_text(json.dumps(data, indent=2, sort_keys=True))
                tmp.replace(self.path)
            finally:
                fcntl.flock(lf, fcntl.LOCK_UN)

    def _prov(self, data: dict, provider: str) -> dict:
        p = data["providers"].setdefault(provider, {
            "cap_usd": self.caps.get(provider, 0.0), "spent_usd": 0.0, "notional_usd": 0.0,
            "calls": 0, "input_tokens": 0, "output_tokens": 0, "reservations": {},
            "halted": False, "halted_reason": None, "by_model": {}})
        p["cap_usd"] = self.caps.get(provider, 0.0)
        return p

    def snapshot(self) -> dict:
        with self._locked() as d:
            return json.loads(json.dumps(d))

    def reserve(self, provider: str, usd: float, label: str = "") -> str:
        with self._locked() as d:
            p = self._prov(d, provider)
            if p["halted"]:
                raise ProviderHalted(f"{provider} is halted: {p['halted_reason']}")
            open_res = sum(r["usd"] for r in p["reservations"].values())
            if p["spent_usd"] + open_res + usd > p["cap_usd"] + 1e-12 and usd > 0:
                raise SpendCapExceeded(
                    f"{provider}: spent ${p['spent_usd']:.4f} + reserved ${open_res:.4f} + new ${usd:.4f} "
                    f"would pass the ${p['cap_usd']:.2f} cap")
            rid = uuid.uuid4().hex[:12]
            p["reservations"][rid] = {"usd": usd, "label": label, "t": time.time()}
            return rid

    def release(self, provider: str, rid: str) -> None:
        with self._locked() as d:
            self._prov(d, provider)["reservations"].pop(rid, None)

    def record(self, provider: str, model_key: str, usage: dict, billed: float, notional: float,
               rid: str | None = None, n_calls: int = 1) -> None:
        with self._locked() as d:
            p = self._prov(d, provider)
            if rid:
                p["reservations"].pop(rid, None)
            p["spent_usd"] = round(p["spent_usd"] + billed, 8)
            p["notional_usd"] = round(p["notional_usd"] + notional, 8)
            p["calls"] += n_calls
            p["input_tokens"] += int(usage.get("input_tokens", 0))
            p["output_tokens"] += int(usage.get("output_tokens", 0))
            m = p["by_model"].setdefault(model_key, {"spent_usd": 0.0, "calls": 0})
            m["spent_usd"] = round(m["spent_usd"] + billed, 8)
            m["calls"] += n_calls

    def halt(self, provider: str, reason: str) -> None:
        with self._locked() as d:
            p = self._prov(d, provider)
            p["halted"] = True
            p["halted_reason"] = reason[:500]
            p["halted_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")

    def clear_halt(self, provider: str) -> None:
        with self._locked() as d:
            p = self._prov(d, provider)
            p["halted"] = False
            p["halted_reason"] = None

    def clear_stale_reservations(self, provider: str, run: str, keep: set | None = None,
                                 max_age_s: float = 900.0) -> None:
        """Drop reservations a crashed process of this run left behind: sync-call
        reservations older than max_age_s, and batch reservations whose batch is
        no longer open. Other runs' reservations are untouched."""
        keep = keep or set()
        now = time.time()
        with self._locked() as d:
            p = self._prov(d, provider)
            new = {}
            for k, v in p["reservations"].items():
                lab = v.get("label", "")
                if lab == f"call:{run}" and now - v.get("t", now) > max_age_s:
                    continue
                if lab.startswith(f"batch:{run}:") and k not in keep:
                    continue
                new[k] = v
            p["reservations"] = new

    def check(self, provider: str) -> None:
        with self._locked() as d:
            p = self._prov(d, provider)
            if p["halted"]:
                raise ProviderHalted(f"{provider} is halted: {p['halted_reason']}")
