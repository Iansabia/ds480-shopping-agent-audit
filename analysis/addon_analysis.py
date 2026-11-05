"""Exploratory add-ons A to D (PLAN.md Deviations D9 and D10), added after the main results were seen.

Ian approved the add-ons on 11/5. Nothing here touches the 8 confirmatory tests,
results/confirmatory.*, or the frozen exploratory family in results/exploratory.*.
All add-on tests form their own Benjamini-Hochberg family at 10% (D9), with the
same name-level machinery as PLAN 5.1: cell residualization (task x arm x wording
x order, plus hidden need in V), name means, OLS with HC2 errors and a t
reference, z(log name frequency) by the PLAN 5.3 rule. Rates also get pooled
95% Wilson intervals.

  A  gender-neutral names (preset neutral): women's-line pick on the 8 twin tasks,
     neutral names vs core men's names and vs core women's names, S0 (bought) and
     V (bought without asking, the agent's guess).
  B  stated line (preset stated): wrong-line rate by name gender x stated line;
     test: women's vs men's names within each stated line.
  C  MENA and South Asian names (presets arab and sasian) vs core White names:
     S0 price (H1 type), S0 identity-linked pick with the need stated (H3 type,
     S0 only because the add-ons have no S1), V identity-linked pick when the
     agent bought without asking (H4 type), V ask rate.
  D  Hispanic and Asian extended-tier names from the main runs, same outcomes.
     Their S0 price and V ask rate are already in the frozen exploratory family,
     so those are shown with the frozen q and are not retested; the H3 and H4
     type rows are new and enter the add-on family.

Black vs White rows in the race table repeat the confirmatory H1 and H4 and the
frozen "race: V ask rate" row (shown with their own adjusted p or q); the S0-only
H3-type row for Black names is descriptive (the confirmatory H3 uses S0 and S1).

A run that is only partly done (turns but no scored outcomes file) is scored in
memory and shown descriptively, never tested. Every caption and table note that
says which runs exist or are partial is built from the run status, not typed in.

    .venv/bin/python analysis/addon_analysis.py
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
sys.path.insert(0, str(ROOT / "src"))
import analyze as A  # noqa: E402
import figstyle as S  # noqa: E402
from h3_2x2 import wilson  # noqa: E402

LOGS = ROOT / "logs"
TAB = ROOT / "paper" / "tables"
FIG = ROOT / "paper" / "figures"
RES = ROOT / "results"
MAIN_RUNS = {"haiku": "main_haiku", "luna": "main_luna", "flashlite": "reduced_flashlite"}
ADDON_PRESETS = ["neutral", "stated", "arab", "sasian"]
MODELS = ["haiku", "luna", "flashlite"]
LABEL = {"haiku": "Claude Haiku 5.5", "luna": "GPT-6 Luna", "flashlite": "Gemini 3.5 Flash-Lite"}
RACES = ["White", "Black", "Hispanic", "Asian", "MENA", "South Asian"]
RACE_LABEL = {"White": "White", "Black": "Black", "Hispanic": "Hispanic", "Asian": "Asian",
              "MENA": "Arab or Middle Eastern (MENA)", "South Asian": "South Asian"}
# figures use one name per group in the title, rows and footer (FIGURES_SPEC: groups by position and label, in ink)
FIG_RACE = {r: lab.replace(" (MENA)", "") for r, lab in RACE_LABEL.items()}
STATED_OPP = {"STM": "women", "STW": "men"}
TAG = "Exploratory, added after the main results were seen."


# ----------------------------------------------------------------------------- data

def _addon_freq() -> pd.DataFrame:
    na = pd.read_csv(A.DATA / "names_addon.csv")
    return pd.DataFrame({"profile_id": na["name_id"],
                         "log_name_freq_addon": np.log1p(na["ssa_births_1950_2005"].astype(float)),
                         "ssa_female_share": na["ssa_female_share"], "full_name": na["full_name"]})


def _addon_exclusions() -> set[str]:
    f = A.DATA / "name_check_exclusions_addon.csv"
    return set(pd.read_csv(f)["profile_id"]) if f.exists() else set()


def load(logs: Path = LOGS) -> tuple[pd.DataFrame, dict]:
    """Main runs plus every add-on run that has a scored outcomes file. Add-on runs
    with turns but no outcomes file (stopped part way) are scored in memory and
    flagged partial. Returns the episode table and a run status dict."""
    from harness.score import score_run
    frames, status = [], {}
    tmp = Path(tempfile.mkdtemp(prefix="addon_partial_"))
    for model, run in MAIN_RUNS.items():
        p = logs / f"{run}.outcomes.csv"
        if p.exists():
            d = A.load_outcomes([str(p)])
            frames.append(d.assign(run=run, preset="main", partial=False))
    for preset in ADDON_PRESETS:
        for model in MODELS:
            run = f"{preset}_{model}"
            p, turns = logs / f"{run}.outcomes.csv", logs / f"{run}.turns.jsonl"
            partial = False
            if not p.exists():
                if not turns.exists():
                    continue
                rows = score_run(run, log_dir=logs, write=False)
                if not rows:
                    continue
                p = tmp / f"{run}.outcomes.csv"
                pd.DataFrame(rows).to_csv(p, index=False)
                partial = True
            d = A.load_outcomes([str(p)])
            status[run] = {"episodes": int(len(d)), "finished": int(d["finished"].sum()),
                           "bought": int((d["outcome"] == "bought").sum()), "partial": partial}
            frames.append(d.assign(run=run, preset=preset, partial=partial))
    df = pd.concat(frames, ignore_index=True)
    fq = _addon_freq()
    df = df.merge(fq[["profile_id", "log_name_freq_addon"]], on="profile_id", how="left")
    df["log_name_freq"] = df["log_name_freq"].fillna(df["log_name_freq_addon"])
    df = df.drop(columns=["log_name_freq_addon"])
    df = df[~df["profile_id"].isin(_addon_exclusions())].reset_index(drop=True)
    stated = df["arm"].map({"STM": "men", "STW": "women"})
    df["wrong_line"] = np.where(df["bought"] == 1, (df["gendered_line"] == df["arm"].map(STATED_OPP)).astype(float),
                                np.nan)
    df.loc[stated.isna(), "wrong_line"] = np.nan
    df["is_neutral"] = (df["race"] == "unmarked").astype(float)
    return df, status


# ----------------------------------------------------------------------------- helpers

def pooled(d: pd.DataFrame, y: str) -> dict:
    v = d[y].dropna()
    k, n = int(v.sum()), int(len(v))
    lo, hi = wilson(k, n)
    return {"k": k, "n": n, "rate": (k / n) if n else float("nan"), "wilson_lo": lo, "wilson_hi": hi,
            "names": int(d.loc[d[y].notna(), "profile_id"].nunique())}


def fmt_rate(r: dict, nd: int = 1) -> str:
    if not r or not r.get("n"):
        return "not run"
    return (f"{100 * r['rate']:.{nd}f}% [{100 * r['wilson_lo']:.{nd}f}, {100 * r['wilson_hi']:.{nd}f}] "
            f"({int(r['k']):,}/{int(r['n']):,})")


def fmt_p(p) -> str:
    if p is None or (isinstance(p, float) and not math.isfinite(p)):
        return "n/a"
    return "<.001" if p < 0.001 else f"{p:.3f}".lstrip("0")


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join("" if (isinstance(v, float) and math.isnan(v)) else str(v) for v in r) + " |")
    return "\n".join(out)


def _join(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def addon_models(status: dict, presets, full_only: bool = True) -> list[str]:
    """Models with a run for every preset given (finished and scored, unless full_only is False)."""
    return [m for m in MODELS if all(f"{p}_{m}" in status and (not full_only or not status[f"{p}_{m}"]["partial"])
                                     for p in presets)]


def partial_note(status: dict) -> str:
    """One sentence naming partial add-on runs from the run status, or "" when every run is complete."""
    parts = []
    for run, st in status.items():
        if st["partial"]:
            preset, model = run.rsplit("_", 1)
            parts.append(f"{LABEL[model]}'s {preset} run is partial ({st['episodes']:,} episodes, "
                         f"{st['bought']:,} bought), so its points are descriptive only")
    return ("; ".join(parts) + ".") if parts else ""


def race_groups_note(status: dict) -> str:
    ms = addon_models(status, ["arab", "sasian"])
    return f"{_join([LABEL[m] for m in ms])}" if ms else "no model"


class Family:
    """The add-on test family (BH at 10%), plus untestable rows (D5 rule)."""

    def __init__(self):
        self.tests: list[dict] = []
        self.untestable: list[dict] = []

    def add(self, part, model, name, nm, focal, other, kind, use_freq="auto") -> dict | None:
        nm = nm.dropna(subset=["mean"])
        if len(nm) < 4 or nm[focal].nunique() < 2:
            return None
        r = A.name_level_test(nm, focal, other, use_freq=use_freq)
        rec = {"part": part, "model": model, "test": name, "kind": kind, **r.to_dict()}
        (self.untestable if r.note == A.NO_VARIATION else self.tests).append(rec)
        return rec

    def finish(self):
        adj = A.bh([t["p"] for t in self.tests])
        for t, q in zip(self.tests, adj):
            t["q_bh"] = q
            t["discovery_q10"] = bool(q < A.BH_Q)
            if t["kind"] == "price":
                t["gap_pct"] = 100 * (math.exp(t["est"]) - 1)
                t["ci_pct"] = [100 * (math.exp(t["ci_lo"]) - 1), 100 * (math.exp(t["ci_hi"]) - 1)]
            else:
                t["gap_points"] = 100 * t["est"]
                t["ci_points"] = [100 * t["ci_lo"], 100 * t["ci_hi"]]
        for t in self.untestable:
            t["q_bh"], t["discovery_q10"] = None, False


def gap_text(t: dict | None) -> str:
    if t is None:
        return "not run"
    if t.get("note") == A.NO_VARIATION:
        return "no name variation"
    if t["kind"] == "price":
        return f"{t['gap_pct']:+.2f}% [{t['ci_pct'][0]:+.2f}, {t['ci_pct'][1]:+.2f}]"
    return f"{t['gap_points']:+.1f} pts [{t['ci_points'][0]:+.1f}, {t['ci_points'][1]:+.1f}]"


def named(df, model, arms, tasks=None, extra=None, tiers=("core", "extended", "addon")):
    d = df[(df["model"] == model) & df["arm"].isin(arms) & df["tier"].isin(tiers) & df["finished"]]
    if tasks == "twin":
        d = d[d["task_group"] == "twin"]
    elif tasks == "identity":
        d = d[d["identity_task"]]
    if extra is not None:
        d = d[extra(d)]
    return d


# ----------------------------------------------------------------------------- A: gender-neutral names

A_ARMS = [("S0", "S0, clear request (bought)", lambda d: d["bought"] == 1),
          ("V", "V, vague request, agent bought without asking", lambda d: (d["bought"] == 1) & (d["asked"] == 0))]
A_GROUPS = [("Men's names", lambda d: (d["tier"] == "core") & (d["gender"] == "man")),
            ("Gender-neutral names", lambda d: d["race"] == "unmarked"),
            ("Women's names", lambda d: (d["tier"] == "core") & (d["gender"] == "woman")),
            ("No-name accounts", lambda d: d["tier"] == "baseline")]
A_REFS = [("men's names", lambda d: (d["tier"] == "core") & (d["gender"] == "man")),
          ("women's names", lambda d: (d["tier"] == "core") & (d["gender"] == "woman"))]


def a_test_name(arm, ref):
    return f"A: {arm} twin women's-line pick, gender-neutral vs {ref}"


def part_a(df, fam: Family):
    rows, byname = [], []
    for model in MODELS:
        dm = df[(df["model"] == model) & (df["preset"].isin(["main", "neutral"])) & df["finished"]
                & (df["task_group"] == "twin")]
        if dm.empty:
            continue
        has_neutral = (dm["race"] == "unmarked").any()
        for arm, arm_lab, filt in A_ARMS:
            da = dm[(dm["arm"] == arm)]
            dsel = da[filt(da)]
            for g, gf in A_GROUPS:
                r = pooled(dsel[gf(dsel)], "womens_line_pick")
                ask = pooled(da[gf(da)], "asked") if arm == "V" else None
                rows.append({"model": model, "arm": arm, "arm_label": arm_lab, "group": g, **r,
                             "v_ask_rate": ask["rate"] if ask else None, "v_ask_k": ask["k"] if ask else None,
                             "v_ask_n": ask["n"] if ask else None})
            if not has_neutral:
                continue
            for ref, rf in A_REFS:
                sub = dsel[(dsel["race"] == "unmarked") | rf(dsel)]
                nm = A.name_means(sub, "womens_line_pick")
                nm["is_neutral"] = (nm["race"] == "unmarked").astype(float)
                fam.add("A", model, a_test_name(arm, ref), nm, "is_neutral", None, "rate")
            # per neutral name (raw pooled rates)
            for pid, g in dsel[dsel["race"] == "unmarked"].groupby("profile_id"):
                byname.append({"model": model, "arm": arm, "profile_id": pid, **pooled(g, "womens_line_pick")})
    tab = pd.DataFrame(rows)
    bn = pd.DataFrame(byname)
    if not bn.empty:
        fq = _addon_freq()
        bn = bn.merge(fq[["profile_id", "full_name", "ssa_female_share"]], on="profile_id", how="left")
    return tab, bn


def one_task_splits(df, fam: Family) -> list[dict]:
    """PLAN D10 caveat, from the data: for each flagged A test, the raw gender-neutral minus core-name gap on
    equal-weight twin task means and the one task that adds most to it, kept only when that task carries more
    than half of the raw gap. Descriptive; the tests are unchanged."""
    tests = {(t["model"], t["test"]): t for t in fam.tests}
    out = []
    for model in MODELS:
        dm = df[(df["model"] == model) & (df["preset"].isin(["main", "neutral"])) & df["finished"]
                & (df["task_group"] == "twin")]
        for arm, _, filt in A_ARMS:
            da = dm[dm["arm"] == arm]
            dsel = da[filt(da)]
            neu = dsel[dsel["race"] == "unmarked"].groupby("task_id")["womens_line_pick"].mean()
            for ref, rf in A_REFS:
                t = tests.get((model, a_test_name(arm, ref)))
                if t is None or not t["discovery_q10"]:
                    continue
                d = (neu - dsel[rf(dsel)].groupby("task_id")["womens_line_pick"].mean()).dropna()
                if d.empty:
                    continue
                part = d / len(d)          # each task's share of the equal-weight mean gap
                top, gap = part.abs().idxmax(), float(d.mean())
                if gap and np.sign(part[top]) == np.sign(gap) and abs(part[top]) > 0.5 * abs(gap):
                    out.append({"model": model, "arm": arm, "ref": ref, "gap_pts": 100 * gap, "task": top,
                                "task_pts": 100 * float(part[top])})
    return out


def neutral_surname_range() -> tuple[float, float, int] | None:
    """2010 Census Black share of the kept gender-neutral names' surnames (PLAN D9 limit): (low, high, n names)."""
    na = pd.read_csv(A.DATA / "names_addon.csv")
    s = na.loc[(na["race"] == "unmarked") & ~na["name_id"].isin(_addon_exclusions()), "surname_census_pctblack"]
    s = pd.to_numeric(s, errors="coerce").dropna()
    return (float(s.min()), float(s.max()), int(len(s))) if len(s) else None


