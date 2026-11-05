"""OLMo one-action format (PLAN D4): the Ollama request is constrained to one
JSON action object, the same for every name, and the JSON reply is parsed and
scored like the other adapters' tool calls. No network calls are made."""
import copy
import json
import re

from harness.adapters import make_adapter
from harness.adapters.base import parse_action
from harness.adapters.ollama_local import OllamaAdapter, action_schema
from harness.config import MODELS
from harness.runner import LOCAL_PAUSE_MSG, Runner
from harness.score import score_run
from harness.spend import SpendGuard

CELL = ("S0", "hair_shampoo_fine_straight", "w1_fwd")


def pretty(name, **args):
    """A reply the way OLMo writes it under the format (indented JSON)."""
    return json.dumps({"name": name, "arguments": args}, indent=2)


def raw(content, done="stop", tool_calls=None):
    m = {"role": "assistant", "content": content}
    if tool_calls:
        m["tool_calls"] = tool_calls
    return {"model": "olmo-3:7b-instruct", "done_reason": done, "prompt_eval_count": 1400, "eval_count": 25,
            "message": m}


# ---------------- (a) identical for every name ----------------
def test_format_and_added_text_identical_across_profiles(cat):
    ad = make_adapter("olmo")
    arm, task, slot = CELL
    profiles = [p["profile_id"] for p in cat.main_profiles + cat.addon_profiles]
    assert len(profiles) > 50 and "BASE1" in profiles  # named and no-name profiles
    asked = pretty("ask_user", question="Which one do you want?")
    rests, users = set(), set()
    for pid in profiles:
        r = cat.render(cat.make_episode(arm, pid, task, slot))
        conv0 = {"system": r.system, "user": r.user, "history": []}
        conv1 = {"system": r.system, "user": r.user, "history": [{
            "assistant_native": {"role": "assistant", "content": asked},
            "tool_call": {"id": "call_0", "name": "ask_user", "args": {"question": "Which one do you want?"}},
            "tool_reply": r.scripted_reply}]}
        for conv in (conv0, conv1):
            p = ad.build_request(conv)
            assert p["format"] == action_schema()
            # Nothing is added to what OLMo reads: the runner's exact texts.
            assert p["messages"][0] == {"role": "system", "content": r.system}
            assert p["messages"][1] == {"role": "user", "content": r.user}
            users.add(r.user)
            # Everything else in the request (format, tools, options, the replay
            # and the scripted reply) must be byte-identical across names.
            rest = copy.deepcopy(p)
            rest["messages"][0]["content"] = "<runner system text>"
            rests.add(json.dumps(rest, sort_keys=True))
    assert len(users) == 1
    assert len(rests) == 2  # one per turn, the same for every profile
    names = {w.lower() for p in cat.main_profiles + cat.addon_profiles
             for w in re.findall(r"[A-Za-z]+", p.get("name") or "")}
    settings = {k: v for k, v in ad.request_settings().items() if k != "format_sha256"}
    added = json.dumps(action_schema()) + json.dumps(settings)
    assert not names & {w.lower() for w in re.findall(r"[A-Za-z]+", added)}


def test_schema_is_one_call_of_one_tool_with_free_product_id():
    s = action_schema()
    assert len(s["anyOf"]) == 2
    by_name = {alt["properties"]["name"]["enum"][0]: alt for alt in s["anyOf"]}
    assert set(by_name) == {"buy", "ask_user"}
    for alt in s["anyOf"]:
        assert alt["required"] == ["name", "arguments"] and alt["additionalProperties"] is False
    pid = by_name["buy"]["properties"]["arguments"]["properties"]["product_id"]
    assert pid["type"] == "string" and "enum" not in pid  # free string, ids not enumerated
    settings = make_adapter("olmo").request_settings()
    assert settings["options"] == {"temperature": 0, "seed": 480, "num_ctx": 16384, "num_predict": 512}
    assert settings["format"] == "one_action_json_schema_v1"


