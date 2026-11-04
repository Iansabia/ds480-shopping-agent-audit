"""Request builders and response parsers for each provider, on canned data.
No network calls are made."""
import json

from harness.adapters import make_adapter
from harness.adapters.base import BillingError, looks_like_billing, parse_action


def conv(cat, turn1=False, native=None, call_id="c1"):
    e = cat.make_episode("V", "BW01", "hair_shampoo_fine_straight", "w1_fwd")
    r = cat.render(e)
    c = {"system": r.system, "user": r.user, "history": []}
    if turn1:
        c["history"].append({"assistant_native": native, "tool_call": {"id": call_id, "name": "ask_user",
                             "args": {"question": "Hair type?"}}, "tool_reply": r.scripted_reply})
    return c, r


def test_anthropic_request_settings(cat):
    ad = make_adapter("haiku")
    c, _ = conv(cat)
    p = ad.build_request(c)
    assert p["model"] == "claude-haiku-5-5"
    assert p["thinking"] == {"type": "disabled"}
    assert "temperature" not in p and "top_p" not in p and "top_k" not in p
    assert p["tool_choice"] == {"type": "any", "disable_parallel_tool_use": True}
    assert {t["name"] for t in p["tools"]} == {"ask_user", "buy"}
    assert p["system"] == c["system"]
    json.dumps(p)


def test_anthropic_turn2_and_parse(cat):
    ad = make_adapter("haiku")
    raw = {"id": "msg_1", "model": "claude-haiku-5-5", "stop_reason": "tool_use",
           "content": [{"type": "text", "text": ""},
                       {"type": "tool_use", "id": "toolu_1", "name": "ask_user", "input": {"question": "Hair type?"}}],
           "usage": {"input_tokens": 1800, "output_tokens": 40}}
    n = ad.normalize(raw)
    assert n.model_returned == "claude-haiku-5-5" and n.usage["input_tokens"] == 1800
    a = parse_action(n, [])
    assert a["type"] == "ask" and a["call_id"] == "toolu_1"
    c, r = conv(cat, True, n.assistant_native, "toolu_1")
    p = ad.build_request(c)
    assert p["messages"][1]["role"] == "assistant"
    assert all(b.get("text", "x") for b in p["messages"][1]["content"])  # empty text block dropped
    tr = p["messages"][2]["content"][0]
    assert tr == {"type": "tool_result", "tool_use_id": "toolu_1", "content": r.scripted_reply}


def test_anthropic_refusal(cat):
    ad = make_adapter("haiku")
    n = ad.normalize({"model": "claude-haiku-5-5", "stop_reason": "refusal", "content": [], "usage": {}})
    assert parse_action(n, [])["type"] == "refusal"


def test_openai_request_settings(cat):
    ad = make_adapter("luna")
    c, _ = conv(cat)
    p = ad.build_request(c)
    assert p["model"] == "gpt-6-luna"
    assert p["reasoning"] == {"effort": "none"}
    assert "temperature" not in p
    assert p["tool_choice"] == "required" and p["parallel_tool_calls"] is False and p["store"] is False
    assert p["instructions"] == c["system"]
    json.dumps(p)
    assert make_adapter("luna", service_tier="flex").build_request(c)["service_tier"] == "flex"


def test_openai_parse_and_turn2(cat):
    ad = make_adapter("luna")
    c0, r = conv(cat)
    raw = {"id": "resp_1", "model": "gpt-6-luna-2026-10-01", "status": "completed",
           "output": [{"type": "function_call", "id": "fc_1", "call_id": "call_9", "name": "buy",
                       "arguments": json.dumps({"product_id": r.order[2]}), "status": "completed"}],
           "usage": {"input_tokens": 1500, "output_tokens": 30, "output_tokens_details": {"reasoning_tokens": 0}}}
    n = ad.normalize(raw)
    a = parse_action(n, r.order)
    assert a == {"type": "buy", "product_id": r.order[2], "valid": True, "call_id": "call_9", "call_name": "buy"}
    assert n.model_returned == "gpt-6-luna-2026-10-01"
    c, _ = conv(cat, True, n.assistant_native, "call_9")
    p = ad.build_request(c)
    assert p["input"][-1] == {"type": "function_call_output", "call_id": "call_9", "output": r.scripted_reply}
    assert p["input"][1]["type"] == "function_call" and "id" not in p["input"][1]