def neutral_caveats(splits: list[dict]) -> list[str]:
    """The add-on A caveats as short clauses: separate sessions, surnames that lean Black, one-task gaps."""
    out = ["the gender-neutral names ran in separate sessions from the core names they are compared with, so a "
           "gap can include session drift"]
    sr = neutral_surname_range()
    if sr:
        out.append(f"their surnames lean Black (2010 Census Black share {sr[0]:.0f} to {sr[1]:.0f}% for the "
                   f"{sr[2]} kept names), so the set is not race-neutral")
    for s in splits:
        out.append(f"for {LABEL[s['model']]} in {s['arm']}, {abs(s['task_pts']):.1f} of the {abs(s['gap_pts']):.1f} "
                   f"points between gender-neutral and {s['ref']} (raw task means) come from one task, "
                   f"{s['task']}")
    return out


# ----------------------------------------------------------------------------- B: stated line

def part_b(df, fam: Family):
    rows = []
    for model in MODELS:
        dm = df[(df["model"] == model) & (df["preset"] == "stated")]
        if dm.empty:
            continue
        partial = bool(dm["partial"].any())
        for arm, lab in [("STM", "asked for the men's version"), ("STW", "asked for the women's version")]:
            da = dm[(dm["arm"] == arm) & dm["finished"]]
            for g in ["man", "woman"]:
                dg = da[da["gender"] == g]
                r = pooled(dg[dg["bought"] == 1], "wrong_line")
                npur = pooled(dg, "nonpurchase")
                # not bought splits into true no_purchase endings and invalid_product endings
                n_nopur = int((dg["outcome"] == "no_purchase").sum())
                n_invalid = int((dg["outcome"] == "invalid_product").sum())
                mismatch = (arm == "STM" and g == "woman") or (arm == "STW" and g == "man")
                rows.append({"model": model, "partial": partial, "stated": arm, "stated_label": lab,
                             "name_group": "women's names" if g == "woman" else "men's names", "mismatch": mismatch,
                             **r, "not_bought_k": npur["k"], "not_bought_n": npur["n"],
                             "not_bought_rate": npur["rate"], "no_purchase_k": n_nopur,
                             "invalid_product_k": n_invalid})
            if not partial:
                nm = A.name_means(da[da["bought"] == 1], "wrong_line")
                fam.add("B", model, f"B: {arm} wrong-line pick, women's vs men's names", nm, "is_woman", "is_black",
                        "rate")
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- C and D: race groups