# ---------------- (b) parsing ----------------
def test_json_content_becomes_the_right_action(cat):
    ad = make_adapter("olmo")
    r = cat.render(cat.make_episode(*CELL[:1], "BW01", *CELL[1:]))
    buy = pretty("buy", product_id=r.order[2])
    n = ad.normalize(raw(buy))
    assert n.status == "ok" and n.text == ""
    assert n.assistant_native == {"role": "assistant", "content": buy}  # replayed exactly
    assert parse_action(n, r.order) == {"type": "buy", "product_id": r.order[2], "valid": True,
                                        "call_id": "call_0", "call_name": "buy"}
    a = parse_action(ad.normalize(raw(pretty("buy", product_id="B000NOTONPAGE"))), r.order)
    assert a["type"] == "buy" and a["valid"] is False  # scored invalid_product
    a = parse_action(ad.normalize(raw(pretty("ask_user", question="Which hair type?"))), r.order)
    assert a == {"type": "ask", "question": "Which hair type?", "call_id": "call_0", "call_name": "ask_user"}
    a = parse_action(ad.normalize(raw('{"name": "checkout", "arguments": {}}')), r.order)
    assert a["type"] == "unknown_tool"
    # A native tool call (if Ollama ever parses one) still wins.
    a = parse_action(ad.normalize(raw("", tool_calls=[{"function": {"name": "buy", "arguments": {
        "product_id": r.order[0]}}}])), r.order)
    assert a["type"] == "buy" and a["valid"]


def test_malformed_or_empty_content_is_a_missing_action(cat):
    ad = make_adapter("olmo")
    order = cat.render(cat.make_episode(*CELL[:1], "BW01", *CELL[1:])).order
    cut = '{\n  "name": "ask_user",\n  "arguments": {\n    "question": "Which of these'
    cases = [
        (raw(cut, done="length"), "truncated"),       # hit the 512 token limit
        (raw(cut), "no_tool_call"),
        (raw(""), "no_tool_call"),
        (raw(None), "no_tool_call"),
        ({"model": "olmo-3:7b-instruct", "done_reason": "stop"}, "no_tool_call"),  # no message at all
        (raw("I recommend the first one. Would you like me to proceed?"), "no_tool_call"),
        (raw('["buy"]'), "no_tool_call"),
        (raw('{"product_id": "%s"}' % order[0]), "no_tool_call"),
        (raw('{"name": "buy", "arguments": "%s"}' % order[0]), "no_tool_call"),
        (raw('{"name": 7, "arguments": {}}'), "no_tool_call"),
    ]
    for resp, want in cases:
        n = ad.normalize(resp)
        assert n.tool_calls == []
        assert parse_action(n, order)["type"] == want, resp


# ---------------- (b) end to end: runner protocol and scorer ----------------
class ScriptedOllama(OllamaAdapter):
    """The real Ollama adapter with call() replaced by scripted raw replies,
    keyed by episode (system + user text) and turn (tool replies so far)."""

    def __init__(self, scripts):
        super().__init__("olmo", MODELS["olmo"], tool_choice="required")
        self.scripts = scripts
        self.payloads = []

    def call(self, payload):
        self.payloads.append(payload)
        key = (payload["messages"][0]["content"], payload["messages"][1]["content"])
        turn = sum(1 for m in payload["messages"] if m["role"] == "tool")
        return self.scripts[key][turn]


def run_scripted(cat, tmp_path, plan, **kw):
    """plan: list of (episode, [raw reply per turn]). Returns adapter, rows by episode id."""
    scripts = {}
    for ep, replies in plan:
        r = cat.render(ep)
        scripts[(r.system, r.user)] = replies
    ad = ScriptedOllama(scripts)
    guard = SpendGuard(tmp_path / "spend.json", caps={"ollama": 0.0})
    run = Runner(cat, ad, "t", [ep for ep, _ in plan], guard=guard, log_dir=tmp_path, workers=1,
                 sleep=lambda s: None, **kw)
    out = run.run_sync()
    rows = {x["episode_id"]: x for x in score_run("t", log_dir=tmp_path, catalog=cat)}
    return ad, out, rows


