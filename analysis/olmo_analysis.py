"""OLMo 3 7B: a separate exploratory block and the training-data link (PLAN.md D4 and D14).

OLMo's run (`reduced_olmo`, 7,040 episodes, S0 and V) finished after the main
results were seen. PLAN 9 says OLMo joins the exploratory family "when
present", but adding it now would change a family whose results were already
read. So, as with the D9/D10 add-ons, OLMo gets its own block and its own
Benjamini-Hochberg family at 10%, written to NEW files:

    results/olmo_exploratory.json
    paper/tables/olmo_exploratory.md and .csv

Nothing here touches results/confirmatory.*, results/exploratory.*,
results/checks.json or results/addon_exploratory.json.

Block (same name-level machinery as PLAN 5.1: cell residualization, name
means, OLS with HC2 errors and a t reference, z(log name frequency) by the
PLAN 5.3 rule with the same SSA source as the main analysis):

  h1_price      S0 log price, names associated with Black vs White buyers (H1 type)
  h2_price      S0 log price, names associated with women vs men (H2 type)
  v_ask_race    V ask rate, Black vs White
  v_ask_gender  V ask rate, women vs men
  h4_pick       V hair and skin tasks, bought without asking: identity-linked pick, Black vs White (H4 type)
  twin_s0       twin tasks, S0: women's-line pick, women vs men
  twin_v        twin tasks, V, bought without asking: women's-line pick, women vs men

A run that is not finished (fewer finished episodes than its manifest lists)
gets estimates and name-level 95% CIs only, labeled partial, and no test, as
for partial add-on runs (D10): a partial run is not a balanced slice of the
grid.

Training-data link (Figure A3, design 5.11): per core name, the log count of
" <first name>" in OLMo 3 pretraining data (the shared base, through Ai2's
32B Instruct infini-gram index; data/olmo_name_counts.csv) vs that name's S0
price relative to the average name; Spearman rho and p over the core names.
Sensitivities: without the names flagged as common words
(word_ambiguity_flag), and on the OLMo 2 pretraining index. Exploratory,
traced, correlation only; not in any BH family (PLAN 9).

    .venv/bin/python analysis/olmo_analysis.py              # after `run_agents.py score --run reduced_olmo`
    .venv/bin/python analysis/olmo_analysis.py --logs <dir> --results <dir> --tabdir <dir>
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import analyze as A  # noqa: E402

LOGS = ROOT / "logs"
TAB = ROOT / "paper" / "tables"
RUN = "reduced_olmo"
MODEL = "olmo"
COUNTS = A.DATA / "olmo_name_counts.csv"
INDEX_PRIMARY = "olmo-3-0625-32b-instruct"
INDEX_OLMO2 = "v4_olmo-mix-1124_llama"
INDEX_WORDS = ("OLMo 3 pretraining data (shared base, via Ai2's 32B Instruct index)")
INDEX_OLMO2_WORDS = "OLMo 2 pretraining mix"
TAG = "Exploratory, added after the main results were seen (OLMo's run finished later)."
BH_Q = 0.10

# key, label, outcome, arms, tasks, row filter, focal, other, kind
TESTS = [
    ("h1_price", "S0 price, names associated with Black vs White buyers (H1 type)", "logp", ["S0"], "all", None,
     "is_black", "is_woman", "price"),
    ("h2_price", "S0 price, names associated with women vs men (H2 type)", "logp", ["S0"], "all", None,
     "is_woman", "is_black", "price"),
    ("v_ask_race", "V ask rate, names associated with Black vs White buyers", "asked", ["V"], "all", None,
     "is_black", "is_woman", "rate"),
    ("v_ask_gender", "V ask rate, names associated with women vs men", "asked", ["V"], "all", None,
     "is_woman", "is_black", "rate"),
    ("h4_pick", "V hair and skin, bought without asking: identity-linked pick, Black vs White (H4 type)",
     "identity_linked_product", ["V"], "identity", lambda d: d["asked"] == 0, "is_black", "is_woman", "rate"),
    ("twin_s0", "Twin tasks, S0: women's-line pick, names associated with women vs men", "womens_line_pick",
     ["S0"], "twin", None, "is_woman", "is_black", "rate"),
    ("twin_v", "Twin tasks, V, bought without asking: women's-line pick, women vs men", "womens_line_pick",
     ["V"], "twin", lambda d: d["asked"] == 0, "is_woman", "is_black", "rate"),
]


# ----------------------------------------------------------------------------- run status

def run_status(csv_path: Path) -> dict:
    """Finished episodes vs the manifest's count. complete = every listed episode finished."""
    csv_path = Path(csv_path)
    man_p = csv_path.with_name(csv_path.name.replace(".outcomes.csv", ".manifest.json"))
    man = json.loads(man_p.read_text()) if man_p.exists() else {}
    d = pd.read_csv(csv_path, usecols=["episode_id", "outcome"])
    fin = int((d["outcome"] != "incomplete").sum())
    exp = man.get("n_episodes")
    return {"run": man.get("run", csv_path.name.split(".")[0]), "preset": man.get("preset"),
            "model_key": man.get("model_key"), "episodes_expected": exp, "rows": int(len(d)), "finished": fin,
            "complete": bool(exp) and fin >= int(exp)}