def _frozen():
    conf = {(r["model"], r["hypothesis"]): r for r in json.loads((RES / "confirmatory.json").read_text())["rows"]}
    ex = {(t["model"], t["test"]): t for t in json.loads((RES / "exploratory.json").read_text())["tests"]}
    return conf, ex


RACE_OUT = {
    "price": dict(y="logp", arms=["S0"], tasks=None, extra=None, kind="price",
                  label="S0 price (H1 type)"),
    "h3": dict(y="identity_linked_product", arms=["S0"], tasks="identity", extra=None, kind="rate",
               label="S0 identity-linked pick, need stated (H3 type, S0 only)"),
    "h4": dict(y="identity_linked_product", arms=["V"], tasks="identity", extra=lambda d: d["asked"] == 0,
               kind="rate", label="V identity-linked pick, bought without asking (H4 type)"),
    "ask": dict(y="asked", arms=["V"], tasks=None, extra=None, kind="rate", label="V ask rate"),
}


def _disp(kind, est, lo, hi):
    """Gap in display units: percent for price, points for rates."""
    f = (lambda x: 100 * (math.exp(x) - 1)) if kind == "price" else (lambda x: 100 * x)
    return f(est), f(lo), f(hi)


def _disp_text(kind, e, lo, hi):
    return (f"{e:+.2f}% [{lo:+.2f}, {hi:+.2f}]" if kind == "price" else f"{e:+.1f} pts [{lo:+.1f}, {hi:+.1f}]")


def _frozen_ref(model, race, out, conf, ex):
    """Dict for a comparison already in a frozen family (source, display numbers, adjusted p or q), else None."""
    kind = RACE_OUT[out]["kind"]
    if race == "Black" and out in ("price", "h4"):
        h = {"price": "H1", "h4": "H4"}[out]
        if (model, h) in conf:
            r = conf[(model, h)]
            d = _disp(kind, r["r_est"], r["r_ci_lo"], r["r_ci_hi"])
            return {"source": f"confirmatory {h}", "adj": f"Holm p {fmt_p(r['p_holm'])}", "est": r["r_est"], "disp": d,
                    "flagged": bool(r["p_holm"] < A.ALPHA)}
    key = None
    if race == "Black" and out == "ask":
        key = "race: V ask rate"
    if race in ("Hispanic", "Asian"):
        key = {"price": f"extended: {race} vs White, S0 logp", "ask": f"extended: {race} vs White, V asked"}.get(out)
    if key and (model, key) in ex:
        t = ex[(model, key)]
        return {"source": "frozen exploratory", "adj": f"q {fmt_p(t['q_bh'])}", "est": t["est"],
                "disp": _disp(kind, t["est"], t["ci_lo"], t["ci_hi"]), "flagged": bool(t["q_bh"] < A.BH_Q)}
    return None


def part_cd(df, fam: Family):
    conf, ex = _frozen()
    rows, gaps = [], []
    for model in MODELS:
        dm = df[(df["model"] == model) & df["preset"].isin(["main", "arab", "sasian"])]
        if dm.empty:
            continue
        present = [r for r in RACES if (dm["race"] == r).any()]
        for out, spec in RACE_OUT.items():
            d = named(dm, model, spec["arms"], spec["tasks"], spec["extra"])
            d = d[d[spec["y"]].notna()]
            # one residualization over every named group the model has for this outcome (as in the frozen
            # extended-tier rows), then each group vs core White names
            nm_all = A.name_means(d, spec["y"])
            for race in present:
                if race == "White":
                    continue
                sub = nm_all[nm_all["race"].isin([race, "White"])].copy()
                sub["focal"] = (sub["race"] == race).astype(float)
                ref = _frozen_ref(model, race, out, conf, ex)
                base = {"model": model, "race": race, "outcome": out}
                if ref is not None:
                    gaps.append({**base, **ref, "gap": _disp_text(spec["kind"], *ref["disp"])})
                    continue
                if race == "Black" or model == "flashlite":
                    # descriptive only: Black S0-only H3 type (the confirmatory H3 uses S0 and S1), and every
                    # Gemini row that is not already in a frozen family (exploratory model)
                    r = A.name_level_test(sub, "focal", "is_woman")
                    if r.note == A.NO_VARIATION or not np.isfinite(r.se):
                        gaps.append({**base, "source": "descriptive", "gap": "no name variation", "adj": "not tested",
                                     "est": r.est, "disp": None})
                    else:
                        d3 = _disp(spec["kind"], r.est, r.ci_lo, r.ci_hi)
                        src = ("descriptive (confirmatory H3 uses S0 and S1)" if out == "h3" and model != "flashlite"
                               else "descriptive")
                        gaps.append({**base, "source": src, "gap": _disp_text(spec["kind"], *d3), "adj": "not tested",
                                     "est": r.est, "disp": d3})
                    continue
                part = "C" if race in ("MENA", "South Asian") else "D"
                t = fam.add(part, model, f"{part}: {race} vs White, {spec['label']}", sub, "focal", "is_woman",
                            spec["kind"])
                if t is not None:
                    gaps.append({**base, "source": "add-on family", "_t": t, "est": t["est"]})
            # descriptive per group
            for race in present:
                g = d[d["race"] == race]
                if out == "price":
                    bought = g[g["logp"].notna()]
                    rows.append({"model": model, "race": race, "outcome": out, "names": int(bought["profile_id"].nunique()),
                                 "n": int(len(bought)), "mean_log_ratio": float(bought["logp"].mean()),
                                 "mean_price_usd": float(pd.to_numeric(bought["price"], errors="coerce").mean())})
                else:
                    rows.append({"model": model, "race": race, "outcome": out, **pooled(g, spec["y"])})
        # H3 type override (opposite-need pick) and the gender-line effect, descriptive
        for race in present:
            d = named(dm, model, ["S0"], "identity", lambda x: x["bought"] == 1)
            rows.append({"model": model, "race": race, "outcome": "override",
                         **pooled(d[d["race"] == race], "opposite_need_pick")})
            d = named(dm, model, ["S0"], "twin", lambda x: x["bought"] == 1)
            for g in ["woman", "man"]:
                rows.append({"model": model, "race": race, "outcome": f"womens_line_{g}",
                             **pooled(d[(d["race"] == race) & (d["gender"] == g)], "womens_line_pick")})
    return pd.DataFrame(rows), gaps


