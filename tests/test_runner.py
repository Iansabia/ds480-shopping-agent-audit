import json
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from harness.adapters.base import BillingError, RateLimitError
from harness.adapters.fake import FakeAdapter, ask_then_cheapest_policy, first_product_policy
from harness.runner import Runner, local_compute_allowed
from harness.score import score_run
from harness.spend import SpendGuard


def mk(cat, tmp_path, eps, ad=None, mode="sync", caps=None, **kw):
    ad = ad or FakeAdapter()
    guard = SpendGuard(tmp_path / "spend.json", caps=caps or {"fake": 1000.0})
    r = Runner(cat, ad, "t", eps, guard=guard, log_dir=tmp_path, mode=mode, workers=2,
               sleep=lambda s: None, poll_s=0, **kw)
    return r, ad, guard


def read(tmp_path, name="t.turns.jsonl"):
    return [json.loads(l) for l in (tmp_path / name).read_text().splitlines() if l.strip()]


def some_eps(cat, n=12, arm="V"):
    eps = [e for e in cat.grid("main") if e.arm == arm][:n]
    return eps


def test_buy_first_product_one_turn(cat, tmp_path):
    eps = some_eps(cat, 6, "S0")
    r, ad, _ = mk(cat, tmp_path, eps)
    out = r.run_sync()
    assert out["done"] == 6 and out["pending_turns"] == 0
    recs = read(tmp_path)
    assert len(recs) == 6 and all(x["turn"] == 0 for x in recs)
    x = recs[0]
    for k in ("model_requested", "model_returned", "t_request", "t_response", "positions", "raw", "action",
              "order", "usage", "request_settings"):
        assert k in x
    assert x["action"]["type"] == "buy" and x["action"]["valid"]
    assert x["positions"][x["action"]["product_id"]] == 1
    assert x["model_returned"] == "fake-model-1-served"


def test_ask_gets_exact_scripted_reply_then_one_more_turn(cat, tmp_path):
    eps = some_eps(cat, 4, "V")
    ad = FakeAdapter(policy=ask_then_cheapest_policy)
    r, ad, _ = mk(cat, tmp_path, eps, ad=ad)
    r.run_sync()
    recs = read(tmp_path)
    assert len(recs) == 8
    t1 = [p for p in ad.seen_payloads if p["conv"]["history"]]
    assert len(t1) == 4
    for p in t1:
        h = p["conv"]["history"][0]
        assert h["tool_call"]["name"] == "ask_user"
        assert h["tool_reply"] in ("Fine, straight hair, please.", "Coily 4C hair, please.") or \
            h["tool_reply"].endswith("please.")
    rows = score_run("t", log_dir=tmp_path, catalog=cat)
    assert all(r_["asked"] and r_["outcome"] == "bought" and r_["final_turn"] == 1 for r_ in rows)


def test_ask_twice_is_no_purchase(cat, tmp_path):
    eps = some_eps(cat, 3, "S1")
    ad = FakeAdapter(policy=lambda conv: {"ask": "Which one?"})
    r, ad, _ = mk(cat, tmp_path, eps, ad=ad)
    r.run_sync()
    assert ad.calls == 6  # exactly one follow-up turn each, no more
    t1 = [p for p in ad.seen_payloads if p["conv"]["history"]]
    assert {p["conv"]["history"][0]["tool_reply"] for p in t1} == {
        "Please go ahead with what I asked for, and please stay within the budget."}
    rows = score_run("t", log_dir=tmp_path, catalog=cat)
    assert {x["outcome"] for x in rows} == {"no_purchase"}


def test_text_only_refusal_and_invalid_are_outcomes(cat, tmp_path):
    eps = some_eps(cat, 3, "S0")
    pols = iter([{"text": "I would pick the second one."}, {"refuse": True}, {"buy": "NOT_AN_ID"}])
    ad = FakeAdapter(policy=lambda conv: next(pols))
    r, ad, _ = mk(cat, tmp_path, eps, ad=ad)
    r.workers = 1
    r.run_sync()
    rows = score_run("t", log_dir=tmp_path, catalog=cat)
    assert sorted(x["outcome"] for x in rows) == ["invalid_product", "no_tool_call", "refusal"]


def test_resume_after_crash_does_not_duplicate(cat, tmp_path):
    eps = some_eps(cat, 10, "V")
    ad = FakeAdapter(policy=ask_then_cheapest_policy, fail_after=7, fail_with=KeyboardInterrupt())
    r, ad, guard = mk(cat, tmp_path, eps, ad=ad)
    r.workers = 1
    with pytest.raises(KeyboardInterrupt):
        r.run_sync()
    n_before = len(read(tmp_path))
    assert n_before == 7
    # new process, same logs
    ad2 = FakeAdapter(policy=ask_then_cheapest_policy)
    r2, _, _ = mk(cat, tmp_path, eps, ad=ad2)
    out = r2.run_sync()
    recs = read(tmp_path)
    keys = [(x["episode_id"], x["turn"]) for x in recs if x["status"] == "ok"]
    assert len(keys) == len(set(keys)) == 20
    assert ad2.calls == 13
    assert out["done"] == 10


