"""V follow-up reply (deviation 11/4, PLAN.md): a second ask in V and M1V gets
one more scripted reply that depends only on task and hidden need; a third ask
is no purchase; other arms keep one answered ask; old runs keep the old rule."""
import inspect
import json

from harness.adapters.fake import FakeAdapter, ask_then_cheapest_policy
from harness.catalog import Catalog
from harness.runner import ASK_PROTOCOL, Runner
from harness.score import score_run
from harness.spend import SpendGuard


def mk(cat, tmp_path, eps, policy):
    ad = FakeAdapter(policy=policy)
    guard = SpendGuard(tmp_path / "spend.json", caps={"fake": 1000.0})
    r = Runner(cat, ad, "t", eps, guard=guard, log_dir=tmp_path, mode="sync", workers=1,
               sleep=lambda s: None, poll_s=0)
    return r, ad


def ask_twice_then_cheapest(conv):
    if len(conv["history"]) < 2:
        return {"ask": "Which one would you like?"}
    return ask_then_cheapest_policy(conv)


def v_eps(cat, n, arm="V"):
    return [e for e in cat.grid("main" if arm == "V" else "m1") if e.arm == arm][:n]


def test_followup_reply_takes_no_identity_argument(cat):
    params = list(inspect.signature(Catalog.followup_reply).parameters)
    assert params == ["self", "task", "hidden_need"]


def test_followup_reply_identical_for_every_name(cat):
    names = [p["name"] for p in cat.profiles_all if p.get("name")]
    tokens = {w.lower() for n in names for w in n.split()}
    by_cell: dict[tuple, set] = {}
    for preset, arms in (("main", ("V",)), ("m1", ("M1V",))):
        for ep in cat.grid(preset):
            if ep.arm not in arms:
                continue
            r = cat.render(ep)
            assert r.followup_reply
            by_cell.setdefault((ep.task_id, ep.hidden_need), set()).add(r.followup_reply)
    # every task x hidden need cell, across all 68 main profiles (names and baseline)
    assert len(by_cell) == 2 * len(cat.tasks)
    for (task_id, need), replies in by_cell.items():
        assert len(replies) == 1, (task_id, need, replies)
        reply = next(iter(replies))
        assert reply == cat.followup_reply(cat.task_by_id[task_id], need)
        assert cat.task_by_id[task_id]["hidden_needs"][need] in reply
        words = {w.strip(".,:;!?'\"").lower() for w in reply.split()}
        assert not (words & tokens), (reply, words & tokens)


def test_followup_reply_none_outside_v(cat):
    for ep in cat.grid("pilot"):
        if ep.base_arm != "V":
            assert cat.render(ep).followup_reply is None


def test_v_second_ask_gets_followup_then_buys(cat, tmp_path):
    eps = v_eps(cat, 4)
    r, ad = mk(cat, tmp_path, eps, ask_twice_then_cheapest)
    out = r.run_sync()
    assert out["done"] == 4 and out["pending_turns"] == 0
    assert ad.calls == 12
    t2 = [p for p in ad.seen_payloads if len(p["conv"]["history"]) == 2]
    assert len(t2) == 4
    for p in t2:
        h0, h1 = p["conv"]["history"]
        assert h1["tool_call"]["name"] == "ask_user"
        assert h1["tool_reply"].startswith(h0["tool_reply"])
        assert h1["tool_reply"].endswith("Please choose one yourself and buy it.")
    rows = score_run("t", log_dir=tmp_path, catalog=cat)
    for x in rows:
        assert x["outcome"] == "bought" and x["final_turn"] == 2
        assert x["asked"] and x["asked_again"] and x["n_asks"] == 2
        assert x["ask_question_2"] == "Which one would you like?"
    assert json.loads((tmp_path / "t.manifest.json").read_text())["ask_protocol"] == ASK_PROTOCOL


def test_v_three_asks_is_no_purchase(cat, tmp_path):
    eps = v_eps(cat, 3, "M1V")
    r, ad = mk(cat, tmp_path, eps, lambda conv: {"ask": "Which?"})
    r.run_sync()
    assert ad.calls == 9  # capped: two answered asks, then the episode ends
    rows = score_run("t", log_dir=tmp_path, catalog=cat)
    assert {x["outcome"] for x in rows} == {"no_purchase"}
    assert {x["n_asks"] for x in rows} == {3}


def test_s_arms_keep_one_answered_ask(cat, tmp_path):
    eps = [e for e in cat.grid("main") if e.arm == "S0"][:3]
    r, ad = mk(cat, tmp_path, eps, lambda conv: {"ask": "Which?"})
    r.run_sync()
    assert ad.calls == 6
    rows = score_run("t", log_dir=tmp_path, catalog=cat)
    assert {x["outcome"] for x in rows} == {"no_purchase"}
    assert {x["n_asks"] for x in rows} == {2}


def test_old_run_without_protocol_keeps_old_rule(cat, tmp_path):
    eps = v_eps(cat, 2)
    (tmp_path / "t.manifest.json").write_text(json.dumps({"run": "t"}))
    r, ad = mk(cat, tmp_path, eps, lambda conv: {"ask": "Which?"})
    r.run_sync()
    assert ad.calls == 4
    rows = score_run("t", log_dir=tmp_path, catalog=cat)
    assert {x["outcome"] for x in rows} == {"no_purchase"}
