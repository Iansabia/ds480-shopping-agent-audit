"""Model name check (design 5.10).

Each API model guesses gender, race, income, education and birth decade for
each name, 5 separate times. The question asks which group a name is "most
common among in US data", to limit refusals (design 5.10).

Keep rule (design 5.10): a name is kept if it is read as intended in at least
14 of 15 guesses across the three API models (9 of 10 if only two models
answer). [Call] "Read as intended" means the race guess AND the gender guess
both match the name's intended cell. Income, education and birth decade are
recorded as descriptives only. A refused or unparseable answer (including a
partial refusal that leaves race or gender blank) is re-asked, up to 3 attempts
per guess. [Call] A guess still refused after 3 attempts is left out of the
denominator (it is not a reading of the name) and the same share is required:
at most 1 miss per 15 guesses (or per 10 with two models). Refusals are counted
and reported per name and per model.

Usage (from the project root):
  .venv/bin/python src/name_check.py run --model haiku [--ids BW01 BW02 ...] [--alternates]
  .venv/bin/python src/name_check.py score
Logs: logs/name_check_<model>.jsonl (one line per guess, resumable).
Keys come from .env and are never printed.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import config  # noqa: E402
from harness.adapters.base import BillingError, looks_like_billing  # noqa: E402
from harness.spend import ProviderHalted, SpendGuard, price_call, worst_case  # noqa: E402

REPS = 5
MAX_OUT = 200
PROMPT_VERSION = "nc3"
# Trial history (logs kept): nc1 asked for a guess about one person; Haiku left
# race blank or refused in 10 of 10 calls (logs/name_check_trial_nc1/). nc2 framed
# it as aggregate population statistics but still asked income and education in
# the same prompt; Haiku refused 8 of 15 guesses after 3 attempts each, citing
# the income and education items (logs/name_check_trial_nc2/). nc3 splits the
# check: one prompt for gender, race and birth decade (the keep rule), and a
# separate prompt for income and education (descriptive only).
SYSTEM = ("You help validate stimuli for a name-based audit study (like Bertrand and Mullainathan 2004 or "
          "Gaddis 2017). Researchers must confirm that each test name signals the demographic group they "
          "intend, using population statistics. You are describing aggregate statistics about names, not "
          "judging any individual person.")
PROMPTS = {
    "rg": """For the name "{name}": in US population records (SSA baby-name data for the first name, Census 2010 surname tables for the last name), answer these aggregate questions.