def status_text(st: dict | None) -> str:
    if not st:
        return "OLMo 3 7B: not scored yet"
    exp = st.get("episodes_expected")
    if st.get("complete"):
        return f"OLMo 3 7B: {st['finished']:,} of {exp:,} episodes finished"
    return (f"OLMo 3 7B: partial run, {st['finished']:,} of {exp:,} episodes finished; estimates only, not tested"
            if exp else f"OLMo 3 7B: {st['finished']:,} episodes finished (no manifest count); estimates only")


# ----------------------------------------------------------------------------- the block

def _s1(v) -> str:
    """Signed, one decimal, never '-0.0'."""
    return f"{0.0 if abs(v) < 0.05 else v:+.1f}"


def _display(kind, v):
    if v is None or not np.isfinite(v):
        return float("nan")
    return 100 * (math.exp(v) - 1) if kind == "price" else 100 * v


def block(df: pd.DataFrame, status: dict | None, test: bool | None = None) -> dict:
    """Estimates (and, for a finished run, tests with their own BH family) for the OLMo block.
    test: None = test only when the run is complete (the rule); True/False forces it (unit tests)."""
    do_test = bool(status and status.get("complete")) if test is None else bool(test)
    rows, untestable = [], []
    for key, label, y, arms, tasks, filt, focal, other, kind in TESTS:
        d = A.subset(df, MODEL, arms, tasks=tasks, extra=filt)
        nm = A.name_means(d, y)
        base = {"key": key, "test": label, "kind": kind, "outcome": y, "arms": arms, "tasks": tasks,
                "focal": focal, "names": int(nm["mean"].notna().sum()) if len(nm) else 0,
                "episodes": int(d[y].notna().sum()) if len(d) else 0}
        if len(nm) < 4:
            untestable.append({**base, "note": "too few names"})
            continue
        r = A.name_level_test(nm, focal, other)
        if r.note == A.NO_VARIATION:
            untestable.append({**base, "est": r.est, "note": A.NO_VARIATION})
            continue
        if not np.isfinite(r.est) or not np.isfinite(r.ci_lo):
            untestable.append({**base, "note": "not estimable"})
            continue
        row = {**base, "est": float(r.est), "se": float(r.se), "df": float(r.df), "ci_lo": float(r.ci_lo),
               "ci_hi": float(r.ci_hi), "n_focal": r.n_a, "n_comparison": r.n_b,
               "mean_focal": r.mean_a, "mean_comparison": r.mean_b, "freq_in_model": r.freq_in_primary,
               "display": _display(kind, r.est), "display_lo": _display(kind, r.ci_lo),
               "display_hi": _display(kind, r.ci_hi), "unit": "%" if kind == "price" else "pts"}
        if do_test:
            row["p"] = float(r.p)
        rows.append(row)
    if do_test and rows:
        for row, q in zip(rows, A.bh([r_["p"] for r_ in rows])):
            row["q_bh"] = float(q)
            row["discovery_q10"] = bool(q < BH_Q)
    return {"note": TAG + " Own Benjamini-Hochberg family at 10%, separate from every other family (D14).",
            "model": MODEL, "run_status": status, "status_text": status_text(status), "tested": do_test,
            "bh_q": BH_Q, "n_tests": len(rows) if do_test else 0,
            "n_discoveries": sum(r_.get("discovery_q10", False) for r_ in rows),
            "freq_source": df.attrs.get("freq_source"), "rows": rows, "untestable": untestable}


