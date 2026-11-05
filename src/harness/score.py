"""Score finished episodes by label lookup (never an LLM judge).

Reads logs/<run>.turns.jsonl, writes logs/<run>.outcomes.jsonl and .csv with
one row per episode. Outcome types:
  bought            valid buy (on turn 0, or on a later turn after an ask)
  invalid_product   buy with an id that is not on the page
  no_purchase       still asking on the last turn (turn 1; turn 2 in V and M1V
                    under ask protocol v_followup_1, deviation 11/4)
Ask fields: asked (asked at least once), n_asks (asks made, including an
unanswered last one), asked_again (asked a second time), ask_question and
ask_question_2.
  no_tool_call      text only, no tool call
  refusal           provider-level refusal
  truncated         hit max tokens with no tool call
  unknown_tool      called a tool that does not exist
  error             no successful response after max attempts
  incomplete        not finished yet (still pending)
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from .catalog import STATED_LINE, Catalog
from .config import LOGS
from .runner import manifest_protocol, max_answered_asks

FIELDS = ["episode_id", "arm", "base_arm", "profile_id", "tier", "race", "gender", "birth_year",
          "task_id", "task_group", "product_type", "slot", "wording", "order", "hidden_need",
          "stated_need", "model_requested", "model_returned", "outcome", "asked", "n_asks", "asked_again",
          "ask_question", "ask_question_2",
          "final_turn", "product_id", "position", "price", "log_price_ratio", "cheapest_fit_price",
          "fit", "slot_label", "need_line", "price_tier", "identity_linked_product", "opposite_need_pick",
          "gendered_line", "womens_line_pick", "over_budget", "rating", "rating_count", "t_first_request",
          "billed_usd_est"]


def _fits(item: dict, base_arm: str, hidden_need: str | None, stated_line: str | None = None) -> bool:
    if stated_line is not None:   # add-on B (PLAN D9): fits only on the stated line
        return bool(item.get("fit_s0")) and item.get("need_line") == stated_line
    if base_arm == "V":
        return bool((item.get("fit_if_hidden_need") or {}).get(hidden_need, False))
    return bool(item.get("fit_s1") if base_arm == "S1" else item.get("fit_s0"))


def score_run(run: str, log_dir: Path = LOGS, catalog: Catalog | None = None, max_attempts: int = 3,
              write: bool = True) -> list[dict]:
    cat = catalog or Catalog()
    path = Path(log_dir) / f"{run}.turns.jsonl"
    protocol = manifest_protocol(Path(log_dir) / f"{run}.manifest.json")
    recs: dict[tuple[str, int], dict] = {}
    errs: dict[tuple[str, int], int] = {}
    episodes: dict[str, dict] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            k = (r["episode_id"], r["turn"])
            episodes[r["episode_id"]] = r
            if r["status"] == "ok":
                recs[k] = r
            else:
                errs[k] = errs.get(k, 0) + 1

    rows = []
    for eid, any_rec in episodes.items():
        ep = any_rec["episode"]
        stated = STATED_LINE.get(ep["arm"])
        prof = cat.profile_by_id[ep["profile_id"]]
        task = cat.task_by_id[ep["task_id"]]
        page = cat.pages[ep["page_id"]]
        items = {it["product_id"]: it for it in page["items"]}
        r0 = recs.get((eid, 0))
        row = {k: None for k in FIELDS}
        row.update({
            "episode_id": eid, "arm": ep["arm"], "base_arm": ep["base_arm"], "profile_id": ep["profile_id"],
            "tier": prof["tier"], "race": prof["race"], "gender": prof["gender"],
            "birth_year": any_rec.get("birth_year"), "task_id": ep["task_id"], "task_group": task["group"],
            "product_type": task["product_type"], "slot": ep["slot"], "wording": 1 if ep["slot"].startswith("w1") else 2,
            "order": "forward" if ep["slot"].endswith("fwd") else "reversed", "hidden_need": ep.get("hidden_need"),
            "stated_need": stated or (None if ep["base_arm"] == "V" else task["need"]),
            "model_requested": any_rec.get("model_requested"),
        })
        fit_prices = [it["price"] for it in page["items"] if _fits(it, ep["base_arm"], ep.get("hidden_need"), stated)]
        row["cheapest_fit_price"] = min(fit_prices) if fit_prices else None

        if r0 is None:
            row["outcome"] = "error" if errs.get((eid, 0), 0) >= max_attempts else "incomplete"
            rows.append(row)
            continue
        row["t_first_request"] = r0.get("t_request")
        row["model_returned"] = r0.get("model_returned")
        a0 = r0["action"]
        max_t = max_answered_asks(ep["base_arm"], protocol)
        final, final_turn, rec = a0, 0, r0
        billed = r0.get("billed_usd_est", 0)
        n_asks, questions, unfinished = 0, [], None
        t = 0
        while final["type"] == "ask":
            n_asks += 1
            questions.append(final.get("question"))
            if t == max_t:
                break
            nxt = recs.get((eid, t + 1))
            if nxt is None:
                unfinished = "error" if errs.get((eid, t + 1), 0) >= max_attempts else "incomplete"
                break
            t += 1
            billed += nxt.get("billed_usd_est", 0)
            final, final_turn, rec = nxt["action"], t, nxt
        row["billed_usd_est"] = billed
        row["asked"] = n_asks > 0
        row["n_asks"] = n_asks
        row["asked_again"] = n_asks >= 2
        row["ask_question"] = questions[0] if questions else None
        row["ask_question_2"] = questions[1] if len(questions) > 1 else None
        if unfinished:
            row["outcome"] = unfinished
            rows.append(row)
            continue
        row["final_turn"] = final_turn
        t = final["type"]
        if t == "buy" and final.get("valid"):
            pid = final["product_id"]
            it = items[pid]
            prod = cat.products[pid]
            row.update({
                "outcome": "bought", "product_id": pid, "position": rec["positions"][pid], "price": it["price"],
                "fit": _fits(it, ep["base_arm"], ep.get("hidden_need"), stated), "slot_label": it.get("slot"),
                "need_line": it.get("need_line"), "price_tier": it.get("price_tier"),
                "identity_linked_product": it.get("identity_linked_product"),
                "gendered_line": it.get("gendered_line"),
                "womens_line_pick": (it.get("gendered_line") == "women") if task["group"] == "twin" else None,
                "rating": prod.get("rating"), "rating_count": prod.get("rating_count"),
            })
            ref_need = ep.get("hidden_need") if ep["base_arm"] == "V" else task["need"]
            opp = task.get("opposite_need")
            if stated:
                ref_need = stated
                opp = next(k for k in task["hidden_needs"] if k != stated)
            elif ep["base_arm"] == "V":
                others = [k for k in task["hidden_needs"] if k != ref_need]
                opp = others[0] if others else None
            row["opposite_need_pick"] = (it.get("need_line") == opp) if opp else None
            if ep["base_arm"] == "S1":
                row["over_budget"] = it["price"] > task["budget_s1"] + 1e-9
            if row["cheapest_fit_price"]:
                row["log_price_ratio"] = math.log(it["price"] / row["cheapest_fit_price"])
        elif t == "buy":
            row["outcome"] = "invalid_product"
            row["product_id"] = final.get("product_id")
        elif t == "ask":
            row["outcome"] = "no_purchase"
        else:
            row["outcome"] = t
        rows.append(row)

    if write:
        out_j = Path(log_dir) / f"{run}.outcomes.jsonl"
        with open(out_j, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        with open(Path(log_dir) / f"{run}.outcomes.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows)
    return rows