1. gender: babies given this first name are mostly "woman" or "man"?
2. race: in US data, this name is most common among which group: "Black", "White", "Hispanic" or "Asian"?
3. birth_decade: the decade when this first name was most often given, for example "1980s".
Reply with only a JSON object with keys gender, race, birth_decade.""",
    "ses": """For the name "{name}": in US data on names (for example studies that link first names to mothers' education or household records), answer these aggregate questions.
1. income: the average household income of people with this name relative to the US average: "lower", "middle" or "upper".
2. education: the most common highest education among people with this name: "high school or less", "some college" or "bachelor's or more".
Reply with only a JSON object with keys income and education. Give the most likely answer for each, even if the statistics are uncertain.""",
}
REQUIRED = {"rg": ("race", "gender"), "ses": ("income", "education")}
MAX_ATTEMPTS = 3  # [Call] a refused or unparseable guess is re-asked up to 3 times in all

FIELDS = ["gender", "race", "income", "education", "birth_decade"]  # union over both prompts


def log_path(model_key: str) -> Path:
    return config.LOGS / f"name_check_{model_key}.jsonl"


def load_names(include_alternates: bool) -> list[dict]:
    rows = list(csv.DictReader(open(config.DATA / "names.csv")))
    return [r for r in rows if r["role"] == "main" or (include_alternates and r["role"] == "alternate")]


def parse_guess(text: str) -> dict | None:
    if not text:
        return None
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None
    out = {k: (str(obj.get(k)).strip() if obj.get(k) is not None else None) for k in FIELDS}
    g = (out["gender"] or "").lower()
    out["gender"] = "woman" if g in ("woman", "women", "female", "f") else "man" if g in ("man", "men", "male", "m") else g or None
    r = (out["race"] or "").lower()
    for cand in ("Black", "White", "Hispanic", "Asian"):
        if r.startswith(cand.lower()):
            out["race"] = cand
            break
    return out


# ---------------------------------------------------------------- provider calls
class Caller:
    def __init__(self, model_key: str):
        self.key = model_key
        self.s = config.MODELS[model_key]
        self.provider = self.s["provider"]
        self.model = self.s["model"]
        self._client = None
        self._last = 0.0
        self._lock = threading.Lock()

    def client(self):
        import os
        if self._client is None:
            if self.provider == "anthropic":
                import anthropic
                self._client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], max_retries=2, timeout=60)
            elif self.provider == "openai":
                import openai
                self._client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"], max_retries=1, timeout=120)
            elif self.provider == "google":
                from google import genai
                self._client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
        return self._client

    def settings(self) -> dict:
        if self.provider == "anthropic":
            return {"thinking": "disabled", "effort": "medium", "max_tokens": MAX_OUT}
        if self.provider == "openai":
            return {"reasoning_effort": "none", "max_output_tokens": MAX_OUT, "store": False}
        return {"thinking": "model default", "response_mime_type": "application/json", "max_output_tokens": MAX_OUT}

    def call(self, prompt: str) -> tuple[str, dict, str | None, str]:
        """Return (text, usage, model_returned, status)."""
        c = self.client()
        if self.provider == "anthropic":
            r = c.messages.create(model=self.model, max_tokens=MAX_OUT, thinking={"type": "disabled"},
                                  output_config={"effort": "medium"}, system=SYSTEM,
                                  messages=[{"role": "user", "content": prompt}])
            text = "".join(b.text for b in r.content if b.type == "text")
            st = "refusal" if r.stop_reason == "refusal" else "ok"
            return text, {"input_tokens": r.usage.input_tokens, "output_tokens": r.usage.output_tokens}, r.model, st
        if self.provider == "openai":
            with self._lock:  # free access: 10 requests per minute
                wait = 6.5 - (time.monotonic() - self._last)
                if wait > 0:
                    time.sleep(wait)
                self._last = time.monotonic()
            r = c.responses.create(model=self.model, instructions=SYSTEM, input=prompt, reasoning={"effort": "none"},
                                   max_output_tokens=MAX_OUT, store=False)
            text, st = "", "ok"
            for it in r.output or []:
                if it.type == "message":
                    for p in it.content:
                        if p.type == "output_text":
                            text += p.text
                        elif p.type == "refusal":
                            st = "refusal"
                            text += p.refusal
            u = r.usage
            return text, {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens}, r.model, st
        # google free tier, paced
        with self._lock:
            wait = 4.6 - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
        r = c.models.generate_content(model=self.model, contents=prompt,
                                      config={"system_instruction": SYSTEM, "response_mime_type": "application/json",
                                              "max_output_tokens": MAX_OUT})
        um = r.usage_metadata
        out_tok = (um.candidates_token_count or 0) + (um.thoughts_token_count or 0)
        text = r.text or ""
        st = "ok"
        if not r.candidates:
            st = "refusal"
        return text, {"input_tokens": um.prompt_token_count or 0, "output_tokens": out_tok,
                      "thinking_tokens": um.thoughts_token_count or 0}, r.model_version, st


def classify_error(provider: str, e: Exception) -> str:
    msg = str(e)
    code = getattr(e, "status_code", None) or getattr(e, "code", None)
    if code == 429 and "quota" not in msg.lower() and "hard limit" not in msg.lower():
        return "rate"  # OpenAI's 429 text mentions /account/billing; it is still a rate limit
    if looks_like_billing(msg) and not (provider == "google" and "free" in msg.lower()):
        return "billing"
    if code in (402,):
        return "billing"
    if code == 429 or "rate" in msg.lower() and "limit" in msg.lower():
        return "rate"
    if code and isinstance(code, int) and code >= 500:
        return "transient"
    if "timeout" in msg.lower() or "connection" in msg.lower():
        return "transient"
    return "permanent"


def cmd_run(a):
    config.load_env()
    caller = Caller(a.model)
    guard = SpendGuard()
    lp = log_path(a.model)
    done = set()
    if lp.exists():
        for line in lp.read_text().splitlines():
            rec = json.loads(line)
            if rec.get("status") in ("ok", "refusal"):
                done.add((rec["name_id"], rec["rep"], rec["kind"]))
    names = load_names(a.alternates)
    if a.ids:
        names = [n for n in names if n["name_id"] in set(a.ids)]
    kinds = ["rg"] if a.rg_only else ["rg", "ses"]
    todo = [(n, rep, k) for n in names for rep in range(REPS) for k in kinds if (n["name_id"], rep, k) not in done]
    print(f"{a.model}: {len(todo)} guesses to run ({len(done)} already done)")
    stop = threading.Event()
    wlock = threading.Lock()
    stats = Counter()

    def one(item):
        n, rep, kind = item
        if stop.is_set():
            return
        prompt = PROMPTS[kind].format(name=n["full_name"])
        tries = 0
        attempt_log: list = []
        while not stop.is_set():
            tries += 1
            est_in = int(len(prompt) / 3 * caller.s.get("token_factor", 1.0)) + 20
            try:
                rid = guard.reserve(caller.provider, worst_case(a.model, est_in, MAX_OUT, "std"), f"call:namecheck_{a.model}")
            except ProviderHalted as e:
                stop.set(); stats["halted"] += 1; print("HALTED:", e); return
            t0 = time.time()
            try:
                text, usage, mret, st = caller.call(prompt)
            except Exception as e:  # noqa: BLE001
                guard.release(caller.provider, rid)
                ekind = classify_error(caller.provider, e)  # not `kind`: that is the prompt kind
                if ekind == "billing":
                    guard.halt(caller.provider, f"billing/credit error in name check: {str(e)[:300]}")
                    stop.set(); stats["billing"] += 1
                    print(f"BILLING ERROR on {caller.provider}; provider halted: {str(e)[:200]}")
                    return
                if ekind == "rate":
                    stats["rate_limited"] += 1
                    m = re.search(r"(?:retry(?:Delay| in)['\"]?\s*[:=]?\s*['\"]?|try again in )([\d.]+)s", str(e))
                    time.sleep(min(120, float(m.group(1)) + 1 if m else 20 * tries))
                    if tries < 8:
                        continue
                if ekind == "transient" and tries < 4:
                    time.sleep(5 * tries); continue
                rec = {"name_id": n["name_id"], "rep": rep, "kind": kind, "model_requested": caller.model,
                       "status": "error", "error_kind": ekind,
                       "attempts": attempt_log,
                       "error": str(e)[:500], "t": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
                with wlock, open(lp, "a") as f:
                    f.write(json.dumps(rec) + "\n")
                stats["error"] += 1
                return
            billed, notional = price_call(a.model, usage, "std")
            guard.record(caller.provider, a.model, usage, billed, notional, rid=rid)
            parsed = parse_guess(text) if st == "ok" else None
            if parsed is None and st == "ok" and re.search(r"\b(can't|cannot|won't|will not|not able)\b", text, re.I):
                st = "refusal"  # declined in prose with no JSON
            if parsed is not None and any(not parsed.get(f) or parsed.get(f) == "None" for f in REQUIRED[kind]):
                st = "refusal"  # partial refusal: answered some items but not race or gender
            attempt_log.append({"status": st if parsed is not None or st == "refusal" else "parse_error",
                                "raw": text[:300]})
            if (st == "refusal" or parsed is None) and tries < (MAX_ATTEMPTS if kind == "rg" else 1):
                stats["reask"] += 1
                continue
            rec = {"name_id": n["name_id"], "full_name": n["full_name"], "rep": rep, "kind": kind,
                   "model_requested": caller.model, "model_returned": mret, "status": st if parsed is not None or st == "refusal" else "parse_error",
                   "raw": text[:1000], "parsed": parsed, "attempts": attempt_log, "usage": usage, "cost_usd": billed, "notional_usd": notional,
                   "latency_s": round(time.time() - t0, 2), "settings": caller.settings(), "prompt_version": PROMPT_VERSION,
                   "t": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
            with wlock, open(lp, "a") as f:
                f.write(json.dumps(rec) + "\n")
            stats[rec["status"]] += 1
            return

    workers = 1 if caller.provider in ("google", "openai") else a.workers
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, todo))
    print(json.dumps({"model": a.model, **stats}))
    if stop.is_set():
        sys.exit(2)


# ---------------------------------------------------------------- scoring
def latest_records(model_key: str) -> dict:
    lp = log_path(model_key)
    out = {}
    if not lp.exists():
        return out
    for line in lp.read_text().splitlines():
        rec = json.loads(line)
        if rec.get("prompt_version", PROMPT_VERSION) != PROMPT_VERSION and rec.get("status") != "error":
            continue
        k = (rec["name_id"], rec["rep"], rec.get("kind", "rg"))
        prev = out.get(k)
        if prev is None or prev["status"] in ("error", "parse_error"):
            out[k] = rec
    return out


def cmd_score(a):
    names = {r["name_id"]: r for r in csv.DictReader(open(config.DATA / "names.csv"))}
    models = [m for m in (a.models or ["haiku", "luna", "flashlite"]) if log_path(m).exists()]
    recs = {m: latest_records(m) for m in models}
    rows = []
    for nid, n in names.items():
        per = {}
        total_ok = total_n = 0
        refusals = Counter()
        errors = 0
        race_c, gen_c, inc, edu, dec = Counter(), Counter(), Counter(), Counter(), Counter()
        for m in models:
            got = [recs[m].get((nid, rep, "rg")) for rep in range(REPS)]
            got = [r for r in got if r is not None]
            if not got:
                continue
            ok = valid = 0
            for r in got:
                refusals[m] += sum(1 for x in r.get("attempts", []) if x["status"] == "refusal")
                if r["status"] != "ok":
                    errors += int(r["status"] != "refusal")
                    continue
                p = r["parsed"]
                valid += 1
                ok += int(p.get("race") == n["race"] and p.get("gender") == n["gender"])
                race_c[p.get("race")] += 1
                gen_c[p.get("gender")] += 1
                dec[p.get("birth_decade")] += 1
            for rep in range(REPS):
                r = recs[m].get((nid, rep, "ses"))
                if r and r["status"] == "ok":
                    inc[r["parsed"].get("income")] += 1
                    edu[r["parsed"].get("education")] += 1
            per[m] = f"{ok}/{valid}"
            total_ok += ok
            total_n += valid
        if total_n == 0:
            continue
        # design 5.10: 14 of 15 with three models, 9 of 10 with two. [Call] when some
        # guesses stay refused, the same share is required (at most 1 miss per 15 or per 10).
        n_models = sum(1 for v in per.values() if not v.endswith("/0"))
        share_need = 14 / 15 if n_models >= 3 else 9 / 10
        keep = total_ok >= share_need * total_n - 1e-9
        rows.append({"name_id": nid, "role": n["role"], "tier": n["tier"], "race": n["race"], "gender": n["gender"],
                     "full_name": n["full_name"], **{f"as_intended_{m}": per.get(m, "") for m in models},
                     "as_intended_total": f"{total_ok}/{total_n}", "keep": keep,
                     "race_guesses": dict(race_c), "gender_guesses": dict(gen_c),
                     "decade_mode": dec.most_common(1)[0][0] if dec else "",
                     "income_mode": inc.most_common(1)[0][0] if inc else "",
                     "education_mode": edu.most_common(1)[0][0] if edu else "",
                     "income_guesses": dict(inc), "education_guesses": dict(edu),
                     "refused_attempts_rg": dict(refusals), "errors": errors})
    out = config.DATA / "name_check_results.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (json.dumps(v) if isinstance(v, dict) else v) for k, v in r.items()})
    print(f"{len(rows)} names scored with models {models} -> {out}")
    for r in rows:
        if not r["keep"]:
            print("FAIL", r["name_id"], r["full_name"], r["as_intended_total"], r["race_guesses"], r["gender_guesses"])
    print("kept:", dict(Counter((r["role"], r["keep"]) for r in rows)))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run")
    p.add_argument("--model", choices=["haiku", "luna", "flashlite"], required=True)
    p.add_argument("--ids", nargs="*")
    p.add_argument("--alternates", action="store_true")
    p.add_argument("--rg-only", action="store_true", help="skip the income/education prompt")
    p.add_argument("--workers", type=int, default=4)
    p.set_defaults(func=cmd_run)
    p = sub.add_parser("score")
    p.add_argument("--models", nargs="*", help="models that enter the keep rule (default: all with logs)")
    p.set_defaults(func=cmd_score)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