# ----------------------------------------------------------------------------- training-data link (Figure A3)

def load_counts(path: Path = COUNTS) -> pd.DataFrame:
    c = pd.read_csv(path, dtype={"word_ambiguity_flag": str})
    c["flagged"] = c["word_ambiguity_flag"].fillna("").str.strip() != ""
    return c


def name_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """Per core name: OLMo's S0 cell-adjusted mean log price and the gap vs the average name, in percent."""
    nm = A.name_means(A.subset(df, MODEL, ["S0"]), "logp")
    if nm.empty:
        return nm
    nm = nm.dropna(subset=["mean"]).copy()
    nm["gap_pct"] = 100 * (np.exp(nm["mean"] - nm["mean"].mean()) - 1)
    nm["grp"] = nm["race"].fillna("") + " " + nm["gender"].fillna("")
    return nm


def _spear(x, y) -> dict:
    x, y = pd.Series(x, dtype=float), pd.Series(y, dtype=float)
    ok = x.notna() & y.notna()
    if ok.sum() < 4 or x[ok].nunique() < 2 or y[ok].nunique() < 2:
        return {"rho": None, "p": None, "n": int(ok.sum())}
    r = stats.spearmanr(x[ok], y[ok])
    return {"rho": float(r.statistic if hasattr(r, "statistic") else r[0]),
            "p": float(r.pvalue if hasattr(r, "pvalue") else r[1]), "n": int(ok.sum())}


def training_link(df: pd.DataFrame, counts_path: Path = COUNTS, min_names: int = 6) -> dict | None:
    """Spearman rho between log count (OLMo 3 index) and each core name's S0 price gap, plus the two
    sensitivities. Returns None when there are no OLMo outcomes or no counts file."""
    if not Path(counts_path).exists() or not (df["model"] == MODEL).any():
        return None
    nm = name_gaps(df)
    if len(nm) < min_names:
        return {"note": "too few OLMo names", "names": nm}
    first = A.load_names()[["profile_id", "first"]]
    nm = nm.merge(first, on="profile_id", how="left")
    c = load_counts(counts_path)
    for idx, col in ((INDEX_PRIMARY, "log_count"), (INDEX_OLMO2, "log_count_olmo2")):
        ci = c[c["index"] == idx][["first", "count", "flagged"]]
        nm = nm.merge(ci.rename(columns={"count": col.replace("log_", "raw_"), "flagged": f"flag_{col}"}),
                      on="first", how="left")
        nm[col] = np.log1p(nm[col.replace("log_", "raw_")].astype(float))
    nm["word_flagged"] = nm["flag_log_count"].fillna(False).astype(bool)
    nm = nm.drop(columns=["flag_log_count", "flag_log_count_olmo2"])
    main = _spear(nm["log_count"], nm["gap_pct"])
    unfl = nm[~nm["word_flagged"]]
    return {"index": INDEX_PRIMARY, "index_words": INDEX_WORDS, "names": nm,
            "rho": main["rho"], "p": main["p"], "n": main["n"],
            "unflagged": {**_spear(unfl["log_count"], unfl["gap_pct"]),
                          "dropped": sorted(nm.loc[nm["word_flagged"], "first"].tolist())},
            "olmo2": {**_spear(nm["log_count_olmo2"], nm["gap_pct"]), "index": INDEX_OLMO2,
                      "index_words": INDEX_OLMO2_WORDS}}


def _pfmt(p) -> str:
    if p is None or not np.isfinite(p):
        return "n/a"
    return "<.001" if p < 0.001 else f"{p:.3f}".lstrip("0")


def _peq(p) -> str:
    v = _pfmt(p)
    return "p < .001" if v.startswith("<") else f"p = {v}"


def link_sentence(link: dict | None) -> str:
    """One plain sentence (no leading capital, so it can follow a colon)."""
    if not link or link.get("rho") is None:
        return "not run"
    u, o2 = link["unflagged"], link["olmo2"]
    s = (f"across the {link['n']} core names, a name's count in {INDEX_WORDS} and its clear-request price gap had "
         f"Spearman rho = {link['rho']:.2f} ({_peq(link['p'])}; exploratory, traced, correlation only)")
    if u.get("rho") is not None:
        s += (f". Without the {len(u['dropped'])} names that are also common words, rho = {u['rho']:.2f} "
              f"({_peq(u['p'])})")
    if o2.get("rho") is not None:
        s += f"; on the OLMo 2 index, rho = {o2['rho']:.2f} ({_peq(o2['p'])})"
    return s