# ----------------------------------------------------------------------------- tables

def build_tables(a_tab, a_byname, b_tab, cd_rows, gaps, fam: Family, status: dict) -> dict:
    TAB.mkdir(parents=True, exist_ok=True)
    tests = {(t["model"], t["test"]): t for t in fam.tests + fam.untestable}
    files = {}

    # ---- A
    a_tab.to_csv(TAB / "addon_A_neutral.csv", index=False)
    a_byname.to_csv(TAB / "addon_A_neutral_by_name.csv", index=False)
    lines = ["# Add-on A: women's-line pick when the name gives no gender cue", "",
             f"{TAG} Ian approved 11/5 (PLAN.md D9 and D10). The 8 twin tasks (a men's and a women's version of the "
             "same product on one page). Cell: share of purchases that were the women's version, pooled over names, "
             "95% Wilson interval, (women's picks/purchases). Men's and women's names are the 40 core names from the "
             "main runs (20 each); gender-neutral names are the 5 that passed the add-on name check; no-name accounts "
             "are the 4 baseline profiles. V uses purchases made without asking, so the pick is the agent's guess. "
             "Gemini 3.5 Flash-Lite has no neutral run. Gaps are from the name-level model (cell-adjusted name "
             "means, HC2), add-on BH family at 10%.", ""]
    for model in MODELS:
        t = a_tab[a_tab["model"] == model]
        if t.empty:
            continue
        lines += [f"## {LABEL[model]}", "", "| Names | S0, clear request | V, agent guessed | V ask rate (twin) |",
                  "|---|---|---|---|"]
        for g, _ in A_GROUPS:
            s0 = t[(t["arm"] == "S0") & (t["group"] == g)].iloc[0].to_dict()
            v = t[(t["arm"] == "V") & (t["group"] == g)].iloc[0].to_dict()
            ask = (f"{100 * v['v_ask_rate']:.1f}% ({int(v['v_ask_k']):,}/{int(v['v_ask_n']):,})"
                   if v.get("v_ask_n") else "not run")
            lines.append(f"| {g} | {fmt_rate(s0)} | {fmt_rate(v)} | {ask} |")
        lines.append("")
        for arm in ["S0", "V"]:
            for ref in ["men's names", "women's names"]:
                tt = tests.get((model, a_test_name(arm, ref)))
                if tt:
                    lines.append(f"- {arm}, gender-neutral minus {ref}: {gap_text(tt)}, q {fmt_p(tt.get('q_bh'))}")
        lines.append("")
    if not a_byname.empty:
        lines += ["## By gender-neutral name (pooled, Wilson)", "",
                  "| Model | Arm | Name | SSA female share | Women's-line pick |", "|---|---|---|---|---|"]
        for _, r in a_byname.sort_values(["model", "arm", "profile_id"]).iterrows():
            lines.append(f"| {LABEL[r['model']]} | {r['arm']} | {r['full_name']} ({r['profile_id']}) | "
                         f"{r['ssa_female_share']:.2f} | {fmt_rate(r.to_dict())} |")
        lines.append("")
    (TAB / "addon_A_neutral.md").write_text("\n".join(lines))
    files["A"] = ["addon_A_neutral.md", "addon_A_neutral.csv", "addon_A_neutral_by_name.csv"]

    # ---- B
    b_tab.to_csv(TAB / "addon_B_stated.csv", index=False)
    lines = ["# Add-on B: does the agent follow the stated line whatever the name?", "",
             f"{TAG} The 40 core names on the 8 twin tasks; the S0 request says \"I want the men's version.\" or "
             "\"I want the women's version.\" for every name, so name gender is crossed with the stated line. Cell: "
             "wrong-line rate = share of purchases that were the other gendered version, 95% Wilson interval "
             "(wrong/purchases); then the episodes that ended without a purchase, split into no purchase (the agent "
             "was still asking at its last turn) and invalid product (the agent tried to buy an id that is not on the "
             "page). **Bold** = mismatch cells (the stated line differs from the name's usual gender reading). A name-driven override would show up as a higher rate there.", ""]
    for model in MODELS:
        t = b_tab[b_tab["model"] == model]
        if t.empty:
            continue
        part = bool(t["partial"].any())
        st = status.get(f"stated_{model}", {})
        lines += [f"## {LABEL[model]}" + (f" (partial run: {st.get('episodes', 0):,} episodes, "
                                          f"{st.get('bought', 0):,} bought, descriptive only, not tested)"
                                          if part else ""), "",
                  "| Names | Asked for the men's version | Asked for the women's version |", "|---|---|---|"]
        for g in ["men's names", "women's names"]:
            cells = []
            for arm in ["STM", "STW"]:
                r = t[(t["stated"] == arm) & (t["name_group"] == g)].iloc[0].to_dict()
                txt = (f"{fmt_rate(r, 2)}; no purchase {r['no_purchase_k']}/{r['not_bought_n']}, "
                       f"invalid product {r['invalid_product_k']}/{r['not_bought_n']}")
                cells.append(f"**{txt}**" if r["mismatch"] else txt)
            lines.append(f"| {g.capitalize()} | {cells[0]} | {cells[1]} |")
        lines.append("")
        for arm, lab in [("STM", "asked for men's"), ("STW", "asked for women's")]:
            tt = tests.get((model, f"B: {arm} wrong-line pick, women's vs men's names"))
            if tt:
                lines.append(f"- {lab}, women's minus men's names: {gap_text(tt)}, q {fmt_p(tt.get('q_bh'))}")
        lines.append("")
    (TAB / "addon_B_stated.md").write_text("\n".join(lines))
    files["B"] = ["addon_B_stated.md", "addon_B_stated.csv"]

    # ---- C and D
    cd_rows.to_csv(TAB / "addon_C_race_groups.csv", index=False)
    gap_rows = []
    for g in gaps:
        if "_t" in g:
            t = g["_t"]
            d3 = (None if t.get("note") == A.NO_VARIATION else _disp(t["kind"], t["est"], t["ci_lo"], t["ci_hi"]))
            g["disp"] = d3
            gap_rows.append({"model": g["model"], "race": g["race"], "outcome": g["outcome"], "source": g["source"],
                             "gap": gap_text(t), "adjusted": f"q {fmt_p(t.get('q_bh'))}", "est": t["est"],
                             "p": t.get("p"), "q_bh": t.get("q_bh")})
        else:
            gap_rows.append({"model": g["model"], "race": g["race"], "outcome": g["outcome"], "source": g["source"],
                             "gap": g["gap"], "adjusted": g["adj"], "est": g["est"]})
        if g.get("disp"):
            gap_rows[-1].update({"gap_display": g["disp"][0], "lo_display": g["disp"][1], "hi_display": g["disp"][2]})
    gdf = pd.DataFrame(gap_rows)
    gdf.to_csv(TAB / "addon_C_race_gaps.csv", index=False)
    lines = ["# Add-ons C and D: six name groups side by side", "",
             f"{TAG} All 40 tasks, core White and Black names (20 each) and the Hispanic and Asian extended names "
             "(12 each) from the main runs; MENA (10) and South Asian (8: 5 women, 3 men) names from the add-on runs, "
             f"run on {race_groups_note(status)}. Gemini 3.5 Flash-Lite ran core names only. Rates: pooled share, "
             "95% Wilson interval "
             "(events/episodes). Price: mean log(price paid / cheapest fitting price) and raw mean price paid (no cell "
             "adjustment), bought episodes. Gap vs White: name-level model (cell-adjusted name means, HC2, gender as "
             "the other axis); price as percent, rates in points. The H3-type row is S0 only (the add-ons have no S1), so it is not "
             "the confirmatory H3. Source column: where the gap's adjusted p or q comes from. Frozen rows are "
             "shown with their frozen value and are not retested.", ""]
    for model in MODELS:
        t = cd_rows[cd_rows["model"] == model]
        if t.empty:
            continue
        present = [r for r in RACES if (t["race"] == r).any()]
        lines += [f"## {LABEL[model]}", "",
                  "| Names associated with | S0 price: mean log ratio, raw mean $ (no cell adjustment) | Override "
                  "(wrong product for the stated need), S0 | Identity-linked pick, V, agent guessed | V ask rate | "
                  "Women's-line pick, twin S0: women's names / men's names |", "|---|---|---|---|---|---|"]
        for race in present:
            tr = t[t["race"] == race]
            pr = tr[tr["outcome"] == "price"].iloc[0]
            row = (f"| {RACE_LABEL[race]} ({int(pr['names'])} names) | {pr['mean_log_ratio']:.3f}, "
                   f"${pr['mean_price_usd']:.2f} | ")
            for o in ["override", "h4", "ask"]:
                row += fmt_rate(tr[tr["outcome"] == o].iloc[0].to_dict()) + " | "
            w = tr[tr["outcome"] == "womens_line_woman"].iloc[0].to_dict()
            m = tr[tr["outcome"] == "womens_line_man"].iloc[0].to_dict()
            row += f"{fmt_rate(w)} / {fmt_rate(m)} |"
            lines.append(row)
        lines += ["", "Gaps vs names associated with White buyers:", "",
                  "| Names associated with | Outcome | Gap [95% CI] | Adjusted | Source |", "|---|---|---|---|---|"]
        for _, g in gdf[gdf["model"] == model].iterrows():
            lines.append(f"| {RACE_LABEL[g['race']]} | {RACE_OUT[g['outcome']]['label']} | {g['gap']} | "
                         f"{g['adjusted']} | {g['source']} |")
        lines.append("")
    (TAB / "addon_C_race_groups.md").write_text("\n".join(lines))
    files["C"] = ["addon_C_race_groups.md", "addon_C_race_groups.csv", "addon_C_race_gaps.csv"]

    # ---- the add-on family
    allt = pd.DataFrame(fam.tests + fam.untestable)
    keep = ["part", "model", "test", "kind", "est", "se", "df", "p", "ci_lo", "ci_hi", "n_a", "n_b", "mean_a",
            "mean_b", "freq_in_primary", "freq_corr", "welch_p", "q_bh", "discovery_q10", "gap_pct", "gap_points",
            "note"]
    allt = allt[[c for c in keep if c in allt.columns]]
    allt.to_csv(TAB / "addon_tests.csv", index=False)
    lines = ["# Add-on test family (Benjamini-Hochberg, 10%)", "",
             f"{TAG} {len(fam.tests)} tests in the family, separate from the frozen exploratory family. Name-level "
             "OLS on cell-adjusted name means, HC2 errors, t reference; z(log SSA name frequency) enters only when it "
             "correlates under 0.5 with the focal group (PLAN 5.3). Rows with no variation across names have no p "
             "and are left out (D5 rule).", "",
             "| Part | Model | Test | Gap [95% CI] | p | q | Names (focal/other) |", "|---|---|---|---|---|---|---|"]
    for t in sorted(fam.tests + fam.untestable, key=lambda t: (t["part"], MODELS.index(t["model"]), t["test"])):
        lines.append(f"| {t['part']} | {LABEL[t['model']]} | {t['test'].split(': ', 1)[1]} | {gap_text(t)} | "
                     f"{fmt_p(t.get('p'))} | {fmt_p(t.get('q_bh'))}{' (discovery)' if t.get('discovery_q10') else ''} | "
                     f"{t.get('n_a')}/{t.get('n_b')} |")
    (TAB / "addon_tests.md").write_text("\n".join(lines) + "\n")
    files["tests"] = ["addon_tests.md", "addon_tests.csv"]
    return files


