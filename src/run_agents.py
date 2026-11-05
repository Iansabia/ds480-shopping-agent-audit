"""Command line for the agent audit harness.

Examples (run from the project root with the venv):
  .venv/bin/python src/run_agents.py plan --preset main --model haiku
  .venv/bin/python src/run_agents.py run --model haiku --preset pilot --mode sync --limit 20
  .venv/bin/python src/run_agents.py run --model haiku --preset main --mode batch
  .venv/bin/python src/run_agents.py status --run main_haiku
  .venv/bin/python src/run_agents.py score --run main_haiku
  .venv/bin/python src/run_agents.py spend
Keys are read from .env by the code and never printed.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import config  # noqa: E402
from harness.adapters import make_adapter  # noqa: E402
from harness.catalog import PRESETS, Catalog  # noqa: E402
from harness.runner import Runner, StopRun  # noqa: E402
from harness.score import score_run  # noqa: E402
from harness.spend import SpendGuard, worst_case  # noqa: E402


def episodes_for(cat: Catalog, preset: str, limit: int | None):
    eps = Catalog.interleave(cat.grid(preset), preset)
    return eps[:limit] if limit else eps


def cmd_plan(a):
    cat = Catalog()
    eps = episodes_for(cat, a.preset, a.limit)
    from collections import Counter
    print(f"preset {a.preset}: {len(eps)} episodes")
    print("by arm:", dict(Counter(e.arm for e in eps)))
    print("by tier:", dict(Counter(cat.profile_by_id[e.profile_id]["tier"] for e in eps)))
    if a.model:
        ad = make_adapter(a.model)
        sample = eps[: min(200, len(eps))]
        est_in = sum(ad.estimate_input_tokens(ad.build_request(
            {"system": cat.render(e).system, "user": cat.render(e).user, "history": []})) for e in sample) / len(sample)
        s = config.MODELS[a.model]
        for mode in ("std", "batch"):
            pin, pout = s[mode]
            for out_tok in (150, 450):
                calls = len(eps) * 1.3  # assume 30% follow-up turns
                usd = calls * (est_in * pin + out_tok * pout) / 1e6
                print(f"  {mode:5s} est_in~{est_in:.0f} tok, out {out_tok} tok: ${usd:.2f}"
                      + (" (free tier: $0 billed)" if s.get("free_tier") else ""))
        wc = len(eps) * worst_case(a.model, int(est_in), config.MAX_OUTPUT_TOKENS, "batch")
        print(f"  worst-case batch reservation for turn 0: ${wc:.2f} (cap ${config.CAPS_USD[s['provider']]:.2f})")


def cmd_run(a):
    config.load_env()
    cat = Catalog()
    eps = episodes_for(cat, a.preset, a.limit)
    run_name = a.run_name or f"{a.preset}_{a.model}" + (f"_n{a.limit}" if a.limit else "")
    if a.fake:
        from harness.adapters.fake import FakeAdapter
        ad = FakeAdapter()
        guard = SpendGuard(config.LOGS / "spend_fake.json", caps={"fake": 1e9})
        run_name = "FAKE_" + run_name
    else:
        ad = make_adapter(a.model, tool_choice=a.tool_choice,
                          service_tier="flex" if a.mode == "flex" else None)
        if a.min_interval_s is not None and hasattr(ad, "min_interval_s"):
            ad.min_interval_s = a.min_interval_s
        guard = SpendGuard()
    runner = Runner(cat, ad, run_name, eps, guard=guard, mode=a.mode, workers=a.workers,
                    batch_size=a.batch_size, poll_s=a.poll_s, allow_daytime_local=a.allow_daytime_local,
                    preset=a.preset, manifest_extra={"limit": a.limit, "tool_choice": a.tool_choice})
    try:
        if a.mode == "batch":
            out = runner.run_batch(wait=not a.no_wait)
        else:
            out = runner.run_sync()
    except StopRun as e:
        out = {"stop_reason": str(e)}
    print(json.dumps({"run": run_name, **out}, indent=2))
    if out.get("stop_reason"):
        sys.exit(2)


def _runner_from_manifest(run: str) -> Runner:
    m = json.loads((config.LOGS / f"{run}.manifest.json").read_text())
    cat = Catalog()
    eps = episodes_for(cat, m["preset"], m.get("limit"))
    if m["provider"] == "fake":
        from harness.adapters.fake import FakeAdapter
        ad = FakeAdapter()
    else:
        ad = make_adapter(m["model_key"])
    return Runner(cat, ad, run, eps, guard=SpendGuard(), mode=m["mode"], preset=m["preset"])


def cmd_cancel_batches(a):
    config.load_env()
    r = _runner_from_manifest(a.run)
    print(json.dumps({"run": a.run, **r.cancel_open_batches()}, indent=2))


def cmd_status(a):
    r = _runner_from_manifest(a.run)
    print(json.dumps({"run": a.run, **r.status(), "open_batches": list(r.open_batches())}, indent=2))


def cmd_score(a):
    rows = score_run(a.run)
    from collections import Counter
    print(f"{len(rows)} episodes scored -> logs/{a.run}.outcomes.csv")
    print("outcomes:", dict(Counter(r["outcome"] for r in rows)))


def cmd_spend(a):
    g = SpendGuard()
    if a.clear_halt:
        g.clear_halt(a.clear_halt)
    if a.clear_stale:
        # Only sync-call reservations of that run older than 15 minutes (a killed process).
        g.clear_stale_reservations(a.clear_stale[0], run=a.clear_stale[1])
    snap = g.snapshot()
    for p, d in snap["providers"].items():
        print(f"{p:10s} spent ${d['spent_usd']:.4f} of ${d['cap_usd']:.2f} cap | notional ${d['notional_usd']:.4f} | "
              f"calls {d['calls']} | open reservations {len(d['reservations'])} | halted {d['halted']}"
              + (f" ({d['halted_reason']})" if d["halted"] else ""))
    print(snap.get("note", ""))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan", help="count episodes and estimate cost (no API calls)")
    p.add_argument("--preset", choices=PRESETS, required=True)
    p.add_argument("--model", choices=list(config.MODELS))
    p.add_argument("--limit", type=int)
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("run", help="run or resume a grid")
    p.add_argument("--model", choices=list(config.MODELS), required=True)
    p.add_argument("--preset", choices=PRESETS, required=True)
    p.add_argument("--mode", choices=["sync", "flex", "batch"], default="sync",
                   help="flex = OpenAI Flex tier (batch prices, sync calls)")
    p.add_argument("--limit", type=int, help="only the first N episodes of the interleaved grid")
    p.add_argument("--run-name")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--batch-size", type=int, default=5000)
    p.add_argument("--poll-s", type=float, default=60.0)
    p.add_argument("--no-wait", action="store_true", help="batch: submit/collect once and exit")
    p.add_argument("--tool-choice", choices=["required", "auto"], default="required")
    p.add_argument("--allow-daytime-local", action="store_true",
                   help="override the 7pm-7am ET rule for OLMo. Only if Ian says so.")
    p.add_argument("--fake", action="store_true", help="use the fake model (no network, no cost)")
    p.add_argument("--min-interval-s", type=float,
                   help="override the model's sync pacing (Luna's 6.5 s is for free access)")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("status")
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("cancel-batches", help="cancel a run's open batches and free their reservations")
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_cancel_batches)

    p = sub.add_parser("score")
    p.add_argument("--run", required=True)
    p.set_defaults(func=cmd_score)

    p = sub.add_parser("spend")
    p.add_argument("--clear-halt", metavar="PROVIDER")
    p.add_argument("--clear-stale", nargs=2, metavar=("PROVIDER", "RUN"),
                   help="drop call reservations of RUN older than 15 min, e.g. openai namecheck_luna")
    p.set_defaults(func=cmd_spend)

    a = ap.parse_args(argv)
    if a.cmd == "run" and a.model == "olmo" and a.mode != "sync":
        ap.error("OLMo runs only in sync mode")
    a.func(a)


if __name__ == "__main__":
    main()
