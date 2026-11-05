"""Episode runner: sync or batch, resumable from the logs.

Files per run (run_name), all under logs/:
  <run>.manifest.json   config, model, settings, git commit, episode count
  <run>.turns.jsonl     one line per model call (turn 0 or the follow-up turn 1)
  <run>.batches.jsonl   batch submissions and collections (batch mode)
  <run>.projection.json spend projection after the first N calls

Episode flow (design 5.4): turn 0 shows the system prompt (account profile)
and the request plus store page. If the agent calls buy, the episode ends. If
it calls ask_user, the scripted reply is returned as the tool result and the
agent gets one more turn (turn 1). In S0, S1 and the arms built on them,
whatever happens on turn 1 ends the episode (a second ask counts as no
purchase). In V and M1V (deviation 11/4, PLAN.md), a second ask on turn 1 gets
one more scripted reply (Catalog.followup_reply, same for every name) and a
final turn 2; an ask on turn 2 counts as no purchase. Refusals, text-only replies,
invalid product ids, truncation and errors are outcomes, never dropped.

Resume: on start the runner reads <run>.turns.jsonl and <run>.batches.jsonl,
collects any open batches, and only sends turns that have no successful record
yet (errors are retried up to max_attempts, then count as an error outcome).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .adapters.base import (Adapter, BillingError, PermanentError, ProviderError, RateLimitError,
                            TransientError, parse_action)
from .catalog import Catalog, Episode
from .config import LOCAL_ALLOWED_END_HOUR, LOCAL_ALLOWED_START_HOUR, LOGS, MAX_OUTPUT_TOKENS
from .spend import ProviderHalted, SpendCapExceeded, SpendGuard, price_call, worst_case


class StopRun(Exception):
    pass


LOCAL_PAUSE_MSG = "Reached 7 am ET; local run paused. Resume tonight."


# Ask protocol version, written to the manifest. Runs logged before 11/4 have no
# such key and keep the old rule (one answered ask in every arm), so resuming or
# rescoring an old pilot never adds turns or changes its outcomes.
ASK_PROTOCOL = "v_followup_1"


def max_answered_asks(base_arm: str, protocol: str | None) -> int:
    if protocol == ASK_PROTOCOL:
        return 2 if base_arm == "V" else 1
    return 1


def manifest_protocol(manifest_path: Path) -> str | None:
    if not manifest_path.exists():
        return ASK_PROTOCOL
    try:
        return json.loads(manifest_path.read_text()).get("ask_protocol")
    except (json.JSONDecodeError, OSError):
        return None


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="milliseconds")


def local_compute_allowed(now: datetime | None = None) -> bool:
    t = (now or datetime.now(ZoneInfo("America/New_York"))).astimezone(ZoneInfo("America/New_York"))
    return t.hour >= LOCAL_ALLOWED_START_HOUR or t.hour < LOCAL_ALLOWED_END_HOUR


def git_commit(root: Path) -> str | None:
    try:
        return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True,
                              text=True, timeout=10).stdout.strip() or None
    except Exception:  # noqa: BLE001
        return None


class Runner:
    def __init__(self, catalog: Catalog, adapter: Adapter, run_name: str, episodes: list[Episode],
                 guard: SpendGuard | None = None, log_dir: Path = LOGS, mode: str = "sync",
                 workers: int = 4, max_attempts: int = 3, projection_after: int = 200,
                 batch_size: int = 5000, poll_s: float = 60.0, allow_daytime_local: bool = False,
                 max_rate_retries: int = 8, sleep=time.sleep, preset: str | None = None,
                 manifest_extra: dict | None = None):
        self.cat = catalog
        self.ad = adapter
        self.run = run_name
        self.episodes = {e.episode_id: e for e in episodes}
        self.order = [e.episode_id for e in episodes]
        self.guard = guard or SpendGuard()
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.mode = mode  # sync | flex | batch
        self.workers = workers
        self.max_attempts = max_attempts
        self.projection_after = projection_after
        self.batch_size = batch_size
        self.poll_s = poll_s
        self.allow_daytime_local = allow_daytime_local
        self.max_rate_retries = max_rate_retries
        self.sleep = sleep
        self.preset = preset
        self.manifest_extra = manifest_extra or {}
        self.turns_path = self.log_dir / f"{run_name}.turns.jsonl"
        self.batches_path = self.log_dir / f"{run_name}.batches.jsonl"
        self.manifest_path = self.log_dir / f"{run_name}.manifest.json"
        self.projection_path = self.log_dir / f"{run_name}.projection.json"
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self.stop_reason: str | None = None
        self._render_cache: dict[str, object] = {}
        self._projection_done = self.projection_path.exists()
        self.ask_protocol = manifest_protocol(self.manifest_path)
        self._repair_tail(self.turns_path)
        self._repair_tail(self.batches_path)

    # ------------------------------------------------------------ logs
    def _append(self, path: Path, rec: dict) -> None:
        line = json.dumps(rec, ensure_ascii=False, default=str)
        with self._lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
                f.flush()

    @staticmethod
    def _repair_tail(path: Path) -> None:
        """If a crash left a partial last line, end it so new records start on a
        fresh line (the partial line is skipped when reading)."""
        if path.exists() and path.stat().st_size > 0:
            with open(path, "rb+") as f:
                f.seek(-1, 2)
                if f.read(1) != b"\n":
                    f.write(b"\n")

    @staticmethod
    def _read_jsonl(path: Path) -> list[dict]:
        if not path.exists():
            return []
        out = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue  # a line cut off by a crash; that turn is simply redone
        return out

    def write_manifest(self) -> None:
        if self.manifest_path.exists():
            m = json.loads(self.manifest_path.read_text())
            t = now_iso()
            m.setdefault("resumed_at", []).append(t)
            # Mode and settings can change on a resume (D11: flex to standard tier);
            # each turn record also carries its own mode and request_settings.
            m.setdefault("resumes", []).append({"at": t, "mode": self.mode,
                                                "settings": self.ad.request_settings()})
        else:
            m = {"run": self.run, "created": now_iso(), "preset": self.preset,
                 "provider": self.ad.provider, "model_key": self.ad.model_key,
                 "model_requested": self.ad.model, "settings": self.ad.request_settings(),
                 "mode": self.mode, "n_episodes": len(self.episodes),
                 "max_output_tokens": MAX_OUTPUT_TOKENS, "git_commit": git_commit(self.cat.data_dir.parent),
                 "episode_ids_sha256": hashlib.sha256("\n".join(sorted(self.episodes)).encode()).hexdigest(),
                 "ask_protocol": self.ask_protocol, **self.manifest_extra}
        self.manifest_path.write_text(json.dumps(m, indent=2))

    # ------------------------------------------------------------ state
    def load_state(self) -> dict[tuple[str, int], dict]:
        """(episode_id, turn) -> {"ok": rec or None, "errors": n}."""
        st: dict[tuple[str, int], dict] = {}
        for r in self._read_jsonl(self.turns_path):
            k = (r["episode_id"], r["turn"])
            s = st.setdefault(k, {"ok": None, "errors": 0})
            if r.get("status") == "ok":
                s["ok"] = r
            else:
                s["errors"] += 1
        return st

    def rendered(self, ep: Episode):
        r = self._render_cache.get(ep.episode_id)
        if r is None:
            r = self.cat.render(ep)
            self._render_cache[ep.episode_id] = r
        return r

    def conversation(self, ep: Episode, turn: int, state: dict) -> dict:
        r = self.rendered(ep)
        conv = {"system": r.system, "user": r.user, "history": []}
        replies = [r.scripted_reply, r.followup_reply]
        for t in range(turn):
            rt = state[(ep.episode_id, t)]["ok"]
            at = rt["action"]
            conv["history"].append({
                "assistant_native": rt["assistant_native"],
                "tool_call": {"id": at.get("call_id"), "name": "ask_user",
                              "args": {"question": at.get("question", "")}},
                "tool_reply": replies[t],
            })
        return conv

    def _next_turn(self, ep: Episode, state: dict) -> tuple[int | None, bool]:
        """(next turn to send or None, episode finished). Walks the turns: an
        ask with a reply left leads to the next turn."""
        max_t = max_answered_asks(ep.base_arm, self.ask_protocol)
        for t in range(max_t + 1):
            s = state.get((ep.episode_id, t), {"ok": None, "errors": 0})
            if s["ok"] is None:
                if s["errors"] >= self.max_attempts:
                    return None, True
                return t, False
            if s["ok"]["action"]["type"] != "ask" or t == max_t:
                return None, True
        return None, True

    def pending(self, state: dict, exclude: set[tuple[str, int]] | None = None) -> list[tuple[Episode, int]]:
        exclude = exclude or set()
        out = []
        for eid in self.order:
            ep = self.episodes[eid]
            t, _ = self._next_turn(ep, state)
            if t is not None and (eid, t) not in exclude:
                out.append((ep, t))
        return out

    def status(self) -> dict:
        st = self.load_state()
        done = errored = asked = 0
        for eid in self.order:
            s0 = st.get((eid, 0))
            if not s0 or s0["ok"] is None:
                if s0 and s0["errors"] >= self.max_attempts:
                    errored += 1
                continue
            if s0["ok"]["action"]["type"] == "ask":
                asked += 1
            if self._next_turn(self.episodes[eid], st)[1]:
                done += 1
        return {"episodes": len(self.order), "done": done, "error_final": errored, "asked": asked,
                "pending_turns": len(self.pending(st))}

    # ------------------------------------------------------------ record helpers
    def _base_record(self, ep: Episode, turn: int, attempt: int) -> dict:
        r = self.rendered(ep)
        return {
            "run": self.run, "episode_id": ep.episode_id, "turn": turn, "attempt": attempt,
            "provider": self.ad.provider, "model_key": self.ad.model_key, "model_requested": self.ad.model,
            "request_settings": self.ad.request_settings(), "mode": self.mode,
            "episode": ep.to_dict(), "order": r.order,
            "positions": {pid: i for i, pid in enumerate(r.order, start=1)},
            "prompt_sha256": hashlib.sha256((r.system + "\x00" + r.user).encode()).hexdigest(),
            "scripted_reply": r.scripted_reply if turn == 1 else (r.followup_reply if turn == 2 else None),
            "birth_year": r.meta["birth_year"],
        }

    def _record_ok(self, ep, turn, attempt, raw, t_req, t_resp, latency, batch_id=None, custom_id=None,
                   rid=None):
        norm = self.ad.normalize(raw)
        action = parse_action(norm, self.rendered(ep).order)
        billed, notional = price_call(self.ad.model_key, norm.usage, self.mode, self.ad.settings)
        rec = self._base_record(ep, turn, attempt)
        rec.update({
            "status": "ok", "t_request": t_req, "t_response": t_resp, "latency_s": latency,
            "batch_id": batch_id, "custom_id": custom_id, "model_returned": norm.model_returned,
            "stop_reason": norm.stop_reason, "response_status": norm.status,
            "usage": norm.usage, "billed_usd_est": billed, "notional_usd_est": notional,
            "text": norm.text, "tool_calls": norm.tool_calls, "action": action,
            "assistant_native": norm.assistant_native, "raw": raw,
        })
        if rid is not None or batch_id is None:
            self.guard.record(self.ad.provider, self.ad.model_key, norm.usage, billed, notional, rid=rid)
        self._append(self.turns_path, rec)
        return rec

    def _record_err(self, ep, turn, attempt, err: str, kind: str, t_req, batch_id=None, custom_id=None):
        rec = self._base_record(ep, turn, attempt)
        rec.update({"status": "error", "error_kind": kind, "error": err[:2000], "t_request": t_req,
                    "t_response": now_iso(), "batch_id": batch_id, "custom_id": custom_id})
        self._append(self.turns_path, rec)

    def _halt(self, reason: str) -> None:
        self.stop_reason = reason
        self._stop.set()

    # ------------------------------------------------------------ guards
    def _local_window_closed(self) -> bool:
        return self.ad.provider == "ollama" and not self.allow_daytime_local and not local_compute_allowed()

    def _preflight(self) -> None:
        self.guard.check(self.ad.provider)
        if self._local_window_closed():
            raise StopRun("Local model runs are allowed only 7 pm to 7 am ET (fan noise rule). "
                          "Pass --allow-daytime-local only if Ian says so.")

    def _maybe_project(self, state: dict) -> None:
        if self._projection_done:
            return
        oks = [s["ok"] for s in state.values() if s["ok"] is not None]
        if len(oks) < self.projection_after:
            return
        mean_billed = sum(r.get("billed_usd_est", 0) for r in oks) / len(oks)
        ask_rate = sum(1 for r in oks if r["turn"] == 0 and r["action"]["type"] == "ask") / max(
            1, sum(1 for r in oks if r["turn"] == 0))
        remaining_t0 = sum(1 for ep, t in self.pending(state) if t == 0)
        remaining_calls = remaining_t0 * (1 + ask_rate) + sum(1 for ep, t in self.pending(state) if t >= 1)
        projected_run = mean_billed * remaining_calls
        snap = self.guard.snapshot()["providers"].get(self.ad.provider, {})
        spent = snap.get("spent_usd", 0.0)
        cap = self.guard.caps.get(self.ad.provider, 0.0)
        proj = {"t": now_iso(), "calls_so_far": len(oks), "mean_billed_per_call": mean_billed,
                "ask_rate_turn0": ask_rate, "remaining_calls_est": remaining_calls,
                "projected_remaining_usd": projected_run, "provider_spent_usd": spent, "cap_usd": cap,
                "ok": spent + projected_run <= cap or projected_run == 0}
        self.projection_path.write_text(json.dumps(proj, indent=2))
        self._projection_done = True
        if not proj["ok"]:
            raise SpendCapExceeded(
                f"Projection after {len(oks)} calls: ${projected_run:.2f} more on top of ${spent:.2f} "
                f"would pass the ${cap:.2f} {self.ad.provider} cap. Stopped; see {self.projection_path.name}.")

    # ------------------------------------------------------------ sync
    def _one_call(self, ep: Episode, turn: int, state: dict, attempt: int):
        if self._stop.is_set():
            return
        if self._local_window_closed():
            # Checked before every local call, so an OLMo run pauses within one
            # call of 7 am ET, not only at the end of a chunk of up to 2,000 turns.
            self._halt(LOCAL_PAUSE_MSG)
            return
        conv = self.conversation(ep, turn, state)
        payload = self.ad.build_request(conv)
        est_in = self.ad.estimate_input_tokens(payload)
        try:
            rid = self.guard.reserve(self.ad.provider,
                                     worst_case(self.ad.model_key, est_in, MAX_OUTPUT_TOKENS, self.mode, self.ad.settings),
                                     label=f"call:{self.run}")
        except (SpendCapExceeded, ProviderHalted) as e:
            self._halt(str(e))
            return
        t_req = now_iso()
        t0 = time.monotonic()
        tries_rate = tries_tr = 0
        while True:
            if self._stop.is_set():
                self.guard.release(self.ad.provider, rid)
                return
            try:
                raw = self.ad.call(payload)
                break
            except BillingError as e:
                self.guard.release(self.ad.provider, rid)
                self.guard.halt(self.ad.provider, f"billing/credit error: {e}")
                self._record_err(ep, turn, attempt, str(e), "billing", t_req)
                self._halt(f"{self.ad.provider} billing/credit error, provider halted: {e}")
                return
            except RateLimitError as e:
                tries_rate += 1
                if tries_rate > self.max_rate_retries:
                    self.guard.release(self.ad.provider, rid)
                    self._record_err(ep, turn, attempt, str(e), "rate_limit", t_req)
                    self._halt(f"{self.ad.provider} still rate limited after {self.max_rate_retries} backoffs "
                               "(free-tier daily quota?). Resume later.")
                    return
                self.sleep(min(300.0, e.retry_after or (5.0 * 2 ** (tries_rate - 1))))
            except TransientError as e:
                tries_tr += 1
                if tries_tr >= 3:
                    self.guard.release(self.ad.provider, rid)
                    self._record_err(ep, turn, attempt, str(e), "transient", t_req)
                    return
                self.sleep(5.0 * tries_tr)
            except ProviderError as e:
                self.guard.release(self.ad.provider, rid)
                self._record_err(ep, turn, attempt, str(e), "permanent", t_req)
                return
            except Exception as e:  # noqa: BLE001
                self.guard.release(self.ad.provider, rid)
                self._record_err(ep, turn, attempt, f"{type(e).__name__}: {e}", "unexpected", t_req)
                return
        latency = round(time.monotonic() - t0, 3)
        try:
            self._record_ok(ep, turn, attempt, raw, t_req, now_iso(), latency, rid=rid)
        except Exception as e:  # noqa: BLE001
            self.guard.release(self.ad.provider, rid)
            self._record_err(ep, turn, attempt, f"normalize failed: {type(e).__name__}: {e}", "parse", t_req)

    def run_sync(self) -> dict:
        self._preflight()
        self.write_manifest()
        self.guard.clear_stale_reservations(self.ad.provider, run=self.run)
        while not self._stop.is_set():
            state = self.load_state()
            try:
                self._maybe_project(state)
            except SpendCapExceeded as e:
                self._halt(str(e))
                break
            todo = self.pending(state)
            if not todo:
                break
            # Run in chunks so the projection check happens early and the
            # local-time guard is re-checked.
            chunk = todo[: self.projection_after] if not self._projection_done else todo[:2000]
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                futs = []
                for ep, turn in chunk:
                    s = state.get((ep.episode_id, turn), {"errors": 0})
                    futs.append(pool.submit(self._one_call, ep, turn, state, s["errors"] + 1))
                for f in as_completed(futs):
                    f.result()
            if self._local_window_closed():
                self._halt(LOCAL_PAUSE_MSG)
        out = self.status()
        out["stop_reason"] = self.stop_reason
        return out

    # ------------------------------------------------------------ batch
    def open_batches(self) -> dict[str, dict]:
        subs, closed = {}, set()
        for r in self._read_jsonl(self.batches_path):
            if r["event"] == "submitted":
                subs[r["batch_id"]] = r
            elif r["event"] in ("collected", "abandoned"):
                closed.add(r["batch_id"])
        return {k: v for k, v in subs.items() if k not in closed}

    def collect(self) -> int:
        """Poll and collect every open batch that has ended. Returns how many are still running."""
        running = 0
        for bid, sub in self.open_batches().items():
            try:
                st = self.ad.poll_batch(bid)
            except BillingError as e:
                self.guard.halt(self.ad.provider, f"billing/credit error: {e}")
                raise StopRun(f"{self.ad.provider} billing error while polling {bid}: {e}") from None
            except ProviderError as e:
                running += 1
                print(f"poll failed for {bid}: {e}")
                continue
            if st == "running":
                running += 1
                continue
            items = sub["items"]  # [custom_id, episode_id, turn, attempt]
            results = {}
            if st == "ended":
                try:
                    results = self.ad.fetch_batch(bid, order=[i[0] for i in items])
                except BillingError as e:
                    self.guard.halt(self.ad.provider, f"billing/credit error: {e}")
                    raise StopRun(f"{self.ad.provider} billing error in batch {bid}: {e}") from None
            t_resp = now_iso()
            tot_usage = {"input_tokens": 0, "output_tokens": 0}
            billed_sum = notional_sum = 0.0
            for cid, eid, turn, attempt in items:
                ep = self.episodes.get(eid)
                if ep is None:
                    continue
                res = results.get(cid)
                if res is None:
                    self._record_err(ep, turn, attempt, f"no result (batch status {st})", "batch_missing",
                                     sub["t_submit"], batch_id=bid, custom_id=cid)
                    continue
                kind, payload = res
                if kind == "ok":
                    try:
                        rec = self._record_ok(ep, turn, attempt, payload, sub["t_submit"], t_resp, None,
                                              batch_id=bid, custom_id=cid)
                        for k in tot_usage:
                            tot_usage[k] += rec["usage"].get(k, 0)
                        billed_sum += rec["billed_usd_est"]
                        notional_sum += rec["notional_usd_est"]
                    except Exception as e:  # noqa: BLE001
                        self._record_err(ep, turn, attempt, f"normalize failed: {e}", "parse",
                                         sub["t_submit"], batch_id=bid, custom_id=cid)
                else:
                    self._record_err(ep, turn, attempt, str(payload), "batch_item_error", sub["t_submit"],
                                     batch_id=bid, custom_id=cid)
            self.guard.record(self.ad.provider, self.ad.model_key, tot_usage, billed_sum, notional_sum,
                              rid=sub.get("reservation"), n_calls=len(results))
            self._append(self.batches_path, {"event": "collected", "batch_id": bid, "status": st,
                                             "t": t_resp, "n_results": len(results),
                                             "billed_usd_est": billed_sum})
        return running

    def cancel_open_batches(self, max_polls: int = 60) -> dict:
        """Cancel every open batch of this run (for example to switch a stuck run to
        sync or flex). Results the provider already finished are collected and kept.
        A batch that ended with no results is logged as 'abandoned' and its spend
        reservation is released, so the pending turns run again on resume."""
        out = {"cancelled": [], "collected": [], "abandoned": [], "still_running": []}
        for bid, sub in self.open_batches().items():
            self.ad.cancel_batch(bid)
            out["cancelled"].append(bid)
            st = "running"
            for i in range(max_polls):
                st = self.ad.poll_batch(bid)
                if st != "running":
                    break
                self.sleep(min(self.poll_s, 10.0))
            if st == "running":
                out["still_running"].append(bid)
                continue
            results = self.ad.fetch_batch(bid) if st == "ended" else {}
            if results:
                out["collected"].append(bid)
                continue  # collect() below records them and frees the reservation
            if sub.get("reservation"):
                self.guard.release(self.ad.provider, sub["reservation"])
            self._append(self.batches_path, {"event": "abandoned", "batch_id": bid, "status": st,
                                             "reason": "cancelled", "t": now_iso(), "n_results": 0})
            out["abandoned"].append(bid)
        if out["collected"]:
            self.collect()
        return out

    def submit(self, limit: int | None = None) -> list[str]:
        state = self.load_state()
        in_flight = set()
        for sub in self.open_batches().values():
            for _cid, eid, turn, _a in sub["items"]:
                in_flight.add((eid, turn))
        todo = self.pending(state, exclude=in_flight)
        if limit is not None:
            todo = todo[:limit]
        ids = []
        for i in range(0, len(todo), self.batch_size):
            chunk = todo[i:i + self.batch_size]
            items, meta, est = [], [], 0.0
            for ep, turn in chunk:
                attempt = state.get((ep.episode_id, turn), {"errors": 0})["errors"] + 1
                payload = self.ad.build_request(self.conversation(ep, turn, state))
                cid = f"{ep.episode_id}__t{turn}a{attempt}"
                items.append((cid, payload))
                meta.append([cid, ep.episode_id, turn, attempt])
                est += worst_case(self.ad.model_key, self.ad.estimate_input_tokens(payload), MAX_OUTPUT_TOKENS,
                                  "batch", self.ad.settings)
            label = f"{self.run}-{len(self.open_batches()) + len(ids) + 1}"
            rid = self.guard.reserve(self.ad.provider, est, label=f"batch:{self.run}:pending")
            try:
                bid = self.ad.submit_batch(items, label)
            except BillingError as e:
                self.guard.release(self.ad.provider, rid)
                self.guard.halt(self.ad.provider, f"billing/credit error: {e}")
                raise StopRun(f"{self.ad.provider} billing error on submit: {e}") from None
            except ProviderError as e:
                self.guard.release(self.ad.provider, rid)
                raise StopRun(f"{self.ad.provider} batch submit failed ({type(e).__name__}): {e}. "
                              "Use --mode sync (or flex for OpenAI) instead.") from None
            except Exception:
                self.guard.release(self.ad.provider, rid)
                raise
            self._append(self.batches_path, {"event": "submitted", "batch_id": bid, "t_submit": now_iso(),
                                             "n": len(items), "reservation": rid, "reserved_usd": est,
                                             "items": meta})
            ids.append(bid)
        return ids

    def run_batch(self, wait: bool = True) -> dict:
        """Collect finished batches, then submit every pending turn. Until the
        spend projection has run, the first submission is capped at
        projection_after turns, so cost is measured before the big grid goes."""
        self._preflight()
        if not self.ad.supports_batch:
            raise StopRun(f"{self.ad.provider} has no batch API; use --mode sync")
        self.write_manifest()
        open_res = {s.get("reservation") for s in self.open_batches().values()}
        self.guard.clear_stale_reservations(self.ad.provider, run=self.run, keep=open_res)
        try:
            while True:
                running = self.collect()
                if not running:
                    state = self.load_state()
                    self._maybe_project(state)
                    if not self._projection_done:
                        # Not enough results yet: send only a projection-sized wave.
                        have = sum(1 for s in state.values() if s["ok"] is not None)
                        new = self.submit(limit=max(0, self.projection_after - have) or None)
                    else:
                        new = self.submit()
                    if new:
                        print(f"submitted {len(new)} batch(es): {', '.join(new)}")
                    else:
                        break
                if not wait:
                    break
                self.sleep(self.poll_s)
        except (SpendCapExceeded, ProviderHalted, StopRun) as e:
            self._halt(str(e))
        out = self.status()
        out["open_batches"] = list(self.open_batches())
        out["stop_reason"] = self.stop_reason
        return out