# ----------------------------------------------------------------------------- figures

OFFS = {"haiku": -0.22, "luna": 0.0, "flashlite": 0.22}
PREREG = {"price": "H1", "h4": "H4"}      # outcomes whose Black vs White row is a confirmatory test
NUM_WORD = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
SMALL = f"font-size:{S.BASE - 4}px;color:{S.MUTED}"


def _hover(model, lab, r):
    return f"{LABEL[model]}<br>{lab}<br>{fmt_rate(r)}"


def _ink(open_):
    """Groups are shown by position and label only, so every marker is ink; open markers are muted (Figure 3)."""
    return S.MUTED if open_ else S.INK


def _key(models):
    """Footer marker key with each glyph and model name kept on one line (no-break spaces)."""
    k = S.marker_key(models)
    for m in models:
        g = S.GLYPH.get(S.symbol(m), "?")
        k = k.replace(f"{g} {S.label(m)}", f"{g} " + S.label(m).replace(" ", " "))
    return k


def _ticks(lo, hi, suffix=""):
    """At most 6 explicit ticks inside [lo, hi], with their text, so both engines print the same labels."""
    step = next(s for s in (0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50)
                if math.floor(hi / s + 1e-9) - math.ceil(lo / s - 1e-9) + 1 <= 6)
    tv = [round(k * step, 6) for k in range(math.ceil(lo / step - 1e-9), math.floor(hi / step + 1e-9) + 1)]
    return tv, [("−" if v < 0 else "") + f"{abs(v):g}{suffix}" for v in tv]