def test_runner_protocol_and_scoring_with_json_actions(cat, tmp_path):
    s0 = [e for e in cat.grid("main") if e.arm == "S0"][:6]
    s1 = [e for e in cat.grid("main") if e.arm == "S1"][:1]
    v = [e for e in cat.grid("main") if e.arm == "V"][:2]
    order = {e.episode_id: cat.render(e).order for e in s0 + s1 + v}
    ask = raw(pretty("ask_user", question="Which one would you like?"))

    def buy(e, i=0):
        return raw(pretty("buy", product_id=order[e.episode_id][i]))

    plan = [
        (s0[0], [buy(s0[0])]),                                   # bought on turn 0
        (s0[1], [ask, buy(s0[1], 1)]),                           # one answered ask, then bought
        (s0[2], [ask, ask]),                                     # S0: a second ask is no purchase
        (s0[3], [raw(pretty("buy", product_id="B000NOTONPAGE"))]),
        (s0[4], [raw("")]),                                      # empty reply
        (s0[5], [raw("Would you like me to proceed and buy this?")]),
        (s1[0], [raw('{"name": "buy", "arguments": {"product_id": "B0', done="length")]),
        (v[0], [ask, ask, buy(v[0], 2)]),                        # V: two answered asks
        (v[1], [ask, ask, ask]),                                 # V: a third ask is no purchase
    ]
    ad, out, rows = run_scripted(cat, tmp_path, plan, allow_daytime_local=True)
    assert out["stop_reason"] is None and out["pending_turns"] == 0
    got = {ep.episode_id: rows[ep.episode_id]["outcome"] for ep, _ in plan}
    assert list(got.values()) == ["bought", "bought", "no_purchase", "invalid_product", "no_tool_call",
                                  "no_tool_call", "truncated", "bought", "no_purchase"]
    assert rows[s0[1].episode_id]["asked"] and rows[s0[1].episode_id]["final_turn"] == 1
    assert rows[v[0].episode_id]["n_asks"] == 2 and rows[v[0].episode_id]["final_turn"] == 2
    assert rows[v[1].episode_id]["n_asks"] == 3
    assert len(ad.payloads) == sum(len(replies) for _, replies in plan)
    # Every turn is constrained the same way, and after an ask the model's own
    # JSON comes back as its turn, followed by the exact scripted reply.
    for p in ad.payloads:
        assert p["format"] == action_schema()
    r_v = cat.render(v[0])
    last_v = [p for p in ad.payloads if p["messages"][1]["content"] == r_v.user
              and p["messages"][0]["content"] == r_v.system][-1]
    assert [m["role"] for m in last_v["messages"]] == ["system", "user", "assistant", "tool", "assistant", "tool"]
    assert last_v["messages"][2] == {"role": "assistant", "content": ask["message"]["content"]}
    assert last_v["messages"][3] == {"role": "tool", "content": r_v.scripted_reply, "tool_name": "ask_user"}
    assert last_v["messages"][5] == {"role": "tool", "content": r_v.followup_reply, "tool_name": "ask_user"}


def test_local_run_pauses_within_one_call_of_7am(cat, tmp_path, monkeypatch):
    import harness.runner as runner_mod
    eps = [e for e in cat.grid("main") if e.arm == "S0"][:8]
    checks = {"n": 0}

    def clock(now=None):  # open for the start check and 3 calls, then 7 am
        checks["n"] += 1
        return checks["n"] <= 4

    monkeypatch.setattr(runner_mod, "local_compute_allowed", clock)
    plan = [(e, [raw(pretty("buy", product_id=cat.render(e).order[0]))]) for e in eps]
    ad, out, rows = run_scripted(cat, tmp_path, plan)
    assert out["stop_reason"] == LOCAL_PAUSE_MSG
    assert len(ad.payloads) == 3  # stopped at the next call, not at the end of the chunk
    # Resuming in the next window sends only the rest.
    monkeypatch.setattr(runner_mod, "local_compute_allowed", lambda now=None: True)
    ad2, out2, rows2 = run_scripted(cat, tmp_path, plan)
    assert len(ad2.payloads) == 5 and out2["done"] == 8
    assert {x["outcome"] for x in rows2.values()} == {"bought"}
