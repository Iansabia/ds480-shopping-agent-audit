"""Write data/spotcheck_20.md: 20 random pages (5 per task group, seeded) for Ian's label check."""
import json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(os.path.join(ROOT, "data/pages.json")))["pages"]
T = {t["task_id"]: t for t in json.load(open(os.path.join(ROOT, "data/tasks.json")))["tasks"]}
PR = json.load(open(os.path.join(ROOT, "data/products.json")))["products"]

rng = random.Random(4804)
picked = []
for g in ("hair", "skin", "twin", "neutral"):
    pool = [p for p in P if T[p["task_id"]]["group"] == g]
    picked += rng.sample(pool, 5)

def esc(x):
    return str(x).replace("|", "/").replace("\u2014", "-").replace("\u2013", "-")

out = ["# Spot check: 20 pages", "",
       "Seeded random draw (seed 4804), 5 pages from each task group (hair, skin, twin, neutral), mixing specified and vague pages.",
       "For each row, check that the label matches the product title. Put an X in the last column if a label looks wrong and say why.",
       "",
       "How to read the labels:",
       "- **slot** on a specified page: fit_low / fit_mid / fit_high (fits the request, price tier), fit_over_budget (fits, but costs more than the S1 budget), opposite (fits the other need), near_miss (wrong product type or an adjacent product).",
       "- **slot** on a vague page: A_low ... B_high are the two hidden needs at three price tiers; near_miss fits neither.",
       "- **need line**: which need or line the product serves. Twin pages use womens_line / mens_line.",
       "- **fits**: S0/S1 = fits in the no-budget arm / the budget arm. On vague pages it lists the hidden need(s) the product fits.",
       "- **pos**: position in the forward order (1 = top of the page). The reversed order is the same list flipped.",
       ""]
for p in picked:
    t = T[p["task_id"]]
    out.append(f"## {p['page_id']}")
    out.append("")
    if p["kind"] == "specified":
        out.append(f"- Request (wording 1): \"{t['request_specified'][0]}\"")
        out.append(f"- S1 budget: ${t['budget_s1']:.2f}")
    else:
        out.append(f"- Request (wording 1): \"{t['request_vague'][0]}\"")
        out.append(f"- Hidden needs and scripted replies: " + "; ".join(f"{k} = \"{v}\"" for k, v in t["hidden_needs"].items()))
    out.append("")
    out.append("| pos | slot | need line | tier | price | rating (n) | fits | title | wrong? |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    pos = {pid: i + 1 for i, pid in enumerate(p["order_forward"])}
    for it in sorted(p["items"], key=lambda i: pos[i["product_id"]]):
        x = PR[it["product_id"]]
        if p["kind"] == "specified":
            fits = f"S0 {'yes' if it['fit_s0'] else 'no'}, S1 {'yes' if it['fit_s1'] else 'no'}"
        else:
            f = [k for k, v in it["fit_if_hidden_need"].items() if v]
            fits = ", ".join(f) if f else "neither"
        out.append(f"| {pos[it['product_id']]} | {it['slot']} | {it.get('need_line', '')} | {it['price_tier']} | ${it['price']:.2f} | "
                   f"{x['rating']} ({x['rating_count']}) | {fits} | {esc(x['title'][:140])} ({it['product_id']}) | |")
    out.append("")
open(os.path.join(ROOT, "data/spotcheck_20.md"), "w").write("\n".join(out) + "\n")
print("wrote", len(picked), "pages")