def fig_a6(a_tab, b_tab, status: dict, caveats=()):
    fig = make_subplots(rows=3, cols=1, vertical_spacing=0.13,
                        row_heights=[0.32, 0.32, 0.36])
    groups = [g for g, _ in A_GROUPS]
    rows_csv = []
    for i, (arm, title) in enumerate([("S0", "Clear request, either version is fine (S0)"),
                                      ("V", "Vague request, agent bought without asking (V)")], start=1):
        for model in MODELS:
            t = a_tab[(a_tab["model"] == model) & (a_tab["arm"] == arm)]
            for gi, g in enumerate(groups):
                r = t[t["group"] == g]
                if r.empty or not r.iloc[0]["n"]:
                    continue
                r = r.iloc[0].to_dict()
                open_ = model == "flashlite"
                S.dots(fig, [100 * r["rate"]], [gi + OFFS[model]], [100 * r["wilson_lo"]], [100 * r["wilson_hi"]],
                       _ink(open_), sym=S.symbol(model), htext=[_hover(model, g, r)], row=i, col=1, size=10,
                       open_=open_)
                rows_csv.append({"panel": arm, "model": model, "row": g, **{k: r[k] for k in
                                 ("k", "n", "rate", "wilson_lo", "wilson_hi", "names")}})
        fig.update_yaxes(tickvals=list(range(len(groups))), ticktext=groups, range=[len(groups) - 0.5, -0.5],
                         row=i, col=1)
        fig.update_xaxes(range=[0, 100], ticksuffix="%", dtick=20, title_text="Women's-line pick", row=i, col=1)
        _panel_title(fig, i, title)
    cells = [("STM", "men's names", "Asked for men's: men's names"),
             ("STM", "women's names", "Asked for men's: women's names"),
             ("STW", "men's names", "Asked for women's: men's names"),
             ("STW", "women's names", "Asked for women's: women's names")]
    mism = ({(a, g) for a, g, m in zip(b_tab["stated"], b_tab["name_group"], b_tab["mismatch"]) if m}
            if not b_tab.empty else set())
    xmax = 0
    for model in MODELS:
        t = b_tab[b_tab["model"] == model]
        if t.empty:
            continue
        part = bool(t["partial"].any())
        for ci, (arm, g, lab) in enumerate(cells):
            r = t[(t["stated"] == arm) & (t["name_group"] == g)].iloc[0].to_dict()
            xmax = max(xmax, 100 * r["wilson_hi"])
            S.dots(fig, [100 * r["rate"]], [ci + OFFS[model]], [100 * r["wilson_lo"]], [100 * r["wilson_hi"]],
                   _ink(part), sym=S.symbol(model), htext=[_hover(model, lab, r)], row=3, col=1, size=10, open_=part)
            rows_csv.append({"panel": "stated", "model": model, "row": lab, "partial": part,
                             **{k: r[k] for k in ("k", "n", "rate", "wilson_lo", "wilson_hi", "names")}})
    fig.update_yaxes(tickvals=list(range(4)), range=[3.5, -0.5], row=3, col=1,
                     ticktext=[lab + (f"<br><span style='{SMALL}'>mismatch</span>" if (a, g) in mism else "")
                               for a, g, lab in cells])
    fig.update_xaxes(range=[0, max(5, math.ceil(xmax + 0.5))], ticksuffix="%", dtick=1,
                     title_text="Wrong-line pick (the other version)", row=3, col=1)
    _panel_title(fig, 3, "Request states the version (men's or women's)")
    models_drawn = [m for m in MODELS if (a_tab["model"] == m).any() or (b_tab["model"] == m).any()]
    open_why = ((["Gemini 3.5 Flash-Lite ran no add-on and is exploratory"] if "flashlite" in models_drawn else [])
                + ([partial_note(status).rstrip(".")] if partial_note(status) else []))
    foot = (f"{TAG} Twin tasks (a men's and a women's version of one product on the same page), 4 runs per name, "
            "task and request. Dots: pooled share of purchases; bars: 95% Wilson intervals. Men's and women's names: "
            "40 core names, main runs. Gender-neutral: 5 names that passed the add-on name check. Mismatch: the "
            "request asks for the other gender's version (for example a woman's name asking for the men's version). "
            + (f"Caveats: {'; '.join(caveats)}. " if caveats else "")
            + (f"Open markers: estimate only ({'; '.join(open_why)}). " if open_why else "")
            + _key(models_drawn))
    S.layout(fig, "GPT-6 Luna puts gender-neutral names between men's and women's names; a stated version is followed",
             "Women's-line pick by name group (top two panels) and wrong-version pick when the request names the "
             "version (bottom).", False, 1050 + S.footer_margin(foot), bottom=S.footer_margin(foot), left=270, gap=40)
    S.footer(fig, foot)
    return fig, pd.DataFrame(rows_csv)


def _panel_title(fig, i, text, col=1):
    sp = fig.get_subplot(i, col)
    fig.add_annotation(text=f"<span style='font-weight:600'>{text}</span>", xref="paper", yref="paper",
                       x=sp.xaxis.domain[0], y=sp.yaxis.domain[1], xanchor="left", yanchor="bottom", yshift=6,
                       showarrow=False, align="left", font=dict(size=S.BASE - 1, color=S.INK))


# Figure A7: two gap panels on top (the tested outcomes), two share panels below
A7_PANELS = [((1, 1), "price", "Price paid, clear request (S0):<br>gap vs White names"),
             ((1, 2), "h3", "Identity-linked pick, need stated (S0):<br>gap vs White names"),
             ((2, 1), "h4", "Identity-linked pick when the<br>agent guessed (V)"),
             ((2, 2), "ask", "Agent asked a question<br>(V, vague request)")]
A7_GAP_AXIS = {"price": ("%", "Price gap (percent)"), "h3": ("", "Gap (percentage points)")}
A7_RATE_AXIS = {"h4": "Share of guessed purchases", "ask": "Share of runs"}
A7_WORD = {"price": "price", "h3": "identity-linked pick with the need stated",
           "h4": "identity-linked pick when guessing", "ask": "ask rate"}
A7_PANEL = {"price": "price", "h3": "need-stated", "h4": "guessed-pick", "ask": "ask"}
A7_LEFT, A7_RIGHT, A7_SIZE = 236, 30, 10


def _gap_disp(g):
    """Display numbers for a gap row (percent for price, points for rates), or None when it has no estimate."""
    if "_t" in g:
        t = g["_t"]
        return None if t.get("note") == A.NO_VARIATION else _disp(t["kind"], t["est"], t["ci_lo"], t["ci_hi"])
    return g.get("disp")


def _gap_flag(g):
    """(adjusted p or q text, flagged): Holm p under ALPHA for confirmatory rows, q under BH_Q for frozen and
    add-on rows; descriptive rows are never flagged."""
    if "_t" in g:
        return f"q {fmt_p(g['_t'].get('q_bh'))}", bool(g["_t"].get("discovery_q10"))
    return g.get("adj", ""), bool(g.get("flagged"))


def _race_names(cd_rows) -> dict:
    """Names per group (the price rows), the largest count over models."""
    pr = cd_rows[cd_rows["outcome"] == "price"]
    return {r: int(pr.loc[pr["race"] == r, "names"].max()) for r in RACES if (pr["race"] == r).any()}


def a7_title(gaps, present) -> str:
    """Title from the tests drawn in Figure A7: which gaps vs White names are flagged (pre-registered tests at
    Holm ALPHA, exploratory tests at q under BH_Q). It never states a null as an absence and never ranks estimates."""
    outs = [o for _, o, _ in A7_PANELS]
    hits = {}
    for g in gaps:
        adj, flag = _gap_flag(g)
        if flag and g["outcome"] in outs and g["race"] in present:
            tag = "pre-registered" if g["source"].startswith("confirmatory") else f"exploratory, {adj}"
            hits.setdefault((g["model"], g["race"]), []).append((outs.index(g["outcome"]), A7_WORD[g["outcome"]], tag))
    head = f"{NUM_WORD.get(len(present), len(present))} name groups"
    if not hits:
        return f"{head}: none of the gaps vs names associated with White buyers is flagged in these panels"

    def details(items):
        items = sorted(items)
        pre = [w for _, w, tag in items if tag == "pre-registered"]
        return "; ".join(([f"{_join(pre)}, pre-registered"] if pre else [])
                         + [f"{w}, {tag}" for _, w, tag in items if tag != "pre-registered"])
    if len(hits) == 1:
        (m, r), items = next(iter(hits.items()))
        return (f"{head}: only names associated with {FIG_RACE[r]} buyers on {LABEL[m]} show "
                f"{'flagged gaps' if len(items) > 1 else 'a flagged gap'} vs White names ({details(items)})")
    return (f"{head}: flagged gaps vs White names appear only for "
            + "; ".join(f"{FIG_RACE[r]} names on {LABEL[m]} ({details(it)})" for (m, r), it in hits.items()))


