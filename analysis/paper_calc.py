"""Numbers behind the paper figures and tables (paper/FIGURES_SPEC.md).

This module runs no new tests. Every test result comes from the frozen code in
analyze.py (PLAN.md). What is added here is only:

  - reading or rebuilding analyze.py's outputs (checks, confirm, explore),
  - descriptive group means with a t interval across names (the same rule as
    analyze.rate_by_group: average within name, then across names),
  - the dollar translation of a log-price gap (FIGURES_SPEC section 0),
  - catalog scale from data/pages.json, design counts from the catalog grids,
    and cost from the turn logs.

Pilot runs: the frozen confirm() admits a model to the confirmatory family only
when 95% of its main grid finished (PLAN 3), which a pilot never does. For a
pilot preview the entry rule is waived (see preview_confirm) and every output
is marked as pilot. Pilot outputs are never written to results/.
"""
from __future__ import annotations

import json
import math
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import analyze as A  # noqa: E402

LOGS = ROOT / "logs"
WATERMARK = "PILOT DATA, NOT RESULTS"
MAIN_PRESETS = {"main", "planted", "validity", "m1", "reduced", "olmo"}
MODEL_ORDER = ["haiku", "luna", "flashlite", "olmo"]
MODEL_LABEL = {"haiku": "Claude Haiku 5.5", "luna": "GPT-6 Luna", "flashlite": "Gemini 3.5 Flash-Lite",
               "olmo": "OLMo 3 7B", "synth_a": "Synthetic A", "synth_b": "Synthetic B"}
CORE_GROUPS = ["Black woman", "Black man", "White woman", "White man", "No name"]
REF_GROUP = {"H1": ("is_black", 0.0, "names associated with White buyers"),
             "H2": ("is_woman", 0.0, "names associated with men")}


def group_label(g: str) -> str:
    """'Black woman' -> 'Names associated with Black women'. Never labels people."""
    if g == "No name":
        return "No name on the account"
    race, gender = g.split()
    return f"Names associated with {race} {'women' if gender == 'woman' else 'men'}"


def model_sort(models) -> list[str]:
    return sorted(models, key=lambda m: MODEL_ORDER.index(m) if m in MODEL_ORDER else 99)


# ----------------------------------------------------------------------------- inputs

def resolve_runs(runs: list[str], logs: Path = LOGS) -> list[Path]:
    """Run names (pilot_haiku) or paths -> outcome CSV paths, in the given order.
    Order matters: analyze.load_outcomes keeps the last copy of an episode id,
    so a later run (vfollowup) replaces the same episode from an earlier one."""
    out = []
    for r in runs:
        p = Path(r)
        if not p.suffix:
            p = logs / f"{r}.outcomes.csv"
        if not p.exists():
            raise FileNotFoundError(p)
        out.append(p)
    return out


def run_manifest(csv_path: Path) -> dict:
    m = csv_path.with_name(csv_path.name.replace(".outcomes.csv", ".manifest.json"))
    return json.loads(m.read_text()) if m.exists() else {}


def run_status(csv_path: Path) -> dict:
    """Completeness of a scored run: rows vs the manifest's episode count."""
    man = run_manifest(csv_path)
    d = pd.read_csv(csv_path, usecols=["episode_id", "outcome"])
    fin = int((d["outcome"] != "incomplete").sum())
    return {"run": man.get("run", csv_path.stem), "preset": man.get("preset"), "model_key": man.get("model_key"),
            "episodes_expected": man.get("n_episodes"), "rows": int(len(d)), "finished": fin,
            "ask_protocol": man.get("ask_protocol", "original (one answered ask)")}


def is_pilot(statuses: list[dict]) -> bool:
    """Watermark unless every run is a main-run preset."""
    return any(s.get("preset") not in MAIN_PRESETS for s in statuses)


# ----------------------------------------------------------------------------- frozen analysis, read or rebuilt

@contextmanager
def _family_rule_waived():
    old = A.MAIN_GRID_EPISODES
    A.MAIN_GRID_EPISODES = 0
    try:
        yield
    finally:
        A.MAIN_GRID_EPISODES = old


def preview_confirm(df, mde_info, checks, confirm_models, n_perm):
    """analyze.confirm() unchanged, except that the 95% main-grid entry rule
    (PLAN 3) is waived so a pilot can be previewed. Pilot only."""
    present = [m for m in confirm_models if (df["model"] == m).any()]
    with _family_rule_waived():
        return A.confirm(df, mde_info, checks, present, n_perm=n_perm)