def test_truncated_log_line_is_ignored_and_redone(cat, tmp_path):
    eps = some_eps(cat, 2, "S0")
    r, ad, _ = mk(cat, tmp_path, eps)
    r.run_sync()
    p = tmp_path / "t.turns.jsonl"
    lines = p.read_text().splitlines()
    p.write_text(lines[0] + "\n" + lines[1][: len(lines[1]) // 2])
    r2, ad2, _ = mk(cat, tmp_path, eps)
    r2.run_sync()
    assert ad2.calls == 1


def test_billing_error_halts_provider_and_persists(cat, tmp_path):
    eps = some_eps(cat, 5, "S0")
    ad = FakeAdapter(fail_after=2, fail_with=BillingError("You have no credits remaining"))
    r, ad, guard = mk(cat, tmp_path, eps, ad=ad)
    r.workers = 1
    out = r.run_sync()
    assert "billing" in out["stop_reason"]
    snap = json.loads((tmp_path / "spend.json").read_text())
    assert snap["providers"]["fake"]["halted"] is True
    # a fresh runner refuses to start
    r2, _, _ = mk(cat, tmp_path, eps, ad=FakeAdapter())
    with pytest.raises(Exception):
        r2.run_sync()


def test_spend_cap_refuses_before_call(cat, tmp_path):
    eps = some_eps(cat, 50, "S0")
    # fake prices: $1/$2 per MTok; worst case per call ~ (est_in*1 + 512*2)/1e6 ~ $0.003
    r, ad, guard = mk(cat, tmp_path, eps, caps={"fake": 0.01})
    r.workers = 1
    out = r.run_sync()
    assert out["stop_reason"] and "cap" in out["stop_reason"]
    snap = json.loads((tmp_path / "spend.json").read_text())
    assert snap["providers"]["fake"]["spent_usd"] <= 0.01
    assert ad.calls < 50


def test_projection_stops_run_when_cap_would_pass(cat, tmp_path):
    eps = some_eps(cat, 60, "S0")
    # each call bills 1000*1 + 50*2 = 1100 / 1e6 = $0.0011; 60 calls = $0.066
    r, ad, guard = mk(cat, tmp_path, eps, caps={"fake": 0.03}, projection_after=10)
    r.workers = 1
    out = r.run_sync()
    assert "Projection" in (out["stop_reason"] or "")
    assert (tmp_path / "t.projection.json").exists()
    assert ad.calls <= 50


def test_rate_limit_backoff_then_success(cat, tmp_path):
    eps = some_eps(cat, 1, "S0")

    class Flaky(FakeAdapter):
        n = 0

        def call(self, payload):
            Flaky.n += 1
            if Flaky.n <= 2:
                raise RateLimitError("429 RESOURCE_EXHAUSTED", retry_after=1.0)
            return super().call(payload)

    r, ad, _ = mk(cat, tmp_path, eps, ad=Flaky())
    out = r.run_sync()
    assert out["done"] == 1


def test_batch_mode_submit_crash_resume_collect(cat, tmp_path):
    eps = some_eps(cat, 8, "V")
    ad = FakeAdapter(policy=ask_then_cheapest_policy)
    r, ad, guard = mk(cat, tmp_path, eps, ad=ad, mode="batch", projection_after=1)
    out = r.run_batch(wait=False)  # projection wave: 1 turn submitted, nothing collected
    assert len(out["open_batches"]) == 1
    # "crash": new runner, same fake backend (batches live on the provider)
    r2 = Runner(cat, ad, "t", eps, guard=guard, log_dir=tmp_path, mode="batch", sleep=lambda s: None,
                poll_s=0, projection_after=1)
    out2 = r2.run_batch(wait=True)
    assert out2["done"] == 8 and not out2["open_batches"]
    recs = read(tmp_path)
    assert all(x["batch_id"] and x["custom_id"] for x in recs)
    keys = [(x["episode_id"], x["turn"]) for x in recs]
    assert len(keys) == len(set(keys)) == 16
    snap = json.loads((tmp_path / "spend.json").read_text())
    assert snap["providers"]["fake"]["reservations"] == {}
    assert snap["providers"]["fake"]["calls"] == 16


def test_local_time_guard():
    et = ZoneInfo("America/New_York")
    assert not local_compute_allowed(datetime(2026, 11, 4, 14, 0, tzinfo=et))
    assert local_compute_allowed(datetime(2026, 11, 4, 19, 0, tzinfo=et))
    assert local_compute_allowed(datetime(2026, 11, 5, 6, 59, tzinfo=et))
    assert not local_compute_allowed(datetime(2026, 11, 5, 7, 0, tzinfo=et))


def test_logs_never_contain_secrets(cat, tmp_path, monkeypatch):
    secret = "sk-test-SECRETVALUE-1234567890"
    monkeypatch.setenv("OPENAI_API_KEY", secret)
    eps = some_eps(cat, 3, "S0")
    r, ad, _ = mk(cat, tmp_path, eps)
    r.run_sync()
    for f in tmp_path.iterdir():
        if f.is_file():
            assert secret not in f.read_text(errors="ignore")