def _a7_ylab(race, n, out):
    tag = ("reference" if race == "White" else
           f"pre-registered test ({PREREG[out]})" if race == "Black" and out in PREREG else "exploratory")
    return (f"Names associated with<br>{FIG_RACE[race]} buyers<br><span style='{SMALL}'>"
            + (f"{n} names, " if n else "") + f"{tag}</span>")


def fig_a7(cd_rows, gaps, status: dict):
    fig = make_subplots(rows=2, cols=2, vertical_spacing=0.18, horizontal_spacing=0.1, shared_yaxes=True)
    present = [r for r in RACES if (cd_rows["race"] == r).any()]
    models_drawn = [m for m in MODELS if (cd_rows["model"] == m).any()]
    nnames = _race_names(cd_rows)
    rows_csv, drawn, no_est = [], [], []
    for (r_, c_), out, title in A7_PANELS:
        xr, yr = S._refs(fig, r_, c_)
        if out in PREREG and "Black" in present:
            # shaded row: the pre-registered Black vs White test in this panel (as in Figure 3)
            yb = present.index("Black")
            fig.add_shape(type="rect", xref=f"{xr} domain", yref=yr, x0=0, x1=1, y0=yb - 0.5, y1=yb + 0.5,
                          fillcolor=S.BAND, line=dict(width=0), layer="below")
        if out in A7_GAP_AXIS:
            # gap vs White names: the outcome that was tested (H1 type price, H3 type pick with the need stated)
            for g in gaps:
                if g["outcome"] != out or g["race"] not in present:
                    continue
                model, race, d3 = g["model"], g["race"], _gap_disp(g)
                if not d3:
                    no_est.append((out, model, race))
                    continue
                est, lo, hi = d3
                adj, _ = _gap_flag(g)
                open_ = model == "flashlite"
                S.dots(fig, [est], [present.index(race) + OFFS[model]], [lo], [hi], _ink(open_),
                       sym=S.symbol(model), row=r_, col=c_, size=A7_SIZE, open_=open_,
                       htext=[f"{LABEL[model]}<br>{FIG_RACE[race]} names minus White names: "
                              f"{_disp_text(RACE_OUT[out]['kind'], est, lo, hi)}<br>{g['source']}, {adj}"])
                rows_csv.append({"panel": f"{out} gap vs White ({'%' if out == 'price' else 'points'})",
                                 "model": model, "race": race, "est": est, "lo": lo, "hi": hi, "source": g["source"],
                                 "adjusted": adj})
                drawn.append((out, (r_, c_), race, est, lo, hi))
            S.vline(fig, 0, r_, c_, layer="below", color=S.AXIS, width=1.2)
            if "White" in present:
                fig.add_annotation(x=0, y=present.index("White"), xref=xr, yref=yr, text="reference",
                                   showarrow=False, xanchor="center", yanchor="middle", bgcolor=S.SURFACE,
                                   font=dict(size=S.BASE - 4, color=S.MUTED))
        else:
            for model in MODELS:
                t = cd_rows[(cd_rows["model"] == model) & (cd_rows["outcome"] == out)]
                for _, rr in t.iterrows():
                    if not rr["n"] or rr["race"] not in present:
                        continue
                    r = rr.to_dict()
                    est, lo, hi = 100 * r["rate"], 100 * r["wilson_lo"], 100 * r["wilson_hi"]
                    open_ = model == "flashlite"
                    S.dots(fig, [est], [present.index(r["race"]) + OFFS[model]], [lo], [hi], _ink(open_),
                           sym=S.symbol(model), htext=[_hover(model, f"Names associated with {FIG_RACE[r['race']]} "
                                                              "buyers", r)],
                           row=r_, col=c_, size=A7_SIZE, open_=open_)
                    rows_csv.append({"panel": out, "model": model, "race": r["race"], "est": est, "lo": lo,
                                     "hi": hi, "k": r["k"], "n": r["n"]})
                    drawn.append((out, (r_, c_), r["race"], est, lo, hi))
        _panel_title(fig, r_, title, c_)
    # x axes: explicit ticks, so both engines print the same labels
    for (r_, c_), out, _ in A7_PANELS:
        if out in A7_GAP_AXIS:
            vals = [v for o, _, _, _, lo, hi in drawn if o == out for v in (lo, hi)] + [0.0]
            pad = 0.06 * (max(vals) - min(vals))
            lo, hi = min(vals) - pad, max(vals) + pad
            tv, tt = _ticks(lo, hi, A7_GAP_AXIS[out][0])
            fig.update_xaxes(range=[lo, hi], tickvals=tv, ticktext=tt, title_text=A7_GAP_AXIS[out][1], row=r_, col=c_)
        else:
            tv, tt = _ticks(0, 100, "%")
            fig.update_xaxes(range=[0, 100], tickvals=tv, ticktext=tt, title_text=A7_RATE_AXIS[out], row=r_, col=c_)
    for r_ in (1, 2):
        left = A7_PANELS[2 * (r_ - 1)][1]
        for c_ in (1, 2):
            fig.update_yaxes(tickvals=list(range(len(present))), range=[len(present) - 0.5, -0.5],
                             ticktext=[_a7_ylab(r, nnames.get(r), left) for r in present],
                             showticklabels=(c_ == 1), row=r_, col=c_)
    # intervals shorter than the marker radius (plus its ring) on both sides are hidden behind the marker
    pw = S.WIDTH - A7_LEFT - A7_RIGHT
    hidden = {}
    for out, (r_, c_), race, est, lo, hi in drawn:
        ax = fig.get_subplot(r_, c_).xaxis
        px = pw * (ax.domain[1] - ax.domain[0]) / (ax.range[1] - ax.range[0])
        if max(est - lo, hi - est) * px < A7_SIZE / 2 + 1 and race not in hidden.get(out, []):
            hidden.setdefault(out, []).append(race)
    hid = "; ".join(f"{A7_PANEL[o]} panel: {_join([FIG_RACE[r] for r in present if r in rs])} names"
                    for o, rs in hidden.items())
    noe = "; ".join(f"{LABEL[m]}, {FIG_RACE[r]} names, {A7_PANEL[o]} panel" for o, m, r in no_est)
    a_, q_ = f"{A.ALPHA:.2f}".lstrip("0"), f"{A.BH_Q:.2f}".lstrip("0")
    foot = (f"{TAG} All 40 tasks, 4 runs per name, task and request. Hispanic and Asian: extended-tier names, main "
            f"runs; Arab or Middle Eastern and South Asian: add-on runs ({race_groups_note(status)}). Top: name-level "
            "gap vs names associated with White buyers (cell-adjusted name means, HC2), 95% CI; the need-stated pick "
            "is S0 only, so it is not the confirmatory H3. Bottom: pooled shares, 95% Wilson intervals; "
            "identity-linked = coily 4C hair or deep shade product, on hair and skin tasks. Shaded: the pre-registered Black vs White "
            f"tests (H1 for price, H4 for the pick when guessing). Flagged in the title: Holm p under {a_} for "
            f"pre-registered tests, q under {q_} for exploratory ones. "
            + (f"Intervals narrower than the marker are hidden behind it ({hid}). " if hid else "")
            + (f"No point is drawn where the name means do not vary ({noe}). " if noe else "")
            + "Open diamond: Gemini 3.5 Flash-Lite (core names only, estimate only). " + _key(models_drawn))
    sub = (_join([f"{LABEL[m]} ({cd_rows.loc[cd_rows['model'] == m, 'race'].nunique()} groups)" for m in models_drawn])
           + ". Top: gap vs names associated with White buyers; bottom: share of purchases or runs.")
    S.layout(fig, a7_title(gaps, present), sub, False, 1060 + S.footer_margin(foot), bottom=S.footer_margin(foot),
             left=A7_LEFT, right=A7_RIGHT, gap=58)
    S.footer(fig, foot)
    return fig, pd.DataFrame(rows_csv)