def run_checks(df, mde_info, shuffles):
    """Same content as analyze.cmd_checks, in memory."""
    models = model_sort(df["model"].unique())
    out = {"main_grid": A.main_grid_status(df, models), "planted": {}, "shuffled_null": {}, "arm_p": {},
           "balance": {}, "position": {}}
    for m in models:
        mr = mde_info.get("models", {}).get(m, {}).get("H1", {}).get("conservative", {}).get("mde_raw")
        out["planted"][m] = A.planted_check(df, m, mr)
        out["shuffled_null"][m] = {h: A.shuffled_null(df, m, h, n=shuffles) for h in A.HYPOTHESES}
        out["arm_p"][m] = A.arm_p_check(df, m)
        out["balance"][m] = A.balance_tables(df, m)
        out["position"][m] = A.position_effect(df, m)
    return out


def analysis_bundle(paths, df, mde_info, pilot, confirm_models, results_dir: Path, n_perm, shuffles):
    """Main data: read results/{checks,confirmatory,exploratory}.json written
    by analyze.py for these exact input files (refuses otherwise). Pilot: rebuild
    them in memory with the same functions, never writing to results/."""
    hashes = A.file_hashes([str(p) for p in paths])
    if not pilot:
        got = {}
        for name in ("checks", "confirmatory", "exploratory"):
            f = results_dir / f"{name}.json"
            if not f.exists():
                raise SystemExit(f"missing {f}: run analyze.py all on these outcome files first (PLAN 8, 12)")
            j = json.loads(f.read_text())
            if name != "exploratory" and j.get("inputs") != hashes:
                raise SystemExit(f"{f} was made from different input files; rerun analyze.py all")
            got[name] = j
        return {"source": "results/ (analyze.py)", **got}
    checks = run_checks(df, mde_info, shuffles)          # PLAN 8: checks before any group result
    conf = preview_confirm(df, mde_info, checks, confirm_models, n_perm)
    models = [m for m in model_sort(df["model"].unique()) if df[df["model"] == m]["arm"].isin(["S0", "S1", "V"]).any()]
    expl = A.explore(df, models)
    return {"source": "rebuilt in memory from pilot logs with analyze.py functions (family entry rule waived)",
            "checks": checks, "confirmatory": conf, "exploratory": expl}


def exploratory_model_estimates(df, models):
    """H1 to H4 estimates for models outside the confirmatory family (Gemini,
    OLMo), from the same name-level model. Shown as estimates with a 95% CI
    only: they are in no tested family, so no p-value is reported."""
    rows = []
    for m in models:
        for h, spec in A.HYPOTHESES.items():
            res, _ = A.run_hypothesis(df, m, h)
            if not np.isfinite(res.est):
                continue
            r = {"model": m, "hypothesis": h, "kind": spec["kind"], "label": spec["label"],
                 "est": res.est, "ci_lo": res.ci_lo, "ci_hi": res.ci_hi, "n_a": res.n_a, "n_b": res.n_b,
                 "status": "exploratory estimate, not tested"}
            if res.note:   # D5: every name has the same mean; an estimate, never a zero-width interval
                r.update(est=float("nan"), ci_lo=float("nan"), ci_hi=float("nan"), note=res.note,
                         status=f"exploratory: {res.note}")
            rows.append(r)
    return rows


# ----------------------------------------------------------------------------- descriptive helpers

def t_interval(values) -> dict:
    v = pd.Series(values, dtype=float).dropna()
    n = len(v)
    if n < 2:
        return {"est": float(v.mean()) if n else float("nan"), "lo": float("nan"), "hi": float("nan"), "names": n}
    se = v.std(ddof=1) / math.sqrt(n)
    half = stats.t.ppf(0.975, n - 1) * se
    return {"est": float(v.mean()), "lo": float(v.mean() - half), "hi": float(v.mean() + half), "names": n}


def _grp(nm: pd.DataFrame) -> pd.Series:
    return pd.Series(np.where(nm["tier"] == "baseline", "No name",
                              nm["race"].fillna("") + " " + nm["gender"].fillna("")), index=nm.index)


def dollars_by_group(df, model, arm="S0"):
    """FIGURES_SPEC Figure 2. Bought episodes in one arm, core names plus the
    no-name baseline. Per name: mean dollar price after removing task x arm x
    wording x order cell means (PLAN 5.1 step 2 on the dollar scale, grand mean
    added back), and the raw mean price. Group: mean over names, t 95% CI."""
    d = A.subset(df, model, [arm], tiers=("core", "baseline"))
    d = d[d["price"].notna() & (d["bought"] == 1)]
    if d.empty:
        return []
    nm = A.name_means(d, "price")
    raw = d.groupby("profile_id")["price"].mean().rename("raw")
    nm = nm.merge(raw, on="profile_id")
    nm["grp"] = _grp(nm)
    rows = []
    for g in CORE_GROUPS:
        sub = nm[nm["grp"] == g]
        if len(sub) < 2:
            continue
        adj, rw = t_interval(sub["mean"]), t_interval(sub["raw"])
        rows.append({"model": model, "arm": arm, "group": g, "label": group_label(g), "adj_usd": adj["est"],
                     "adj_lo": adj["lo"], "adj_hi": adj["hi"], "raw_usd": rw["est"], "raw_lo": rw["lo"],
                     "raw_hi": rw["hi"], "names": adj["names"], "episodes": int(d[d["profile_id"].isin(sub["profile_id"])].shape[0])})
    return rows