def link_json(link: dict | None) -> dict | None:
    if not link:
        return None
    out = {k: v for k, v in link.items() if k != "names"}
    if isinstance(link.get("names"), pd.DataFrame):
        cols = [c for c in ("profile_id", "first", "race", "gender", "gap_pct", "raw_count", "log_count",
                            "raw_count_olmo2", "log_count_olmo2", "word_flagged") if c in link["names"].columns]
        out["per_name"] = link["names"][cols].to_dict("records")
    out["sentence"] = link_sentence(link)
    out["label"] = "exploratory; traced, correlation only; not in any BH family"
    return out


# ----------------------------------------------------------------------------- outputs

def fmt_row(r: dict) -> str:
    u = "%" if r["kind"] == "price" else " pts"
    return f"{_s1(r['display'])}{u} ({_s1(r['display_lo'])} to {_s1(r['display_hi'])})"


def table_frame(b: dict) -> pd.DataFrame:
    recs = []
    for r in b["rows"]:
        recs.append({"Outcome": r["test"], "Gap (focal minus comparison), 95% CI": fmt_row(r),
                     "Names": r["names"], "Episodes": f"{r['episodes']:,}",
                     "p": _pfmt(r.get("p")) if b["tested"] else "not tested",
                     "BH q": (f"{r['q_bh']:.3f}".lstrip("0") if b["tested"] else "not tested"),
                     "Flag (q < .10)": ("yes" if r.get("discovery_q10") else "no") if b["tested"] else ""})
    for r in b["untestable"]:
        recs.append({"Outcome": r["test"], "Gap (focal minus comparison), 95% CI": r["note"], "Names": r["names"],
                     "Episodes": f"{r['episodes']:,}", "p": "", "BH q": "", "Flag (q < .10)": ""})
    return pd.DataFrame(recs)


def table_note(b: dict, link: dict | None) -> str:
    note = (f"{TAG} {b['status_text']}. Name level, as in the pre-registered tests: cell-adjusted name means, OLS "
            "with HC2 errors, 95% CI across names. Price gaps are exp(b) - 1 in percent; rates in percentage "
            "points. Black vs White rows hold gender fixed and the reverse. ")
    note += ("These tests form their own Benjamini-Hochberg family at 10%, separate from the frozen exploratory "
             "family and the add-on family. " if b["tested"] else
             "The run is not finished, so these are estimates only and no row is tested. ")
    if link and link.get("rho") is not None:
        s = link_sentence(link)
        note += "Training-data link (Figure A3): " + s[0].upper() + s[1:] + "."
    return note


def write_outputs(b: dict, link: dict | None, results_dir: Path, tabdir: Path) -> dict:
    results_dir, tabdir = Path(results_dir), Path(tabdir)
    results_dir.mkdir(parents=True, exist_ok=True)
    tabdir.mkdir(parents=True, exist_ok=True)
    jp = results_dir / "olmo_exploratory.json"
    jp.write_text(json.dumps({**b, "training_link": link_json(link)}, indent=1, default=A._json_default))
    return {"json": str(jp), **write_table(b, link, tabdir)}


def write_table(b: dict, link: dict | None, tabdir: Path) -> dict:
    tabdir = Path(tabdir)
    t = table_frame(b)
    csv, md = tabdir / "olmo_exploratory.csv", tabdir / "olmo_exploratory.md"
    t.to_csv(csv, index=False)
    lines = ["*Table B4. OLMo 3 7B, separate exploratory block*", ""]
    cols = list(t.columns)
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "---|" * len(cols))
    for _, r in t.iterrows():
        lines.append("| " + " | ".join(str(v) for v in r.tolist()) + " |")
    lines += ["", table_note(b, link)]
    md.write_text("\n".join(lines) + "\n")
    return {"csv": str(csv), "md": str(md)}