def test_gemini_request_settings_and_roundtrip(cat):
    from google.genai import types
    ad = make_adapter("flashlite")
    c0, r = conv(cat)
    p = ad.build_request(c0)
    assert p["model"] == "gemini-3.5-flash-lite"
    assert p["config"]["tool_config"]["function_calling_config"]["mode"] == "ANY"
    assert "temperature" not in p["config"]
    contents, config = ad._typed(p)
    assert config.system_instruction == c0["system"]
    resp = types.GenerateContentResponse(
        model_version="gemini-3.5-flash-lite-001",
        candidates=[types.Candidate(finish_reason="STOP", content=types.Content(role="model", parts=[
            types.Part(function_call=types.FunctionCall(name="ask_user", args={"question": "Hair type?"}),
                       thought_signature=b"\x01\x02sig")]))],
        usage_metadata=types.GenerateContentResponseUsageMetadata(prompt_token_count=1700, candidates_token_count=12,
                                                                  thoughts_token_count=5))
    raw = resp.model_dump(mode="json", exclude_none=True)
    json.dumps(raw)
    n = ad.normalize(raw)
    assert n.usage == {"input_tokens": 1700, "output_tokens": 17, "thinking_tokens": 5}
    a = parse_action(n, r.order)
    assert a["type"] == "ask"
    c1, _ = conv(cat, True, n.assistant_native, None)
    p1 = ad.build_request(c1)
    contents, _ = ad._typed(p1)
    assert contents[1].parts[0].thought_signature == b"\x01\x02sig"
    assert contents[2].parts[0].function_response.response == {"result": r.scripted_reply}


def test_gemini_safety_block_is_refusal(cat):
    ad = make_adapter("flashlite")
    n = ad.normalize({"prompt_feedback": {"block_reason": "SAFETY"}, "model_version": "x"})
    assert parse_action(n, [])["type"] == "refusal"


def test_ollama_request_settings_and_parse(cat):
    ad = make_adapter("olmo")
    c0, r = conv(cat)
    p = ad.build_request(c0)
    assert p["model"] == "olmo-3:7b-instruct"
    assert p["options"]["temperature"] == 0 and p["options"]["seed"] == 480 and p["options"]["num_ctx"] == 16384
    assert p["messages"][0] == {"role": "system", "content": c0["system"]}
    raw = {"model": "olmo-3:7b-instruct", "done_reason": "stop", "prompt_eval_count": 1900, "eval_count": 20,
           "message": {"role": "assistant", "content": "",
                       "tool_calls": [{"function": {"name": "buy", "arguments": {"product_id": r.order[0]}}}]}}
    a = parse_action(ad.normalize(raw), r.order)
    assert a["type"] == "buy" and a["valid"]
    # text fallback when the model writes the call as JSON
    raw2 = {"model": "olmo", "done_reason": "stop",
            "message": {"role": "assistant", "content": 'Sure. {"name": "buy", "arguments": {"product_id": "%s"}}' % r.order[1]}}
    a2 = parse_action(ad.normalize(raw2), r.order)
    assert a2["type"] == "buy" and a2["recovered_from_text"]


def test_billing_patterns():
    assert looks_like_billing("Your credit balance is too low to access the Anthropic API.")
    assert looks_like_billing("You exceeded your current quota, please check your plan and billing details.")
    assert looks_like_billing("no credits remaining")
    assert not looks_like_billing("429 Too Many Requests: rate limit, retry in 20s")
    assert issubclass(BillingError, Exception)