def reference_price(df, model, h) -> dict:
    """Average S0 price paid by the reference group (names associated with
    White buyers for H1, with men for H2) and by the focal group: core names,
    bought episodes, dollar price with task x wording x order cell means
    removed and the grand mean added back (PLAN 5.1 step 2 on the dollar
    scale, as in Figure 2), averaged within name, then over names. In a full
    grid every name sees every task and this equals the plain average; the
    raw averages are kept as *_raw."""
    col, val, label = REF_GROUP[h]
    d = A.subset(df, model, ["S0"])
    d = d[d["price"].notna() & (d["bought"] == 1)]
    if d.empty:
        return {"reference_group": label, "ref_usd": float("nan"), "ref_names": 0, "focal_usd": float("nan"),
                "ref_usd_raw": float("nan"), "focal_usd_raw": float("nan")}
    nm = A.name_means(d, "price")
    raw = d.groupby("profile_id")["price"].mean()
    ref, foc = nm[nm[col] == val], nm[nm[col] != val]
    return {"reference_group": label, "ref_usd": float(ref["mean"].mean()), "ref_names": int(len(ref)),
            "focal_usd": float(foc["mean"].mean()),
            "ref_usd_raw": float(raw[raw.index.isin(ref["profile_id"])].mean()),
            "focal_usd_raw": float(raw[raw.index.isin(foc["profile_id"])].mean())}


def dollar_translation(b: float, lo: float, hi: float, ref_usd: float) -> dict:
    """FIGURES_SPEC section 0: a log-price gap b means the focal group paid
    exp(b) - 1 more for the same request. Dollars per purchase = (exp(b) - 1) x
    the reference group's average price; per 1,000 purchases = 1,000 x that.
    The interval uses the same transform on the CI ends. Not a separate test."""
    f = lambda x: (math.exp(x) - 1) if x is not None and np.isfinite(x) else float("nan")  # noqa: E731
    pct = [100 * f(b), 100 * f(lo), 100 * f(hi)]
    usd = [f(b) * ref_usd, f(lo) * ref_usd, f(hi) * ref_usd]
    return {"gap_pct": pct[0], "ci_pct": pct[1:], "usd_per_purchase": usd[0], "usd_ci": usd[1:],
            "usd_per_1000": 1000 * usd[0], "usd_per_1000_ci": [1000 * usd[1], 1000 * usd[2]], "ref_usd": ref_usd}


def unify_focal(ref: dict, tr: dict) -> dict:
    """D12: one dollar definition. The focal group's average is the reference
    group's cell-adjusted average moved by the tested percent gap, so focal
    minus reference equals the dollars-per-purchase translation everywhere
    (Table 1, Figures 1, 3 and 4). The group mean of cell-adjusted dollar
    prices, which differs by a few cents because the test is on log price, is
    kept as focal_usd_cellmean (Figure A8)."""
    out = dict(ref)
    out["focal_usd_cellmean"] = ref["focal_usd"]
    out["focal_usd"] = ref["ref_usd"] + tr["usd_per_purchase"]
    return out


def rates(df, model, arm, y, tasks="all", extra=None, need_split=False):
    """analyze.rate_by_group, with the plain-language group label added."""
    rows = A.rate_by_group(df, model, arm, y, tasks=tasks, extra=extra, need_split=need_split)
    for r in rows:
        r["label"] = group_label(r["group"])
        r["y"] = y
    return rows


def episode_denominators(df, model, arm, y, tasks="all", extra=None):
    d = A.subset(df, model, [arm], tiers=("core", "baseline"), tasks=tasks, extra=extra)
    d = d[d[y].notna()]
    g = np.where(d["tier"] == "baseline", "No name", d["race"].fillna("") + " " + d["gender"].fillna(""))
    return d.groupby(g)[y].agg(["sum", "count"]).to_dict("index")