# ----------------------------------------------------------------------------- captions

def caption_a6(a_tab, b_tab, fam, status: dict, caveats=()):
    def rate(model, arm, g):
        t = a_tab[(a_tab["model"] == model) & (a_tab["arm"] == arm) & (a_tab["group"] == g)]
        return f"{100 * t.iloc[0]['rate']:.0f}%" if not t.empty and t.iloc[0]["n"] else "n/a"
    parts = []
    for model in ["haiku", "luna"]:
        if not (a_tab["model"] == model).any():
            continue
        parts.append(f"{LABEL[model]}: men's names {rate(model, 'S0', 'Men' + chr(39) + 's names')}, gender-neutral "
                     f"{rate(model, 'S0', 'Gender-neutral names')}, women's names "
                     f"{rate(model, 'S0', 'Women' + chr(39) + 's names')} in S0; "
                     f"{rate(model, 'V', 'Men' + chr(39) + 's names')}, {rate(model, 'V', 'Gender-neutral names')} "
                     f"and {rate(model, 'V', 'Women' + chr(39) + 's names')} in V")
    return ("Figure A6. Which gendered version the agents pick when the name gives no gender cue, and whether a "
            "stated version overrides the name. " + TAG + " Twin tasks (8 products, each sold in a men's and a "
            "women's version on the same page). Top two panels: share of purchases that were the women's version, "
            "for the 40 core names split by gender, 5 gender-neutral names (SSA female share 0.41 to 0.71) that "
            "passed the add-on name check, and the 4 no-name accounts; S0 is the clear request that says either "
            "version is fine, V is the vague request, counting only purchases made without asking. Bottom panel: "
            "the same 40 core names with a request that names the version; wrong-version rate by name gender and "
            "stated version (mismatch: the request asks for the other gender's version). Dots: pooled share; bars: "
            "95% Wilson intervals. Name-level tests are in paper/tables/addon_tests.md (Benjamini-Hochberg at 10% "
            "within the add-on family). " + "; ".join(parts) + "."
            + (f" Caveats: {'; '.join(caveats)}." if caveats else "")
            + (" " + partial_note(status) if partial_note(status) else ""))


def caption_a7(status: dict, cd_rows=None):
    n = _race_names(cd_rows) if cd_rows is not None else {}

    def pair(a, b, what):
        na, nb = n.get(a), n.get(b)
        if not na or not nb:
            return f"{a} and {b}: {what}"
        return f"{a} and {b}: {na} {what} each" if na == nb else f"{a} and {b}: {na} and {nb} {what}"
    groups = NUM_WORD.get(len(n), "Six") if n else "Six"
    a_, q_ = f"{A.ALPHA:.2f}".lstrip("0"), f"{A.BH_Q:.2f}".lstrip("0")
    return (f"Figure A7. {groups} name groups side by side. " + TAG + " Top: gap vs names associated with White "
            "buyers for the same clear request (name-level model on cell-adjusted name means, HC2, 95% CI), for "
            "price paid (percent) and for the identity-linked pick when the buyer stated the need (percentage "
            "points; the H3-type outcome that was tested, S0 only, so not the confirmatory H3). Bottom: "
            "identity-linked pick when the agent bought without asking on a vague hair or skin request, and ask rate "
            "on vague requests (pooled shares, 95% Wilson intervals). Shaded rows: the pre-registered Black vs White "
            "tests (H1 for price, H4 for the pick when guessing); every other comparison is exploratory. The title "
            f"calls a gap flagged when its Holm p is under {a_} (pre-registered tests) or its q is under {q_} "
            f"(exploratory tests). {pair('White', 'Black', 'core names')}; "
            f"{pair('Hispanic', 'Asian', 'extended-tier names')}, main runs; Arab or Middle Eastern (Moroccan names "
            "from Ghekiere et al. 2025; weak rater validation, so our own name check is the main support) and South "
            "Asian (Indian and Pakistani names from Table 2 of Oreopoulos 2009): "
            + (f"{n['MENA']} and {n['South Asian']} names, " if n.get("MENA") and n.get("South Asian") else "")
            + f"{race_groups_note(status)}. Gemini 3.5 Flash-Lite ran core names only and is shown as an estimate "
            "only. Exact numbers and adjusted p or q values are in paper/tables/addon_C_race_groups.md.")


def write_caption_entries(entries: dict[str, tuple[str, str]]):
    p = FIG / "CAPTIONS.md"
    text = p.read_text() if p.exists() else "# Figure captions\n\n"
    for key, (stem, cap) in entries.items():
        entry = f"## {key}\n\n`{stem}.png` (interactive: `{stem}.html`)\n\n{cap}\n"
        lines = text.split("\n")
        start = next((i for i, ln in enumerate(lines) if ln.strip() == f"## {key}"), None)
        if start is not None:
            end = next((j for j in range(start + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
            lines[start:end] = entry.split("\n")
            text = "\n".join(lines)
        else:
            anchor = text.find("\n## figA3 (not drawn)")
            text = (text[:anchor + 1] + entry + "\n" + text[anchor + 1:]) if anchor >= 0 else \
                text.rstrip("\n") + "\n\n" + entry
    p.write_text(text)
    return p


# ----------------------------------------------------------------------------- main

def run(write_figures: bool = True) -> dict:
    df, status = load()
    fam = Family()
    a_tab, a_byname = part_a(df, fam)
    b_tab = part_b(df, fam)
    cd_rows, gaps = part_cd(df, fam)
    fam.finish()
    files = build_tables(a_tab, a_byname, b_tab, cd_rows, gaps, fam, status)
    out = {"runs": status, "n_tests": len(fam.tests), "n_untestable": len(fam.untestable), "bh_q": A.BH_Q,
           "tests": fam.tests, "untestable": fam.untestable, "tables": files,
           "note": TAG + " Separate BH family; no frozen output changed."}
    if write_figures:
        made: list = []
        caveats = neutral_caveats(one_task_splits(df, fam))
        f6, d6 = fig_a6(a_tab, b_tab, status, caveats)
        S.save(f6, FIG, "figA6_gender_line", False, made)
        S.save(f6, FIG, "figA6_gender_line", False, made, engine="matplotlib")
        d6.to_csv(FIG / "figA6_gender_line.csv", index=False)
        f7, d7 = fig_a7(cd_rows, gaps, status)
        S.save(f7, FIG, "figA7_race_groups", False, made)
        S.save(f7, FIG, "figA7_race_groups", False, made, engine="matplotlib")
        d7.to_csv(FIG / "figA7_race_groups.csv", index=False)
        write_caption_entries({"figA6": ("figA6_gender_line", caption_a6(a_tab, b_tab, fam, status, caveats)),
                               "figA7": ("figA7_race_groups", caption_a7(status, cd_rows))})
        out["figures"] = made
    (RES / "addon_exploratory.json").write_text(json.dumps(out, indent=1, default=A._json_default))
    return out


if __name__ == "__main__":
    o = run()
    print(json.dumps({"runs": o["runs"], "n_tests": o["n_tests"], "n_untestable": o["n_untestable"],
                      "discoveries": [(t["model"], t["test"], round(t["q_bh"], 4)) for t in o["tests"]
                                      if t["discovery_q10"]]}, indent=1))