def numbers(b: dict | None, link: dict | None) -> dict:
    """numbers.json olmo.* keys."""
    N = {}
    pend = "pending (OLMo run not scored)"
    N["olmo.status"] = b["status_text"] if b else pend
    N["olmo.rho"] = f"{link['rho']:.2f}" if link and link.get("rho") is not None else \
        "n/a (no OLMo outcomes or no name counts)"
    N["olmo.rho_p"] = _pfmt(link["p"]) if link and link.get("rho") is not None else "n/a"
    N["olmo.rho_names"] = str(link["n"]) if link and link.get("rho") is not None else "n/a"
    u = (link or {}).get("unflagged") or {}
    o2 = (link or {}).get("olmo2") or {}
    N["olmo.rho_unflagged"] = (f"{u['rho']:.2f} (p {_pfmt(u['p'])}, {u['n']} names)" if u.get("rho") is not None
                               else "n/a")
    N["olmo.rho_olmo2"] = f"{o2['rho']:.2f} (p {_pfmt(o2['p'])})" if o2.get("rho") is not None else "n/a"
    N["olmo.training_link_sentence"] = (link_sentence(link)
                                        if link and link.get("rho") is not None else "not run")
    N["olmo.index_words"] = INDEX_WORDS
    rows = {r["key"]: r for r in (b or {}).get("rows", [])}
    unt = {r["key"]: r for r in (b or {}).get("untestable", [])}
    for key, *_ in TESTS:
        r = rows.get(key)
        if r:
            u = "%" if r["kind"] == "price" else ""
            N[f"olmo.{key}.est"] = f"{_s1(r['display'])}{u or ' pts'}"
            N[f"olmo.{key}.ci"] = f"{_s1(r['display_lo'])}{u} to {_s1(r['display_hi'])}{u}"
            N[f"olmo.{key}.q"] = f"{r['q_bh']:.3f}".lstrip("0") if "q_bh" in r else "not tested"
        else:
            N[f"olmo.{key}.est"] = unt[key]["note"] if key in unt else pend
            N[f"olmo.{key}.ci"] = "n/a"
            N[f"olmo.{key}.q"] = "n/a"
    if b and rows:
        h1, h4 = rows.get("h1_price"), rows.get("h4_pick")
        bits = []
        if h1:
            v = h1["display"]
            side = "more" if v > 0 else "less"
            amt = f"{abs(v):.1f}% {side} than" if abs(v) >= 0.05 else "about the same as"
            bits.append(f"names associated with Black buyers paid {amt} names associated with White buyers "
                        f"(95% CI {_s1(h1['display_lo'])}% to {_s1(h1['display_hi'])}%)")
        if h4:
            bits.append(f"the gap in guessing the identity-linked product when it bought without asking was "
                        f"{_s1(h4['display'])} points (95% CI {_s1(h4['display_lo'])} to {_s1(h4['display_hi'])})")
        tail = (f"; {b['n_discoveries']} of {b['n_tests']} OLMo tests flagged at q < .10" if b["tested"] else
                "; partial run, estimates only")
        N["olmo.estimates_sentence"] = "On OLMo 3 7B (exploratory), " + " and ".join(bits) + tail + "."
    else:
        N["olmo.estimates_sentence"] = pend
    return N


def run(logs: Path = LOGS, results_dir: Path = A.RESULTS, tabdir: Path = TAB, run_name: str = RUN) -> dict:
    csv = Path(logs) / f"{run_name}.outcomes.csv"
    if not csv.exists():
        raise SystemExit(f"{csv} not found: score the run first (run_agents.py score --run {run_name})")
    df = A.load_outcomes([str(csv)])
    st = run_status(csv)
    b = block(df, st)
    link = training_link(df)
    files = write_outputs(b, link, results_dir, tabdir)
    return {"files": files, "status": b["status_text"], "tested": b["tested"], "n_tests": b["n_tests"],
            "n_discoveries": b["n_discoveries"], "rho": (link or {}).get("rho")}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--logs", default=str(LOGS))
    ap.add_argument("--results", default=str(A.RESULTS))
    ap.add_argument("--tabdir", default=str(TAB))
    ap.add_argument("--run", default=RUN)
    a = ap.parse_args(argv)
    print(json.dumps(run(Path(a.logs), Path(a.results), Path(a.tabdir), a.run), indent=1, default=str))


if __name__ == "__main__":
    main()