def shuffled_pvalues(df, model, h, n, seed=A.SEED) -> list[float]:
    """The p-values behind analyze.shuffled_null (same shuffles, same seed, same
    test), kept for the Figure 6D histogram. Its reject share equals the one in
    checks.json (tested)."""
    spec = A.HYPOTHESES[h]
    nm = A.name_means(A.hyp_data(df, model, h), spec["y"]).dropna(subset=["mean"]).reset_index(drop=True)
    if len(nm) < 6:
        return []
    rng = np.random.default_rng(seed)
    strata = nm[spec["other"]].to_numpy()
    lab = nm[spec["focal"]].to_numpy(float)
    ps = []
    for _ in range(n):
        perm = lab.copy()
        for sv in np.unique(strata):
            idx = np.where(strata == sv)[0]
            perm[idx] = rng.permutation(perm[idx])
        ps.append(A.name_level_test(nm.assign(**{spec["focal"]: perm}), spec["focal"], spec["other"]).p)
    return ps


def planted_per_name(df, model) -> pd.DataFrame:
    """Figure 6A: for each planted name, mean percent above the cheapest
    fitting price and mean dollars, in S0 and in PB on the same task, wording
    and order cells (descriptive view of PLAN 8.1a)."""
    pb = df[(df["model"] == model) & (df["arm"] == "PB") & df["finished"]]
    if pb.empty:
        return pd.DataFrame()
    s0 = df[(df["model"] == model) & (df["arm"] == "S0") & df["finished"] & df["profile_id"].isin(pb["profile_id"])]
    keys = ["profile_id", "task_id", "wording", "order"]
    both = pd.concat([s0.assign(cond="S0"), pb.assign(cond="PB")])
    both = both[both["logp"].notna()]
    cells = both.groupby(keys)["cond"].nunique()
    both = both.set_index(keys).loc[cells[cells == 2].index].reset_index()
    out = both.groupby(["profile_id", "cond"]).agg(logp=("logp", "mean"), usd=("price", "mean"),
                                                   n=("logp", "size")).reset_index()
    out["pct_over_cheapest"] = 100 * (np.exp(out["logp"]) - 1)
    return out


# ----------------------------------------------------------------------------- catalog, design, cost

def catalog_scale(pages_path: Path = A.DATA / "pages.json") -> dict:
    """FIGURES_SPEC section 0: scale of the specified pages (not outcomes)."""
    pages = [p for p in json.loads(pages_path.read_text())["pages"] if p["kind"] == "specified"]
    cheap = np.array([p["cheapest_fit_price_s0"] for p in pages], float)
    mid = np.array([next(i["price"] for i in p["items"] if i["slot"] == "fit_mid") for p in pages], float)
    return {"specified_pages": len(pages), "cheapest_fit_mean": float(cheap.mean()),
            "cheapest_fit_median": float(np.median(cheap)), "cheapest_fit_min": float(cheap.min()),
            "cheapest_fit_max": float(cheap.max()), "mid_fit_mean": float(mid.mean())}


def design_counts() -> dict:
    """Episodes per preset from the catalog grids (no API calls)."""
    sys.path.insert(0, str(ROOT / "src"))
    from harness.catalog import Catalog
    cat = Catalog()
    out = {}
    for preset in ["main", "planted", "validity", "m1", "reduced", "olmo", "pilot", "pilotsmall", "vfollowup"]:
        eps = cat.grid(preset)
        arms = pd.Series([e.arm for e in eps]).value_counts().to_dict()
        out[preset] = {"episodes": len(eps), "by_arm": arms, "profiles": len({e.profile_id for e in eps}),
                       "tasks": len({e.task_id for e in eps})}
    out["n_core"] = len(cat.core_profiles)
    out["n_baseline"] = len(cat.baseline_profiles)
    out["n_main_profiles"] = len(cat.main_profiles)
    out["n_tasks"] = len(cat.tasks)
    return out


def run_cost(csv_path: Path) -> dict:
    """Calls, tokens, estimated dollars and wall-clock time from a run's turn
    log (read only). Estimates from logged tokens; consoles are the record."""
    tp = csv_path.with_name(csv_path.name.replace(".outcomes.csv", ".turns.jsonl"))
    calls = tin = tout = 0
    usd = 0.0
    t0, t1 = None, None
    if not tp.exists():
        return {}
    with tp.open() as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            u = r.get("usage") or {}
            if r.get("status") == "ok" or u:
                calls += 1
            tin += int(u.get("input_tokens") or 0)
            tout += int(u.get("output_tokens") or 0)
            usd += float(r.get("billed_usd_est") or 0.0)
            for k in ("t_request", "t_response"):
                v = r.get(k)
                if v:
                    ts = pd.Timestamp(v)
                    t0 = ts if t0 is None or ts < t0 else t0
                    t1 = ts if t1 is None or ts > t1 else t1
    st = run_status(csv_path)
    hours = (t1 - t0).total_seconds() / 3600 if t0 is not None and t1 is not None else float("nan")
    return {**st, "calls": calls, "input_mtok": tin / 1e6, "output_mtok": tout / 1e6, "usd_est": usd,
            "usd_per_1000_episodes": 1000 * usd / max(st["finished"], 1), "wall_clock_hours": hours}
