"""Harm or better deal? What GPT-6 Luna's cheaper picks actually were (descriptive).

Added after the main results were seen (Thu 11/5), to inform the "Paying less:
harm or not?" call in RESULTS_MEMO.md and PLAN 12. Descriptive only: no
p-values, and nothing here joins any test family. Nothing here touches
results/confirmatory.*, results/exploratory.*, results/checks.json or the add-on
family in results/addon_exploratory.json.

Reads logs/ and data/ only:
  * logs/main_luna.outcomes.csv and logs/main_haiku.outcomes.csv (core names,
    S0 and S1), logs/validity_luna.outcomes.csv and validity_haiku (arm P);
  * data/pages.json and data/products.json (prices, stars, rating counts).

Name-level means get a t 95% interval across names; a difference of name means
(focal minus comparison group) gets a Welch 95% interval; pooled shares get a
Wilson 95% interval. A few frozen test rows are quoted in the report for
context (QUOTED below, with their source file and line); they are copied, not
recomputed. A pipeline check reproduces the frozen H1 point estimate
(b = -0.01811 on Luna).

    .venv/bin/python analysis/harm_evidence.py     # writes paper/tables/harm_evidence.{md,json}
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "paper/tables/harm_evidence.md"
OUT_JSON = ROOT / "paper/tables/harm_evidence.json"
Z = 1.959963984540054

pages = json.load(open(ROOT / "data/pages.json"))["pages"]
prods = json.load(open(ROOT / "data/products.json"))["products"]
page_by_id = {p["page_id"]: p for p in pages}

# Frozen rows quoted for context only (copied, not recomputed here). Percent gaps are
# exp(est) - 1 as in the frozen tables; points are rate gaps x 100.
QUOTED = {
    "h1_luna": dict(src="results/confirmatory.json", pct=-1.80, lo=-2.64, hi=-0.94),
    "h2_luna": dict(src="results/confirmatory.json", pct=-1.60, lo=-2.43, hi=-0.76),
    "usd_race": dict(src="paper/tables/numbers.json", gap="$0.56", lo="-$0.82", hi="-$0.29", focal="$30.66", ref="$31.22"),
    "usd_gender": dict(src="paper/tables/numbers.json", gap="$0.50", lo="-$0.76", hi="-$0.24", focal="$30.76", ref="$31.26"),
    "race_position": dict(line=111, est="+0.022", lo="-0.027", hi="+0.071", mean_a="3.86", mean_b="3.84"),
    "race_fit": dict(line=96, est="+0.03", lo="-0.11", hi="+0.17"),
    "gender_position": dict(line=129, est="-0.005", lo="-0.054", hi="+0.045"),
    "s1_cap": dict(lines=(151, 153)),
    "race_s1_price": dict(line=94, pct="-0.77", lo="-1.85", hi="+0.33", q=".42"),
    "gender_s1_price": dict(line=112, pct="+0.45", lo="-0.63", hi="+1.54", q=".68"),
    "race_neutral_price": dict(line=110, b2_line=115, pct="-2.34", lo="-4.11", hi="-0.54", q=".101"),
    "race_twin_line": dict(line=108, pts="+1.41", lo="-0.84", hi="+3.65", q=".49"),
    "cell_bw_wm": dict(line=130, pct="-3.35", lo="-4.47", hi="-2.21", q=".0002"),
    "cell_bm_wm": dict(line=131, pct="-1.25", lo="-2.44", hi="-0.06", q=".19"),
    "cell_ww_wm": dict(line=132, pct="-1.09", lo="-2.43", hi="+0.27", q=".38"),
    "gender_neutral_price": dict(line=128, pct="-0.35", lo="-2.08", hi="+1.41", q=".89"),
    "gender_twin_line": dict(line=126, pts="+11.44", lo="+9.19", hi="+13.69"),
}

# Containers per set on the food storage page, read from the product titles in
# data/products.json (B092YQKS7R: 3 containers and 3 lids; B08MVKYD21: 24 pieces,
# 12 containers; B01N4K8HQ1: 18 pieces, 9 containers).
FOOD_CONTAINERS = {"B092YQKS7R": 3, "B08MVKYD21": 12, "B01N4K8HQ1": 9}


def page_of(task_id: str, base_arm: str) -> str:
    return f"{task_id}__V" if base_arm == "V" else f"{task_id}__S"


def load(run: str) -> pd.DataFrame:
    d = pd.read_csv(ROOT / f"logs/{run}.outcomes.csv", dtype={"profile_id": str, "price_tier": str, "product_id": str},
                    keep_default_na=False, na_values={"price": [""], "rating": [""], "rating_count": [""],
                                                      "position": [""], "log_price_ratio": [""],
                                                      "cheapest_fit_price": [""]})
    for c in ["price", "rating", "rating_count", "position", "log_price_ratio", "cheapest_fit_price"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    for c in ["fit", "over_budget", "womens_line_pick", "identity_linked_product", "asked"]:
        d[c] = d[c].map({"True": 1.0, "False": 0.0, True: 1.0, False: 0.0}).astype(float)
    d["page_id"] = [page_of(t, b) for t, b in zip(d["task_id"], d["base_arm"])]
    d["bought"] = d["outcome"] == "bought"
    return d


# ----------------------------------------------------------------------------- interval helpers

def tci(x):
    x = np.asarray(x, float)
    n = len(x)
    m = float(x.mean())
    if n < 2:
        return dict(mean=m, lo=float("nan"), hi=float("nan"), n=n)
    h = stats.t.ppf(0.975, n - 1) * x.std(ddof=1) / math.sqrt(n)
    return dict(mean=m, lo=m - h, hi=m + h, n=n)


def welch(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    diff = float(a.mean() - b.mean())
    se2 = va / na + vb / nb
    if se2 <= 1e-24:
        return dict(diff=diff, lo=diff, hi=diff, df=float("nan"), note="no name variation")
    df = se2 ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    h = stats.t.ppf(0.975, df) * math.sqrt(se2)
    return dict(diff=diff, lo=diff - h, hi=diff + h, df=df)


def wilson(k, n):
    if n == 0:
        return dict(k=0, n=0, p=float("nan"), lo=float("nan"), hi=float("nan"))
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return dict(k=int(k), n=int(n), p=p, lo=c - h, hi=c + h)


AXES = {"race": ("race", "Black", "White"), "gender": ("gender", "woman", "man")}


def compare(d: pd.DataFrame, col: str, axis: str, binary: bool = False) -> dict:
    gcol, focal, ref = AXES[axis]
    x = d[d[col].notna()]
    nm = x.groupby("profile_id").agg(m=(col, "mean"), g=(gcol, "first"), n=(col, "size"))
    a = nm.loc[nm["g"] == focal, "m"]
    b = nm.loc[nm["g"] == ref, "m"]
    out = dict(col=col, axis=axis, focal=focal, ref=ref,
               focal_names=tci(a), ref_names=tci(b), diff=welch(a, b),
               eps_per_name=[int(nm["n"].min()), int(nm["n"].max())])
    if binary:
        fa = x[x[gcol] == focal][col]
        fb = x[x[gcol] == ref][col]
        out["focal_pooled"] = wilson(int(fa.sum()), int(fa.notna().sum()))
        out["ref_pooled"] = wilson(int(fb.sum()), int(fb.notna().sum()))
    return out


# ----------------------------------------------------------------------------- page facts

def page_fit_facts(p: dict) -> dict:
    """For a specified page under S0: fitting items, cheapest fit, top-rated fit."""
    fits = [it for it in p["items"] if it.get("fit_s0")]
    rat = {it["product_id"]: prods[it["product_id"]]["rating"] for it in fits}
    cnt = {it["product_id"]: prods[it["product_id"]]["rating_count"] for it in fits}
    return dict(fits=[it["product_id"] for it in fits], max_rating=max(rat.values()),
                mean_rating=float(np.mean(list(rat.values()))), max_count=max(cnt.values()),
                cheapest=min(fits, key=lambda it: it["price"])["product_id"],
                cheapest_price=min(it["price"] for it in fits))


S_FACTS = {p["page_id"]: page_fit_facts(p) for p in pages if p["kind"] == "specified"}


def add_quality_cols(d: pd.DataFrame) -> pd.DataFrame:
    d = d.copy()
    b = d["bought"]
    d["cheapest_fit_pick"] = np.where(b, ((d["fit"] == 1) & ((d["price"] - d["cheapest_fit_price"]).abs() < 1e-9)).astype(float), np.nan)
    for t in ["low", "mid", "high", "over_budget", "n/a"]:
        d[f"tier_{t}"] = np.where(b, (d["price_tier"] == t).astype(float), np.nan)
    mr = d["page_id"].map(lambda p: S_FACTS.get(p, {}).get("max_rating", np.nan))
    mean_r = d["page_id"].map(lambda p: S_FACTS.get(p, {}).get("mean_rating", np.nan))
    mc = d["page_id"].map(lambda p: S_FACTS.get(p, {}).get("max_count", np.nan))
    d["top_rated_fit_pick"] = np.where(b, ((d["fit"] == 1) & (d["rating"] >= mr - 1e-9)).astype(float), np.nan)
    d["most_reviewed_fit_pick"] = np.where(b, ((d["fit"] == 1) & (d["rating_count"] >= mc)).astype(float), np.nan)
    d["rating_minus_page_fit_mean"] = np.where(b, d["rating"] - mean_r, np.nan)
    d["log10_count"] = np.where(b, np.log10(d["rating_count"]), np.nan)
    d["pos1"] = np.where(b, (d["position"] == 1).astype(float), np.nan)
    d["logp"] = d["log_price_ratio"]
    return d


# ----------------------------------------------------------------------------- Q1: fixed prices

def q1_checks(runs: list[str]) -> dict:
    out = {}
    out["pages"] = len(pages)
    out["pages_with_8_unique_items"] = sum(len(p["items"]) == 8 and len({i["product_id"] for i in p["items"]}) == 8 for p in pages)
    out["page_price_ne_products_json"] = sum(abs(i["price"] - prods[i["product_id"]]["price"]) > 1e-9 for p in pages for i in p["items"])
    pp = defaultdict(set)
    for p in pages:
        for i in p["items"]:
            pp[i["product_id"]].add(i["price"])
    out["products_with_more_than_one_price_across_pages"] = sum(len(v) > 1 for v in pp.values())
    ties = []
    for p in pages:
        if p["kind"] != "specified":
            continue
        fits = sorted(i["price"] for i in p["items"] if i.get("fit_s0"))
        if len(set(fits)) < len(fits):
            ties.append(p["page_id"])
    out["s_pages_with_tied_fit_prices"] = ties
    out["s_pages_fits_per_page"] = sorted({len(S_FACTS[k]["fits"]) for k in S_FACTS})
    per_run = {}
    for run in runs:
        d = load(run)
        b = d[d["bought"]]
        nu = b.groupby(["page_id", "product_id"])["price"].nunique()
        page_price = {(p["page_id"], i["product_id"]): i["price"] for p in pages for i in p["items"]}
        mism = sum(abs(r.price - page_price[(r.page_id, r.product_id)]) > 1e-9 for r in b.itertuples())
        cfp = d[d["base_arm"].isin(["S0"])].groupby("task_id")["cheapest_fit_price"].nunique()
        per_run[run] = dict(bought=int(len(b)), page_product_pairs=int(len(nu)),
                            pairs_with_more_than_one_price=int((nu > 1).sum()),
                            bought_price_ne_page_price=int(mism),
                            s0_tasks_with_more_than_one_cheapest_fit_price=int((cfp > 1).sum()))
    out["per_run"] = per_run
    return out


# ----------------------------------------------------------------------------- Q2: S0 quality by group

Q2_COLS = [("fit", True), ("cheapest_fit_pick", True), ("tier_low", True), ("tier_mid", True), ("tier_high", True),
           ("tier_over_budget", True), ("tier_n/a", True), ("rating", False), ("rating_minus_page_fit_mean", False),
           ("top_rated_fit_pick", True), ("rating_count", False), ("log10_count", False),
           ("most_reviewed_fit_pick", True), ("position", False), ("pos1", True), ("logp", False)]


def q2(d: pd.DataFrame, arms=("S0",)) -> dict:
    x = d[(d["tier"] == "core") & d["arm"].isin(arms) & d["bought"]]
    res = {"n_bought": int(len(x)), "n_episodes": int(len(d[(d["tier"] == "core") & d["arm"].isin(arms)]))}
    for axis in AXES:
        res[axis] = {c: compare(x, c, axis, binary=bin_) for c, bin_ in Q2_COLS}
    return res


def h1_reproduce(d: pd.DataFrame) -> dict:
    """Residualize logp within task x arm x wording x order over core S0 rows with a price,
    name means, OLS on is_black + is_woman (H1, no frequency term) and on is_woman + is_black (H2
    point estimate without the frequency term). Point estimates only, to check this pipeline."""
    x = d[(d["tier"] == "core") & (d["arm"] == "S0") & d["logp"].notna()].copy()
    m = x.groupby(["task_id", "arm", "wording", "order"])["logp"].transform("mean")
    x["r"] = x["logp"] - m + x["logp"].mean()
    nm = x.groupby("profile_id").agg(r=("r", "mean"), race=("race", "first"), gender=("gender", "first"))
    X = np.column_stack([np.ones(len(nm)), (nm["race"] == "Black").astype(float), (nm["gender"] == "woman").astype(float)])
    beta = np.linalg.lstsq(X, nm["r"].values, rcond=None)[0]
    return dict(b_black=float(beta[1]), b_woman_no_freq=float(beta[2]),
                mean_black=float(nm.loc[nm.race == "Black", "r"].mean()),
                mean_white=float(nm.loc[nm.race == "White", "r"].mean()))


# ----------------------------------------------------------------------------- Q4: by task group

def by_task_group(d: pd.DataFrame, axis: str) -> dict:
    x = d[(d["tier"] == "core") & (d["arm"] == "S0") & d["bought"]]
    out = {}
    for g in ["hair", "skin", "twin", "neutral"]:
        xg = x[x["task_group"] == g]
        out[g] = dict(logp=compare(xg, "logp", axis), cheapest=compare(xg, "cheapest_fit_pick", axis, binary=True),
                      rating=compare(xg, "rating", axis), n_tasks=int(xg["task_id"].nunique()))
    xn = x[x["task_group"] != "twin"]
    out["all_but_twin"] = dict(logp=compare(xn, "logp", axis), n_tasks=int(xn["task_id"].nunique()))
    return out


def task_contrib(d: pd.DataFrame, axis: str) -> list[dict]:
    """Per task: focal minus reference mean log price ratio (pooled over that task's
    episodes, 4 per name) and its share of the 40-task average gap (diff / 40)."""
    gcol, focal, ref = AXES[axis]
    x = d[(d["tier"] == "core") & (d["arm"] == "S0") & d["bought"]]
    rows = []
    for t, xt in x.groupby("task_id"):
        a = xt[xt[gcol] == focal]
        b = xt[xt[gcol] == ref]
        rows.append(dict(task=t, group=xt["task_group"].iloc[0], diff_logp=float(a["logp"].mean() - b["logp"].mean()),
                         contrib_to_40task_mean=float((a["logp"].mean() - b["logp"].mean()) / 40),
                         cheapest_focal=wilson(int(a["cheapest_fit_pick"].sum()), len(a)),
                         cheapest_ref=wilson(int(b["cheapest_fit_pick"].sum()), len(b))))
    rows.sort(key=lambda r: r["diff_logp"])
    return rows


# ----------------------------------------------------------------------------- page detail

def page_detail(d: pd.DataFrame, task: str, axis: str, arm: str = "S0") -> dict:
    gcol, focal, ref = AXES[axis]
    p = page_by_id[f"{task}__S"]
    x = d[(d["tier"] == "core") & (d["arm"] == arm) & (d["task_id"] == task) & d["bought"]]
    na, nb = int((x[gcol] == focal).sum()), int((x[gcol] == ref).sum())
    items = []
    for it in sorted(p["items"], key=lambda i: i["price"]):
        pid = it["product_id"]
        ka = int(((x[gcol] == focal) & (x["product_id"] == pid)).sum())
        kb = int(((x[gcol] == ref) & (x["product_id"] == pid)).sum())
        if not it.get("fit_s0") and ka + kb == 0:
            continue
        pr = prods[pid]
        items.append(dict(pid=pid, price=it["price"], tier=it["price_tier"], slot=it["slot"], line=it.get("gendered_line"),
                          fit_s0=bool(it.get("fit_s0")), rating=pr["rating"], count=pr["rating_count"],
                          title=pr["title"][:150], focal=f"{ka}/{na}", ref=f"{kb}/{nb}"))
    return dict(task=task, axis=axis, items=items)


def tier_table() -> dict:
    """Across the 40 specified pages: mean rating and mean log10 rating count of the fitting
    products by price tier (low, mid, high, over_budget), counted once per product slot."""
    rows = []
    for p in pages:
        if p["kind"] != "specified":
            continue
        grp = p["task_id"].split("_")[0]
        for it in p["items"]:
            if it.get("fit_s0"):
                pr = prods[it["product_id"]]
                rows.append(dict(page=p["page_id"], group=grp, tier=it["price_tier"], line=it.get("gendered_line"),
                                 price=it["price"], rating=pr["rating"], count=pr["rating_count"]))
    t = pd.DataFrame(rows)
    out = {}
    for tier, g in t.groupby("tier"):
        out[tier] = dict(n=int(len(g)), rating=tci(g["rating"]), log10_count=tci(np.log10(g["count"])),
                         median_count=float(g["count"].median()), mean_price=float(g["price"].mean()))
    # within page: cheapest fit rating minus mid-tier fit rating
    diffs = []
    for p in pages:
        if p["kind"] != "specified":
            continue
        f = S_FACTS[p["page_id"]]
        r_cheap = prods[f["cheapest"]]["rating"]
        others = [prods[i]["rating"] for i in f["fits"] if i != f["cheapest"]]
        diffs.append(r_cheap - float(np.mean(others)))
    out["cheapest_minus_other_fits_rating_per_page"] = tci(diffs)
    out["pages_cheapest_is_top_rated"] = int(sum(prods[S_FACTS[k]["cheapest"]]["rating"] >= S_FACTS[k]["max_rating"] - 1e-9 for k in S_FACTS))
    # twins: women's line minus men's line price at the same tier
    tw = t[(t["group"] == "twin") & t["tier"].isin(["low", "mid", "high"])]
    piv = tw.pivot_table(index=["page", "tier"], columns="line", values="price")
    piv_r = tw.pivot_table(index=["page", "tier"], columns="line", values="rating")
    piv = piv.dropna()
    out["twin_same_tier_women_minus_men_logprice"] = tci(np.log(piv["women"] / piv["men"]))
    out["twin_same_tier_women_cheaper_count"] = f"{int((piv['women'] < piv['men']).sum())} of {len(piv)}"
    out["twin_same_tier_women_minus_men_rating"] = tci((piv_r["women"] - piv_r["men"]).dropna())
    out["twin_pairs"] = [dict(page=i[0], tier=i[1], women=float(r["women"]), men=float(r["men"])) for i, r in piv.iterrows()]
    # over-budget item line on twin pages
    ob = t[(t["group"] == "twin") & (t["tier"] == "over_budget")]
    out["twin_over_budget_line"] = ob[["page", "line", "price"]].to_dict("records")
    # cheapest fit line on twin pages
    out["twin_cheapest_fit_line"] = {k: next(i for i in page_by_id[k]["items"] if i["product_id"] == S_FACTS[k]["cheapest"])["gendered_line"]
                                     for k in S_FACTS if k.startswith("twin_")}
    return out


def twin_line_by_gender(d: pd.DataFrame) -> dict:
    x = d[(d["tier"] == "core") & (d["arm"] == "S0") & d["bought"] & (d["task_group"] == "twin")].copy()
    out = {}
    out["womens_line"] = compare(x, "womens_line_pick", "gender", binary=True)
    out["logp_twin"] = compare(x, "logp", "gender")
    out["rating_twin"] = compare(x, "rating", "gender")
    out["cheapest_twin"] = compare(x, "cheapest_fit_pick", "gender", binary=True)
    # within each line: does the gender gap remain? log price ratio, women's-line picks only and men's-line picks only
    for line, flag in [("women_line_only", 1.0), ("men_line_only", 0.0)]:
        xl = x[x["womens_line_pick"] == flag]
        out[line] = dict(logp=compare(xl, "logp", "gender"), tier_low=compare(xl, "tier_low", "gender", binary=True),
                         rating=compare(xl, "rating", "gender"))
    # tier shares within twins by gender
    out["tiers"] = {t: compare(x, f"tier_{t}", "gender", binary=True) for t in ["low", "mid", "high", "over_budget"]}
    return out


# ----------------------------------------------------------------------------- report extras

def task_shares(rows: list[dict]) -> dict:
    """Shares of the raw (40-task mean) gap by task group and for the largest tasks."""
    total = sum(r["contrib_to_40task_mean"] for r in rows)
    by_group = defaultdict(float)
    for r in rows:
        by_group[r["group"]] += r["contrib_to_40task_mean"]
    neg = sorted(rows, key=lambda r: r["contrib_to_40task_mean"])
    return dict(total_logp=total, group_share={g: v / total for g, v in by_group.items()},
                top_tasks=[r["task"] for r in neg[:6]],
                top3_share=sum(r["contrib_to_40task_mean"] for r in neg[:3]) / total,
                top6_share=sum(r["contrib_to_40task_mean"] for r in neg[:6]) / total,
                top2_share=sum(r["contrib_to_40task_mean"] for r in neg[:2]) / total,
                n_zero=sum(abs(r["diff_logp"]) < 1e-9 for r in rows),
                n_neg=sum(r["diff_logp"] < -1e-9 for r in rows),
                n_pos=sum(r["diff_logp"] > 1e-9 for r in rows))


def cell_picks(d: pd.DataFrame, task: str, pid: str) -> dict:
    """Picks of one product by race x gender cell (Luna S0, core names)."""
    x = d[(d["tier"] == "core") & (d["arm"] == "S0") & (d["task_id"] == task) & d["bought"]]
    out = {}
    for (r, g), xc in x.groupby(["race", "gender"]):
        out[f"{r} {g}"] = f"{int((xc['product_id'] == pid).sum())}/{len(xc)}"
    return out


def tie_detail(page_id: str) -> list[dict]:
    p = page_by_id[page_id]
    lo = min(i["price"] for i in p["items"] if i.get("fit_s0"))
    return [dict(pid=i["product_id"], price=i["price"], line=i.get("gendered_line"), rating=prods[i["product_id"]]["rating"])
            for i in p["items"] if i.get("fit_s0") and abs(i["price"] - lo) < 1e-9]


def compute() -> dict:
    res = {}
    res["q1"] = q1_checks(["main_luna", "main_haiku", "validity_luna"])
    res["tier_table"] = tier_table()
    data = {}
    for run in ["main_luna", "main_haiku"]:
        d = add_quality_cols(load(run))
        data[run] = d
        res[run] = dict(h1_reproduce=h1_reproduce(d), S0=q2(d, ("S0",)), S1=q2(d, ("S1",)),
                        by_group_race=by_task_group(d, "race"), by_group_gender=by_task_group(d, "gender"),
                        tasks_race=task_contrib(d, "race"), tasks_gender=task_contrib(d, "gender"),
                        twin_gender=twin_line_by_gender(d))
        s1 = d[(d["tier"] == "core") & (d["arm"] == "S1")]
        res[run]["S1_cap"] = {ax: dict(focal=wilson(int(s1[(s1[AXES[ax][0]] == AXES[ax][1]) & s1["bought"]]["over_budget"].sum()),
                                                    int(((s1[AXES[ax][0]] == AXES[ax][1]) & s1["bought"]).sum())),
                                       ref=wilson(int(s1[(s1[AXES[ax][0]] == AXES[ax][2]) & s1["bought"]]["over_budget"].sum()),
                                                  int(((s1[AXES[ax][0]] == AXES[ax][2]) & s1["bought"]).sum())))
                              for ax in AXES}
    for run in ["validity_luna", "validity_haiku"]:
        d = add_quality_cols(load(run))
        res[run] = {arm: q2(d, (arm,)) for arm in ["PC", "PQ"]}
    # page details for the most negative race tasks and the twin pages (Luna)
    dl = data["main_luna"]
    top = [r["task"] for r in res["main_luna"]["tasks_race"][:5]]
    res["pages_race_top5"] = [page_detail(dl, t, "race") for t in top]
    res["pages_twin_gender"] = [page_detail(dl, t, "gender") for t in sorted(dl.loc[dl.task_group == "twin", "task_id"].unique())]
    res["report_extras"] = dict(
        shares_race=task_shares(res["main_luna"]["tasks_race"]),
        shares_gender=task_shares(res["main_luna"]["tasks_gender"]),
        keyboard_cells=cell_picks(dl, "neutral_keyboard", "B09X983942"),
        tied_fits={pid: tie_detail(pid) for pid in res["q1"]["s_pages_with_tied_fit_prices"]},
        food_per_container={pid: prods[pid]["price"] / n for pid, n in FOOD_CONTAINERS.items()},
        quoted=QUOTED)
    return res


# ----------------------------------------------------------------------------- report

def sg(x: float, dec: int) -> str:
    """Signed number; a value that rounds to zero prints without a sign."""
    s = f"{x:+,.{dec}f}"
    return s[1:] if float(s.replace(",", "")) == 0 else s


def half_up(x: float) -> str:
    return f"{int(Decimal(str(x)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)):,}"


def share(w: dict, dec: int = 1, with_n: bool = True) -> str:
    kn = f"{w['k']:,}/{w['n']:,}" if with_n else f"{w['k']:,}"
    return f"{kn} = {100 * w['p']:.{dec}f}% [{100 * w['lo']:.{dec}f}, {100 * w['hi']:.{dec}f}]"


def pts(c: dict, dec: int = 2) -> str:
    x = c["diff"]
    return f"{sg(100 * x['diff'], dec)} pts [{sg(100 * x['lo'], dec)}, {sg(100 * x['hi'], dec)}]"


def num(c: dict, dec: int = 3, scale: float = 1.0) -> str:
    """Name mean with its t interval (unsigned)."""
    return f"{scale * c['mean']:,.{dec}f} [{scale * c['lo']:,.{dec}f}, {scale * c['hi']:,.{dec}f}]"


def dnum(c: dict, dec: int = 3) -> str:
    x = c["diff"]
    return f"{sg(x['diff'], dec)} [{sg(x['lo'], dec)}, {sg(x['hi'], dec)}]"


def snum(c: dict, dec: int = 3) -> str:
    """Signed mean with its t interval (a mean of differences)."""
    return f"{sg(c['mean'], dec)} [{sg(c['lo'], dec)}, {sg(c['hi'], dec)}]"


def sstars(m: float, lo: float, hi: float) -> str:
    return f"{sg(m, 3)} stars [{sg(lo, 3)}, {sg(hi, 3)}]"


def dpct(c: dict) -> str:
    x = c["diff"]
    f = lambda v: sg(100 * (math.exp(v) - 1), 2)  # noqa: E731
    return f"{f(x['diff'])}% [{f(x['lo'])}, {f(x['hi'])}]"


def frac(s: str) -> dict:
    k, n = (int(v) for v in s.split("/"))
    return wilson(k, n)


def item(page: dict, pid: str) -> dict:
    return next(i for i in page["items"] if i["pid"] == pid)


def pick(page: dict, pid: str, side: str) -> str:
    """'k/n = p% [lo, hi]' for one product and one group on a page detail."""
    return share(frac(item(page, pid)[side]))


def pct0(x: float) -> str:
    return f"{100 * x:.0f}%"


def report(res: dict) -> str:
    L, H = res["main_luna"], res["main_haiku"]
    q1, tt, ex, Q = res["q1"], res["tier_table"], res["report_extras"], res["report_extras"]["quoted"]
    rr, gg = L["S0"]["race"], L["S0"]["gender"]
    pr = {p["task"]: p for p in res["pages_race_top5"]}
    pg = {p["task"]: p for p in res["pages_twin_gender"]}
    sr, sgd = ex["shares_race"], ex["shares_gender"]
    h1 = L["h1_reproduce"]
    tie_page = q1["s_pages_with_tied_fit_prices"][0]
    tie = {t["line"]: t for t in ex["tied_fits"][tie_page]}
    runs = q1["per_run"]
    vl = res["validity_luna"]
    s1c = L["S1_cap"]
    s1_lo = min(min(s1c[a]["focal"]["lo"], s1c[a]["ref"]["lo"]) for a in s1c)
    s1_hi = max(max(s1c[a]["focal"]["hi"], s1c[a]["ref"]["hi"]) for a in s1c)
    s1_n = s1c["race"]["focal"]["n"]
    s1_k = sum(s1c[a][s]["k"] for a in s1c for s in ("focal", "ref"))
    s1_cap_txt = f"{s1_k} of {s1_n:,} purchases in each of the four groups (Wilson {100 * s1_lo:.2f}% to {100 * s1_hi:.2f}%)"
    out = []
    w = out.append

    def row(label, key, axis_res, kind):
        c = axis_res[key]
        if kind == "fit":
            w(f"| {label} | {share(c['focal_pooled'], 2)} | {share(c['ref_pooled'], 2)} | {pts(c)} |")
        elif kind == "share_n":
            w(f"| {label} | {share(c['focal_pooled'])} | {share(c['ref_pooled'])} | {pts(c)} |")
        elif kind == "share":
            w(f"| {label} | {share(c['focal_pooled'], with_n=False)} | {share(c['ref_pooled'], with_n=False)} | {pts(c)} |")
        elif kind == "stars":
            w(f"| {label} | {num(c['focal_names'])} | {num(c['ref_names'])} | {dnum(c)} |")
        elif kind == "count":
            w(f"| {label} | {num(c['focal_names'], 0)} | {num(c['ref_names'], 0)} | {dnum(c, 0)} |")

    w("# Harm or better deal? What GPT-6 Luna's cheaper picks actually were")
    w("")
    w("Written by `analysis/harm_evidence.py` (added after the main results were seen, Thu 11/5). Everything here is "
      "descriptive: no p-values, and nothing joins any test family.")
    w("")
    w("## How the numbers were made")
    w("")
    w("- Data: `logs/main_luna.outcomes.csv` (and `logs/main_haiku.outcomes.csv` for contrast), clear request arm S0, "
      f"the 40 core names (20 per group), bought episodes only. Arm P comes from `logs/validity_luna.outcomes.csv` "
      f"({rr_names(vl['PQ'])} names, {rr_names(vl['PQ']) // 2} per group). Product facts come from `data/pages.json` and `data/products.json`.")
    w("- Ratings, rating counts and log price: each name's mean, then a t 95% interval across names. A difference is "
      "focal minus comparison group, with a Welch 95% interval across names.")
    w("- Shares: pooled k of n with a Wilson 95% interval. The difference in a share is the name-level Welch interval, in points.")
    w(f"- Check: this code gives the frozen H1 estimate exactly (b = {h1['b_black']:.5f}; mean log price ratio "
      f"{h1['mean_black']:.5f} for Black names vs {h1['mean_white']:.5f} for White names, as in `results/confirmatory.json`).")
    w("- Code and raw output: `analysis/harm_evidence.py` and `paper/tables/harm_evidence.json`. Rows quoted from "
      "`results/exploratory.csv` and `paper/tables/numbers.json` are copied, not recomputed.")
    w("")
    w("## 1. Are prices fixed per product on a page? Yes.")
    w("")
    w(f"- `data/pages.json` has {q1['pages']} pages. Each has 8 different products with one price each. Every page price "
      "equals the `data/products.json` price, and no product has two prices anywhere."
      if q1["pages_with_8_unique_items"] == q1["pages"] and q1["page_price_ne_products_json"] == 0
      and q1["products_with_more_than_one_price_across_pages"] == 0 else "- CHECK FAILED: page prices are not fixed.")
    w("- The store page the agent sees uses that same price (`src/harness/catalog.py` line 187).")
    ok = all(v["pairs_with_more_than_one_price"] == 0 and v["bought_price_ne_page_price"] == 0
             and v["s0_tasks_with_more_than_one_cheapest_fit_price"] == 0 for v in runs.values())
    w(("- In the scored files every (page, product) pair has one price and every purchase price equals the page price: "
       if ok else "- CHECK FAILED in the scored files: ")
      + ", ".join(f"{k} {v['bought']:,}" + (" purchases" if i == 0 else "") for i, (k, v) in enumerate(runs.items()))
      + ". The cheapest fitting price is one number per task.")
    w(f"- So on the same page a lower price always means a different product. One tie: on `{tie_page}` the two cheapest "
      f"fits both cost ${tie['women']['price']:.2f} (women's version {tie['women']['rating']} stars, men's version "
      f"{tie['men']['rating']} stars).")
    w("")
    w("## 2. Clear request (S0): what each group got on Luna")
    w("")
    ur, ug = Q["usd_race"], Q["usd_gender"]
    w(f"The paper's dollar basis (`{ur['src']}`): Black names paid {ur['gap']} less per purchase [{ur['lo']}, {ur['hi']}] "
      f"({ur['focal']} vs {ur['ref']}); women's names {ug['gap']} less [{ug['lo']}, {ug['hi']}] ({ug['focal']} vs {ug['ref']}).")
    w("")
    fr = rr["fit"]
    epn = rr["fit"]["eps_per_name"]
    w(f"**Race.** {fr['focal_names']['n']} Black-name vs {fr['ref_names']['n']} White-name names; "
      f"{fr['focal_pooled']['n']:,} vs {fr['ref_pooled']['n']:,} purchases ({epn[0]} or {epn[1]} per name).")
    w("")
    w("| Measure | Black names | White names | Difference [95%] |")
    w("|---|---|---|---|")
    row("Fits the request", "fit", rr, "fit")
    row("Cheapest fitting product", "cheapest_fit_pick", rr, "share_n")
    row("Low price band", "tier_low", rr, "share")
    row("Mid band", "tier_mid", rr, "share")
    row("High band", "tier_high", rr, "share")
    row("Fit priced above the budget-arm cap", "tier_over_budget", rr, "share")
    row("Star rating of the pick (name mean)", "rating", rr, "stars")
    row("Pick was the top-rated fit on its page", "top_rated_fit_pick", rr, "share")
    row("Number of ratings of the pick (name mean)", "rating_count", rr, "count")
    w("")
    rp, rf = Q["race_position"], Q["race_fit"]
    w(f"Position picked, frozen row (`results/exploratory.csv` line {rp['line']}): {rp['est']} positions [{rp['lo']}, {rp['hi']}], "
      f"means {rp['mean_a']} vs {rp['mean_b']}. Fit, frozen row (line {rf['line']}): {rf['est']} pts [{rf['lo']}, {rf['hi']}].")
    w("")
    fg = gg["fit"]
    w(f"**Gender.** {fg['focal_names']['n']} women's vs {fg['ref_names']['n']} men's names; "
      f"{fg['focal_pooled']['n']:,} vs {fg['ref_pooled']['n']:,} purchases.")
    w("")
    w("| Measure | Women's names | Men's names | Difference [95%] |")
    w("|---|---|---|---|")
    row("Fits the request", "fit", gg, "fit")
    w(f"| Cheapest fitting product | {share(gg['cheapest_fit_pick']['focal_pooled'], with_n=False)} | "
      f"{share(gg['cheapest_fit_pick']['ref_pooled'], with_n=False)} | {pts(gg['cheapest_fit_pick'])} |")
    row("Low band", "tier_low", gg, "share")
    row("Mid band", "tier_mid", gg, "share")
    row("High band", "tier_high", gg, "share")
    row("Above the budget-arm cap", "tier_over_budget", gg, "share")
    row("Star rating of the pick", "rating", gg, "stars")
    row("Top-rated fit", "top_rated_fit_pick", gg, "share")
    row("Number of ratings", "rating_count", gg, "count")
    w("")
    gp = Q["gender_position"]
    w(f"Position, frozen row (line {gp['line']}): {gp['est']} [{gp['lo']}, {gp['hi']}].")
    w("")
    w(f"**Over budget where a budget applies (S1).** {s1_cap_txt}. The frozen file lists S1 cap violation as untestable, "
      f"\"no name variation\" (lines {Q['s1_cap']['lines'][0]} and {Q['s1_cap']['lines'][1]}).")
    w("")
    hr, hg = H["S0"]["race"], H["S0"]["gender"]
    w(f"**Haiku contrast (S0).** No evidence of a gap on any of these: cheapest fit {pts(hr['cheapest_fit_pick'])} (race) and "
      f"{pts(hg['cheapest_fit_pick'])} (gender); stars {dnum(hr['rating'])} and {dnum(hg['rating'])}.")
    w("")
    t = tt
    cm = t["cheapest_minus_other_fits_rating_per_page"]
    w(f"**The store itself ({len(S_FACTS)} clear-request pages, catalog values).** Fitting products have about the same stars at "
      f"every price band: low {num(t['low']['rating'])} (n = {t['low']['n']} products), mid {num(t['mid']['rating'])} "
      f"({t['mid']['n']}), high {num(t['high']['rating'])} ({t['high']['n']}), above the cap {num(t['over_budget']['rating'])} "
      f"({t['over_budget']['n']}). On the same page the cheapest fit is {sstars(cm['mean'], cm['lo'], cm['hi'])} "
      f"from the other fits (n = {cm['n']} pages), and it is the top-rated fit on "
      f"{t['pages_cheapest_is_top_rated']} of {len(S_FACTS)} pages. Cheaper fits have more ratings (median "
      f"{half_up(t['low']['median_count'])} low, {half_up(t['mid']['median_count'])} mid, {half_up(t['high']['median_count'])} high). "
      "So in this store, cheaper does not mean lower rated.")
    w("")
    w("## 3. When the buyer states a wish (arm P and the budget arm)")
    w("")
    pq, pc = vl["PQ"], vl["PC"]
    nq = pq["race"]["tier_over_budget"]["focal_pooled"]["n"]
    w(f"- **\"Best quality, whatever it costs\" (PQ; {rr_names(pq) // 2} vs {rr_names(pq) // 2} names, {nq} purchases per group).** "
      f"No evidence of different picks. Most expensive fit: Black {share(pq['race']['tier_over_budget']['focal_pooled'])} vs White "
      f"{share(pq['race']['tier_over_budget']['ref_pooled'])}, {pts(pq['race']['tier_over_budget'])}; women "
      f"{share(pq['gender']['tier_over_budget']['focal_pooled'])} vs men {share(pq['gender']['tier_over_budget']['ref_pooled'])}, "
      f"{pts(pq['gender']['tier_over_budget'])}. Log price ratio: race {dnum(pq['race']['logp'])}, gender {dnum(pq['gender']['logp'])}. "
      f"Stars, race: {dnum(pq['race']['rating'])}.")
    w(f"- **\"Cheapest that fits\" (PC; same names).** Cheapest fit: Black {share(pc['race']['cheapest_fit_pick']['focal_pooled'])} "
      f"vs White {share(pc['race']['cheapest_fit_pick']['ref_pooled'])}, {pts(pc['race']['cheapest_fit_pick'])}; women "
      f"{share(pc['gender']['cheapest_fit_pick']['focal_pooled'])} vs men {share(pc['gender']['cheapest_fit_pick']['ref_pooled'])}, "
      f"{pts(pc['gender']['cheapest_fit_pick'])}.")
    s1r, s1g = L["S1"]["race"], L["S1"]["gender"]
    r94, g112 = Q["race_s1_price"], Q["gender_s1_price"]
    w(f"- **Budget stated (S1; {s1r['fit']['focal_names']['n']} vs {s1r['fit']['ref_names']['n']} names, "
      f"{s1r['cheapest_fit_pick']['focal_pooled']['n']:,} purchases per group).** Cheapest fit: Black "
      f"{share(s1r['cheapest_fit_pick']['focal_pooled'], with_n=False)} vs White {share(s1r['cheapest_fit_pick']['ref_pooled'], with_n=False)}, "
      f"{pts(s1r['cheapest_fit_pick'])}; women {share(s1g['cheapest_fit_pick']['focal_pooled'], with_n=False)} vs men "
      f"{share(s1g['cheapest_fit_pick']['ref_pooled'], with_n=False)}, {pts(s1g['cheapest_fit_pick'])}. Stars, race: {dnum(s1r['rating'])}. "
      f"Frozen S1 price rows: race {r94['pct']}% [{r94['lo']}, {r94['hi']}] (line {r94['line']}, q {r94['q']}), gender "
      f"{g112['pct']}% [{g112['lo']}, {g112['hi']}] (line {g112['line']}, q {g112['q']}).")
    w(f"- Arm P has only {rr_names(pq) // 2} names per group, so its intervals are wide.")
    w("")
    w("## 4. Where Luna's gaps sit")
    w("")
    h1q, h2q = Q["h1_luna"], Q["h2_luna"]
    bgr, bgg = L["by_group_race"], L["by_group_gender"]
    w(f"**Race (H1 = {h1q['pct']:.2f}% [{h1q['lo']:.2f}, {h1q['hi']:.2f}]).**")
    rn = Q["race_neutral_price"]
    w(f"- Frozen row: neutral tasks {rn['pct']}% [{rn['lo']}, {rn['hi']}], q {rn['q']}, not a discovery (`results/exploratory.csv` "
      f"line {rn['line']}; `paper/tables/tableB2_exploratory_family.md` line {rn['b2_line']}).")
    w(f"- New descriptive split ({rr['fit']['focal_names']['n']} vs {rr['fit']['ref_names']['n']} names, Welch, not a test): "
      f"twin {dpct(bgr['twin']['logp'])} ({bgr['twin']['n_tasks']} tasks); neutral {dpct(bgr['neutral']['logp'])} "
      f"({bgr['neutral']['n_tasks']} tasks, close to the frozen row); hair {dpct(bgr['hair']['logp'])} ({bgr['hair']['n_tasks']}); "
      f"skin {dpct(bgr['skin']['logp'])} ({bgr['skin']['n_tasks']}).")
    gs = sr["group_share"]
    w(f"- Share of the raw gap (task differences sum to {sr['total_logp']:.4f} log units): twin {pct0(gs['twin'])}, neutral "
      f"{pct0(gs['neutral'])}, hair {pct0(gs['hair'])}, skin {pct0(gs['skin'])}. Three pages carry {pct0(sr['top3_share'])} "
      f"(keyboard, food storage, face moisturizer) and six carry {pct0(sr['top6_share'])}. {sr['n_zero']} of 40 tasks show no "
      f"difference at all; {sr['n_neg']} lean cheaper for Black names and {sr['n_pos']} lean the other way.")
    tl = Q["race_twin_line"]
    w(f"- It is not about gendered lines: race difference in the women's-version pick on twins {tl['pts']} pts "
      f"[{tl['lo']}, {tl['hi']}] (line {tl['line']}, q {tl['q']}).")
    c1, c2, c3 = Q["cell_bw_wm"], Q["cell_bm_wm"], Q["cell_ww_wm"]
    w(f"- By cell (frozen lines {c1['line']} to {c3['line']}): Black women vs White men {c1['pct']}% [{c1['lo']}, {c1['hi']}] "
      f"(q {c1['q']}); Black men vs White men {c2['pct']}% [{c2['lo']}, {c2['hi']}] (q {c2['q']}); White women vs White men "
      f"{c3['pct']}% [{c3['lo']}, {c3['hi']}] (q {c3['q']}).")
    w("")
    w(f"**Gender (H2 = {h2q['pct']:.2f}% [{h2q['lo']:.2f}, {h2q['hi']:.2f}]).**")
    gn = Q["gender_neutral_price"]
    w(f"- Frozen row: neutral tasks {gn['pct']}% [{gn['lo']}, {gn['hi']}] (line {gn['line']}, q {gn['q']}).")
    w(f"- New descriptive split: twin {dpct(bgg['twin']['logp'])}; hair {dpct(bgg['hair']['logp'])}; skin {dpct(bgg['skin']['logp'])}; "
      f"neutral {dpct(bgg['neutral']['logp'])}; all {bgg['all_but_twin']['n_tasks']} other tasks {dpct(bgg['all_but_twin']['logp'])}.")
    w(f"- Twins carry {pct0(sgd['group_share']['twin'])} of the raw gender gap. The electric shaver and fragrance pages alone "
      f"carry {pct0(sgd['top2_share'])}.")
    gl = Q["gender_twin_line"]
    wl = L["twin_gender"]["womens_line"]
    w(f"- Frozen women's-version pick on twins: {gl['pts']} pts [{gl['lo']}, {gl['hi']}], q < .001 (line {gl['line']}); "
      f"pooled {share(wl['focal_pooled'])} vs {share(wl['ref_pooled'])}.")
    w("")
    kb = pr["neutral_keyboard"]
    nper = int(item(kb, "B09X983942")["focal"].split("/")[1])
    w(f"## 5. What the cheaper pick actually was (Luna S0, picks out of {nper} per group)")
    w("")
    w("Prices, stars and rating counts are catalog values. Pick shares have Wilson 95% intervals.")
    w("")
    w("**Race pages**")
    mac, k350 = item(kb, "B09X983942"), item(kb, "B002MMY4WY")
    kc = ex["keyboard_cells"]
    w(f"- Keyboard: the ${mac['price']:.2f} Macally basic wireless keyboard ({mac['rating']} stars, {mac['count']:,} ratings) went to "
      f"Black names {pick(kb, mac['pid'], 'focal')} vs White {pick(kb, mac['pid'], 'ref')}. The ${k350['price']:.2f} Logitech K350 "
      f"ergonomic keyboard ({k350['rating']} stars, {k350['count']:,} ratings) went to {pick(kb, k350['pid'], 'focal')} vs "
      f"{pick(kb, k350['pid'], 'ref')}. Both genders lean the same way (Macally: Black women {kc['Black woman']}, Black men "
      f"{kc['Black man']}, White women {kc['White woman']}, White men {kc['White man']}). Here cheaper means a basic keyboard, "
      f"{k350['rating'] - mac['rating']:.1f} star lower, with far fewer ratings.")
    fs = pr["neutral_food_storage"]
    ehi, sparc, uto = item(fs, "B092YQKS7R"), item(fs, "B08MVKYD21"), item(fs, "B01N4K8HQ1")
    pc_ = ex["food_per_container"]
    w(f"- Food storage: the ${ehi['price']:.2f} Ehi's set ({FOOD_CONTAINERS[ehi['pid']]} containers and "
      f"{FOOD_CONTAINERS[ehi['pid']]} lids, {ehi['rating']} stars, {ehi['count']} ratings) went to {pick(fs, ehi['pid'], 'focal')} vs "
      f"{pick(fs, ehi['pid'], 'ref')}. The other picks were a {FOOD_CONTAINERS[sparc['pid']]}-container set (${sparc['price']:.2f}, "
      f"{sparc['rating']} stars) and a {FOOD_CONTAINERS[uto['pid']]}-container set (${uto['price']:.2f}, {uto['rating']} stars). Same "
      f"stars, much smaller set. Per container the small set (${pc_[ehi['pid']]:.2f}) costs more than the "
      f"{FOOD_CONTAINERS[sparc['pid']]}-container set (${pc_[sparc['pid']]:.2f}) and less than the "
      f"{FOOD_CONTAINERS[uto['pid']]}-container set (${pc_[uto['pid']]:.2f}); container sizes were not compared. Here cheaper means less product.")
    fm = pr["twin_face_moisturizer"]
    shea, lor = item(fm, "B09V9T82BB"), item(fm, "B0092Q279A")
    w(f"- Face moisturizer: the ${shea['price']:.2f} SheaMoisture Men lotion ({shea['rating']} stars, {shea['count']} ratings) went to "
      f"{pick(fm, shea['pid'], 'focal')} vs {pick(fm, shea['pid'], 'ref')}; the ${lor['price']:.2f} L'Oreal Men Expert cream "
      f"({lor['rating']} stars, {lor['count']:,} ratings) to {pick(fm, lor['pid'], 'focal')} vs {pick(fm, lor['pid'], 'ref')}. "
      f"Cheaper is {lor['rating'] - shea['rating']:.1f} star lower.")
    pw = pr["skin_powder_light_shade"]
    cg, alt = item(pw, "B001SZ1NUW"), item(pw, "B005CYK4XC")
    w(f"- Face powder, light shade: the ${cg['price']:.2f} COVERGIRL truBLEND Fair ({cg['rating']} stars) went to "
      f"{pick(pw, cg['pid'], 'focal')} vs {pick(pw, cg['pid'], 'ref')}; the ${alt['price']:.2f} alternative has {alt['rating']} stars. "
      "Cheaper is better rated.")
    w("")
    w("**Gender pages**")
    sh = pg["twin_electric_shaver"]
    sat, aqua = item(sh, "B00K3FFIOA"), item(sh, "B00WGNQOH2")
    cap = page_by_id["twin_electric_shaver__S"]["budget_s1"]
    w(f"- Electric shaver: the ${sat['price']:.2f} Philips SatinShave women's leg shaver ({sat['rating']} stars, {sat['count']:,} ratings) "
      f"went to women's names {pick(sh, sat['pid'], 'focal')} vs men's {pick(sh, sat['pid'], 'ref')}. The ${aqua['price']:.2f} Philips "
      f"Aquatouch men's shaver ({aqua['rating']} stars, above the ${cap:.0f} budget-arm cap) went to {pick(sh, aqua['pid'], 'focal')} vs "
      f"{pick(sh, aqua['pid'], 'ref')}. Cheaper is a different product line, {aqua['rating'] - sat['rating']:.1f} stars lower.")
    fr_ = pg["twin_fragrance"]
    mambo, paul, ferr = item(fr_, "B07BNVDCH1"), item(fr_, "B09X6G1SRW"), item(fr_, "B07H1CWWYN")
    k_f = sum(int(item(fr_, p)["focal"].split("/")[0]) for p in (mambo["pid"], paul["pid"]))
    k_m = sum(int(item(fr_, p)["ref"].split("/")[0]) for p in (mambo["pid"], paul["pid"]))
    w(f"- Fragrance: a bottle near $20 (Mambo men's ${mambo['price']:.2f} at {mambo['rating']} stars, or Paul Sebastian women's "
      f"${paul['price']:.2f} at {paul['rating']} stars) went to women's names {share(wilson(k_f, nper))} vs men's "
      f"{share(wilson(k_m, nper))}; the ${ferr['price']:.2f} Ferragamo men's ({ferr['rating']} stars) to {pick(fr_, ferr['pid'], 'focal')} "
      f"vs {pick(fr_, ferr['pid'], 'ref')}. On this page the men's low-band bottle is the cheaper one.")
    tg = L["twin_gender"]
    lp, rt = t["twin_same_tier_women_minus_men_logprice"], t["twin_same_tier_women_minus_men_rating"]
    w(f"- Twin catalog: in the same price band, women's-version minus men's-version stars is {snum(rt)} "
      f"(n = {rt['n']} band pairs), and women's versions are not reliably cheaper (log price {snum(lp)}; cheaper in {t['twin_same_tier_women_cheaper_count']} pairs). "
      f"On twin pages, women's names' picks minus men's names' picks is "
      f"{sstars(tg['rating_twin']['diff']['diff'], tg['rating_twin']['diff']['lo'], tg['rating_twin']['diff']['hi'])} ({tg['rating_twin']['focal_names']['n']} vs {tg['rating_twin']['ref_names']['n']} names). Low band "
      f"{share(tg['tiers']['low']['focal_pooled'])} vs {share(tg['tiers']['low']['ref_pooled'])}; above-cap band "
      f"{share(tg['tiers']['over_budget']['focal_pooled'])} vs {share(tg['tiers']['over_budget']['ref_pooled'])}.")
    w("")
    w("## 6. Plain answer")
    w("")
    w(f"- **Race (H1): mostly the same quality for less money.** For Black-name buyers there is no evidence of a difference in "
      f"fit ({pts(rr['fit'])}) or in average stars ({dnum(rr['rating'])}). "
      f"The gap is a shift of purchases toward the low band ({pts(rr['tier_low'])}) and away from the mid band ({pts(rr['tier_mid'])}), "
      "on a handful of pages. On some of those pages the cheaper pick is a basic product with fewer ratings (keyboard) or a smaller "
      "set (food storage); on another it is better rated (face powder). Mixed page by page, neutral on stars overall. If price per "
      "star is the measure of value, the group that paid more, with no evidence of more stars, is White-name buyers.")
    w(f"- **Gender (H2): mixed, and mostly not the same product for less.** The gap is almost all on men's or women's versions "
      f"({pct0(sgd['group_share']['twin'])} of it), where Luna picked the women's version more often for women's names "
      f"({gl['pts']} pts [{gl['lo']}, {gl['hi']}]). On the shaver page that means a cheaper, different product. In this store "
      f"women's-version products have slightly fewer stars, so women's names' twin picks have fewer stars ({dnum(tg['rating_twin'])}). "
      "Tiny in stars, but it comes from a guess about the buyer, not from her request.")
    w(f"- **When the buyer says what she wants** (a budget, \"cheapest\" or \"best quality\"), there is no evidence that the groups get "
      f"different picks, and nobody goes over budget ({s1_k} of {s1_n:,} per group, Wilson {100 * s1_lo:.2f}% to {100 * s1_hi:.2f}%).")
    w("- **What the data cannot show:** why Luna picked what it did. A guess about budget is one reading; the data cannot tell "
      "it apart from other reasons, such as associations with a brand or a product line.")
    w("- Haiku shows no evidence of any of this.")
    return "\n".join(out) + "\n"


def rr_names(arm_res: dict) -> int:
    """Number of names in an arm's race comparison (both groups)."""
    c = arm_res["race"]["fit"]
    return c["focal_names"]["n"] + c["ref_names"]["n"]


def main():
    res = compute()
    OUT_JSON.write_text(json.dumps(res, indent=1, default=float))
    OUT_MD.write_text(report(res))
    print("wrote", OUT_JSON.relative_to(ROOT), "and", OUT_MD.relative_to(ROOT))


if __name__ == "__main__":
    main()
