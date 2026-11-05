"""Six race groups in the headline figure, plus one omnibus price test (PLAN.md D12).

Ian's decision of Thu 11/5 (paper/FIGURES_SPEC.md, "all races in the headline
figure"), made after the main results were seen. Exploratory. Nothing here
touches results/confirmatory.*, results/exploratory.* or the add-on family in
results/addon_exploratory.json.

  * The group rows are read from the add-on tables that analysis/addon_analysis.py
    already wrote (paper/tables/addon_C_race_gaps.csv and addon_C_race_groups.csv),
    so every number in the figure is the same number as in Table C. Black vs White
    rows are the confirmatory H1 and H4.
  * The one new test: "does S0 price differ across any of the six race groups?"
    Name level, same cell residualization of log price as PLAN 5.1 (task x arm x
    wording x order, one residualization over every named group the model has, as
    in Table C). OLS of the name means on five race indicators (White is the base)
    plus a women's-name indicator; statistic: the F for the five race terms.
    p from 10,000 shuffles of the race label across names within gender (seed 480),
    with the classical F p beside it. One test per model; Gemini 3.5 Flash-Lite ran
    core names only (two groups), so it gets none.

    .venv/bin/python analysis/race_headline.py       # writes results/race_omnibus.json and paper/tables/race_headline.*

analysis/make_figures.py draws Figure 3 from these outputs (no inference there).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import analyze as A  # noqa: E402
import figstyle as S  # noqa: E402

TAB = ROOT / "paper" / "tables"
RES = ROOT / "results"
OMNIBUS = RES / "race_omnibus.json"
RACES = ["White", "Black", "Hispanic", "Asian", "MENA", "South Asian"]
NAMES_OF = {"White": "White", "Black": "Black", "Hispanic": "Hispanic", "Asian": "Asian",
            "MENA": "Arab or Middle Eastern", "South Asian": "South Asian"}
MODELS = ["haiku", "luna", "flashlite"]
OFFS = {"haiku": -0.2, "luna": 0.0, "flashlite": 0.2}
SHORT = {"haiku": "Haiku", "luna": "Luna", "flashlite": "Gemini"}
N_PERM = 10_000
TAG = "Exploratory, added after the main results were seen (PLAN D12)."


# ----------------------------------------------------------------------------- omnibus test

def _race_f(y: np.ndarray, race: np.ndarray, woman: np.ndarray, groups: list[str]) -> tuple[float, int, int]:
    """F for the race terms: OLS of y on [1, woman, race dummies] vs [1, woman]."""
    X0 = np.column_stack([np.ones_like(y), woman])
    X1 = np.column_stack([X0] + [(race == g).astype(float) for g in groups[1:]])

    def rss(X):
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ b
        return float(e @ e)
    q, dfr = X1.shape[1] - X0.shape[1], len(y) - X1.shape[1]
    r0, r1 = rss(X0), rss(X1)
    return ((r0 - r1) / q) / (r1 / dfr), q, dfr


def omnibus(df: pd.DataFrame, model: str, n_perm: int = N_PERM, seed: int = A.SEED) -> dict:
    import addon_analysis as X
    dm = df[(df["model"] == model) & df["preset"].isin(["main", "arab", "sasian"])]
    d = X.named(dm, model, ["S0"])
    d = d[d["logp"].notna()]
    nm = A.name_means(d, "logp")
    nm = nm[nm["race"].isin(RACES)].dropna(subset=["mean"]).reset_index(drop=True)
    groups = [r for r in RACES if (nm["race"] == r).sum() >= 2]
    nm = nm[nm["race"].isin(groups)].reset_index(drop=True)
    names = {r: int((nm["race"] == r).sum()) for r in groups}
    if len(groups) < 3:
        return {"model": model, "groups": groups, "names": names, "note": "fewer than 3 groups: not run"}
    y, race, woman = nm["mean"].to_numpy(float), nm["race"].to_numpy(), nm["is_woman"].to_numpy(float)
    f, q, dfr = _race_f(y, race, woman, groups)
    rng = np.random.default_rng(seed)
    idx_w, idx_m = np.where(woman == 1)[0], np.where(woman == 0)[0]
    hits = 0
    for _ in range(n_perm):
        r2 = race.copy()
        r2[idx_w] = race[rng.permutation(idx_w)]
        r2[idx_m] = race[rng.permutation(idx_m)]
        if _race_f(y, r2, woman, groups)[0] >= f - 1e-12:
            hits += 1
    return {"model": model, "groups": groups, "names": names, "n_names": int(len(nm)), "F": f, "df1": q, "df2": dfr,
            "p_F": float(stats.f.sf(f, q, dfr)), "p_perm": (hits + 1) / (n_perm + 1), "perm_hits": hits,
            "n_perm": n_perm, "seed": seed,
            "group_mean_pct_vs_white": {r: 100 * (math.exp(float(nm.loc[nm.race == r, "mean"].mean())
                                                           - float(nm.loc[nm.race == "White", "mean"].mean())) - 1)
                                        for r in groups},
            "note": "name level, cell-residualized log price, race F with a women's-name term; "
                    "p from race labels shuffled within gender"}


# ----------------------------------------------------------------------------- rows for the figure

def _gap_rows() -> pd.DataFrame:
    g = pd.read_csv(TAB / "addon_C_race_gaps.csv")
    return g[g["outcome"].isin(["price", "h4"])].copy()


def _rate_rows() -> pd.DataFrame:
    c = pd.read_csv(TAB / "addon_C_race_groups.csv")
    return c[c["outcome"].isin(["h4", "price"])].copy()


def headline_rows(ref_usd: dict[str, float]) -> pd.DataFrame:
    """One row per model x group: price gap vs White names (percent, and dollars at the White names'
    average price paid from Table 1), and the H4-type identity-linked pick rate when the agent guessed."""
    gaps, rates = _gap_rows(), _rate_rows()
    out = []
    for m in MODELS:
        for r in RACES:
            pr = rates[(rates.model == m) & (rates.race == r) & (rates.outcome == "price")]
            h4 = rates[(rates.model == m) & (rates.race == r) & (rates.outcome == "h4")]
            if pr.empty and h4.empty:
                continue
            row = {"model": m, "race": r, "names": int(pr["names"].iloc[0]) if not pr.empty else np.nan}
            gp = gaps[(gaps.model == m) & (gaps.race == r) & (gaps.outcome == "price")]
            ref = ref_usd.get(m, np.nan)
            if r == "White":
                row.update(gap_pct=0.0, gap_lo=np.nan, gap_hi=np.nan, gap_usd=0.0, usd_lo=np.nan, usd_hi=np.nan,
                           price_source="reference", price_adj="")
            elif not gp.empty and pd.notna(gp["gap_display"].iloc[0]):
                e, lo, hi = (float(gp[c].iloc[0]) for c in ("gap_display", "lo_display", "hi_display"))
                row.update(gap_pct=e, gap_lo=lo, gap_hi=hi, gap_usd=e / 100 * ref, usd_lo=lo / 100 * ref,
                           usd_hi=hi / 100 * ref, price_source=gp["source"].iloc[0], price_adj=gp["adjusted"].iloc[0])
            row["ref_usd_white"] = ref
            if not h4.empty and h4["n"].iloc[0]:
                h = h4.iloc[0]
                row.update(h4_rate=100 * h["rate"], h4_lo=100 * h["wilson_lo"], h4_hi=100 * h["wilson_hi"],
                           h4_k=int(h["k"]), h4_n=int(h["n"]), h4_names=int(h["names"]))
            gh = gaps[(gaps.model == m) & (gaps.race == r) & (gaps.outcome == "h4")]
            if not gh.empty:
                row.update(h4_gap=gh["gap"].iloc[0], h4_source=gh["source"].iloc[0], h4_adj=gh["adjusted"].iloc[0])
            out.append(row)
    return pd.DataFrame(out)


def load_omnibus() -> dict:
    return json.loads(OMNIBUS.read_text()) if OMNIBUS.exists() else {}


def omnibus_text(om: dict, label=S.label) -> str:
    parts = []
    for m in MODELS:
        o = om.get(m)
        if not o or "F" not in o:
            continue
        parts.append(f"{label(m)} F({o['df1']}, {o['df2']}) = {o['F']:.2f}, permutation p = "
                     f"{o['p_perm']:.3f}".replace("p = 0.", "p = ."))
    return "; ".join(parts)


# ----------------------------------------------------------------------------- Figure 3

def _p(p):
    return "< .001" if p < 0.001 else f"{p:.3f}".lstrip("0")


def headline_title(t: pd.DataFrame, om: dict) -> str:
    """Takeaway title from the omnibus results (and, for a model with a price difference, whether every group's
    estimate sits on the same side of White names). Never claims a gap the omnibus does not support."""
    yes = [m for m in MODELS if om.get(m, {}).get("p_perm") is not None and om[m]["p_perm"] < 0.05]
    no = [m for m in MODELS if om.get(m, {}).get("p_perm") is not None and om[m]["p_perm"] >= 0.05]
    if not yes and not no:
        return "Price paid and identity-linked picks for six name groups, same request"
    if not yes:
        return ("No price difference across the six name groups on "
                + " or ".join(f"{SHORT[m]} (p = {_p(om[m]['p_perm'])})" for m in no))
    bits = []
    for m in yes:
        g = t[(t.model == m) & (t.race != "White")].dropna(subset=["gap_pct"])
        side = (", every estimate below White names" if len(g) and (g["gap_pct"] < 0).all() else
                ", every estimate above White names" if len(g) and (g["gap_pct"] > 0).all() else "")
        bits.append(f"{SHORT[m]} (p = {_p(om[m]['p_perm'])}{side})")
    title = "Price differs across the six name groups on " + " and ".join(bits)
    if no:
        title += " but not on " + " or ".join(f"{SHORT[m]} (p = {_p(om[m]['p_perm'])})" for m in no)
    return title


def six_group_sentence(t: pd.DataFrame, om: dict) -> str:
    """Lead sentence for the paper (numbers.json result.six_group_sentence): the omnibus result per model, then
    the side every exploratory estimate falls on when a model's price differs. Exploratory, D12."""
    yes, no = [], []
    for m in MODELS:
        o = om.get(m, {})
        if o.get("p_perm") is None:
            continue
        if o["p_perm"] < 0.05:
            g = t[(t.model == m) & (t.race != "White")].dropna(subset=["gap_pct"])
            side = (", with every group paying less than White names" if len(g) and (g["gap_pct"] < 0).all() else
                    ", with every group paying more than White names" if len(g) and (g["gap_pct"] > 0).all() else "")
            yes.append(f"{S.label(m)}'s prices differed (p = {_p(o['p_perm'])}){side}")
        else:
            no.append(f"{S.label(m)}'s did not (p = {_p(o['p_perm'])})" if yes else
                      f"{S.label(m)}'s prices did not differ (p = {_p(o['p_perm'])})")
    if not yes and not no:
        return "Six name groups: not run."
    return "Across six name groups (Figure 3, exploratory), " + "; ".join(yes + no) + "."


def figure(t: pd.DataFrame, om: dict):
    """Price gap vs White names in dollars per purchase (left) and the identity-linked pick when the
    agent guessed (right), six groups, one marker per model. Black row is the pre-registered test."""
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.06, column_widths=[0.54, 0.46])
    ms = [m for m in MODELS if (t["model"] == m).any()]
    nrow = {r: t[(t.race == r) & (t.model.isin(["haiku", "luna"]))]["names"].max() for r in RACES}
    # highlight band behind the pre-registered row
    # (plain shapes: add_hrect skips subplots that have no traces yet, and the matplotlib engine reads these)
    for xr, yr in (("x", "y"), ("x2", "y2")):
        fig.add_shape(type="rect", xref=f"{xr} domain", yref=yr, x0=0, x1=1, y0=0.5, y1=1.5, fillcolor=S.BAND,
                      line=dict(width=0), layer="below")
    for m in ms:
        sub = t[t.model == m]
        open_ = m == "flashlite"
        for _, r in sub.iterrows():
            yi = RACES.index(r["race"]) + OFFS[m]
            if pd.notna(r.get("gap_usd")) and r["race"] != "White":
                lo, hi = r.get("usd_lo"), r.get("usd_hi")
                ht = (f"{S.label(m)}<br>{NAMES_OF[r['race']]} names minus White names: "
                      f"{S.fmt_usd(r['gap_usd'])} per purchase ({r['gap_pct']:+.2f}%"
                      + (f", 95% CI {r['gap_lo']:+.2f} to {r['gap_hi']:+.2f}%" if pd.notna(lo) else "")
                      + f")<br>at the White names' average of ${r['ref_usd_white']:,.2f}"
                      + (f"<br>{r['price_source']}, {r['price_adj']}" if r["race"] != "White" else ""))
                S.dots(fig, [r["gap_usd"]], [yi], [lo if pd.notna(lo) else None], [hi if pd.notna(hi) else None],
                       S.INK if not open_ else S.MUTED, sym=S.symbol(m), htext=[ht], row=1, col=1, size=10,
                       open_=open_)
            if pd.notna(r.get("h4_rate")):
                ht = (f"{S.label(m)}<br>{NAMES_OF[r['race']]} names: {r['h4_rate']:.1f}% "
                      f"[{r['h4_lo']:.1f}, {r['h4_hi']:.1f}] ({int(r['h4_k'])}/{int(r['h4_n'])})"
                      + (f"<br>minus White: {r['h4_gap']}, {r['h4_source']}, {r['h4_adj']}"
                         if isinstance(r.get("h4_gap"), str) else ""))
                S.dots(fig, [r["h4_rate"]], [yi], [r["h4_lo"]], [r["h4_hi"]], S.INK if not open_ else S.MUTED,
                       sym=S.symbol(m), htext=[ht], row=1, col=2, size=10, open_=open_)
    S.vline(fig, 0, 1, 1, layer="below", color=S.AXIS, width=1.2)
    refs = t[t.race == "White"].dropna(subset=["ref_usd_white"])
    fig.add_annotation(x=0.5, y=0, xref="x domain", yref="y", xanchor="center", yanchor="middle", showarrow=False,
                       bgcolor=S.SURFACE, align="center", text="Reference: average paid by White names<br>" + ", ".join(
                           f"{SHORT[m]} ${v:,.2f}" for m, v in zip(refs["model"], refs["ref_usd_white"])),
                       font=dict(size=S.BASE - 4, color=S.MUTED))
    # dollar ticks with the sign before the dollar sign
    vals = np.r_[t["usd_lo"].to_numpy(float), t["usd_hi"].to_numpy(float), 0.0]
    lo_v, hi_v = np.nanmin(vals), np.nanmax(vals)
    # at most 6 ticks, so the labels stay level
    step = next(st for st in (0.1, 0.2, 0.25, 0.5, 1.0, 2.0, 5.0)
                if math.ceil(hi_v / st) - math.floor(lo_v / st) + 1 <= 6)
    tv = np.arange(math.floor(lo_v / step), math.ceil(hi_v / step) + 1) * step
    fig.update_xaxes(tickvals=list(tv), ticktext=[S.fmt_usd(v) if abs(v) > 1e-9 else "$0" for v in tv],
                     range=[tv[0] - step * 0.12, tv[-1] + step * 0.12], row=1, col=1)
    hl = np.nanmin(t["h4_lo"].to_numpy(float)) if "h4_lo" in t else 0
    hh = np.nanmax(t["h4_hi"].to_numpy(float)) if "h4_hi" in t else 100
    r_lo, r_hi = 10 * math.floor(hl / 10), 10 * math.ceil(hh / 10)
    ylab = []
    for r in RACES:
        n = nrow.get(r)
        tag = "pre-registered test" if r == "Black" else ("reference" if r == "White" else "exploratory")
        ylab.append(f"<b>{NAMES_OF[r]} names</b><br><span style='font-size:{S.BASE - 4}px;color:{S.MUTED}'>"
                    f"{int(n) if pd.notna(n) else '?'} names, {tag}</span>")
    fig.update_yaxes(tickvals=list(range(len(RACES))), ticktext=ylab, range=[len(RACES) - 0.45, -0.75], row=1, col=1)
    fig.update_yaxes(range=[len(RACES) - 0.45, -0.75], row=1, col=2)
    fig.update_xaxes(title_text="Paid per purchase vs White names", row=1, col=1)
    fig.update_xaxes(ticksuffix="%", range=[r_lo - 1, r_hi + 1], dtick=10,
                     title_text="Share of guessed hair or skin purchases", row=1, col=2)
    for c, txt in ((1, "Price paid, same clear request (S0)"),
                   (2, "Identity-linked pick when guessing (V)")):
        fig.add_annotation(x=0, y=1.0, xref=f"x{'' if c == 1 else c} domain", yref=f"y{'' if c == 1 else c} domain",
                           xanchor="left", yanchor="bottom", yshift=6, showarrow=False, text=f"<b>{txt}</b>",
                           font=dict(size=S.BASE - 1, color=S.INK))
    ot = omnibus_text(om)
    title = headline_title(t, om)
    sub = ("Same request, only the account name changes. Dots: gap vs names associated with White buyers (left) or "
           "share of purchases (right); bars: 95% intervals. Shaded row: the pre-registered Black vs White test.")
    foot = (f"{TAG} Left: name-level gap in log price vs White names, in dollars at the White names' average price paid "
            "(Table 1); Black row = confirmatory H1 (Holm, m = 8), other rows exploratory (Hispanic and Asian in the "
            "frozen exploratory family, Arab or Middle Eastern and South Asian in the add-on family; BH 10%). Right: "
            "coily 4C hair or deep shade product on hair and skin tasks, vague request, purchases made without "
            "asking; pooled share, 95% Wilson interval; Black vs White = confirmatory H4. Hispanic and Asian: "
            "extended-tier names, main runs; Arab or Middle Eastern and South Asian: add-on runs. Gemini 3.5 "
            "Flash-Lite ran White and Black core names only (open marker, estimate only). "
            + (f"Omnibus test, does price differ across any of the six groups (exploratory): {ot}. " if ot else "")
            + S.marker_key(ms, open_note="flashlite" in ms))
    S.layout(fig, title, sub, False, 150 + 74 * len(RACES) + S.footer_margin(foot), bottom=S.footer_margin(foot),
             left=210, right=24, gap=44)
    S.footer(fig, foot)
    cap = ("Figure 3. Six name groups side by side, for the same request. Left: price paid vs names associated with "
           "White buyers, as a name-level gap in log price (cell-adjusted name means, HC2), shown in dollars per "
           "purchase at the White names' average price paid in Table 1; bars: 95% CI. Right: identity-linked pick "
           "(coily 4C hair or deep shade product) when the agent bought without asking on a vague hair or skin "
           "request; pooled share with 95% Wilson interval. The Black vs White comparison is the pre-registered "
           "confirmatory test (H1 left, H4 right, Holm across 8 tests); every other group is exploratory and was "
           "added to the headline after the main results were seen (PLAN D12). White and Black: 20 core names each; "
           "Hispanic and Asian: 12 extended-tier names each (main runs); Arab or Middle Eastern: 10 names and South "
           "Asian: 8 names (add-on runs). Gemini 3.5 Flash-Lite ran core names only. "
           + (f"One exploratory omnibus test asks whether price differs across any of the six groups (name level, "
              f"race labels shuffled within gender, 10,000 shuffles): {ot}. " if ot else "")
           + "Exact numbers: paper/tables/race_headline.md and addon_C_race_groups.md. The dollar levels by race and "
           "gender cell are in Figure A8.")
    return fig, cap


# ----------------------------------------------------------------------------- main

def write_table(t: pd.DataFrame, om: dict, tabdir: Path = TAB):
    """Writes into the caller's table folder (make_figures passes its --tabdir, so tests never touch paper/tables)."""
    tabdir = Path(tabdir)
    t.to_csv(tabdir / "race_headline.csv", index=False)
    lines = ["# Six name groups (headline Figure 3)", "",
             f"{TAG} Price: gap vs White names for the same clear request (S0), name level, 95% CI, in percent and in "
             "dollars per purchase at the White names' average price paid (Table 1). Identity-linked pick: vague "
             "request, hair and skin tasks, purchases made without asking, pooled share with 95% Wilson interval. "
             "Black vs White rows are the confirmatory H1 and H4.", ""]
    for m in MODELS:
        s = t[t.model == m]
        if s.empty:
            continue
        lines += [f"## {S.label(m)}", "", "| Names | n names | Price gap vs White | Adjusted p or q | Identity-linked pick "
                  "when guessed | Gap vs White |", "|---|---|---|---|---|---|"]
        for _, r in s.iterrows():
            if r["race"] == "White":
                pg = f"reference (${r['ref_usd_white']:,.2f})"
            elif pd.notna(r.get("gap_pct")):
                pg = (f"{r['gap_pct']:+.2f}% [{r['gap_lo']:+.2f}, {r['gap_hi']:+.2f}], "
                      f"{S.fmt_usd(r['gap_usd'])} per purchase")
            else:
                pg = "not run"
            h4 = (f"{r['h4_rate']:.1f}% [{r['h4_lo']:.1f}, {r['h4_hi']:.1f}] ({int(r['h4_k'])}/{int(r['h4_n'])})"
                  if pd.notna(r.get("h4_rate")) else "not run")
            hg = (f"{r['h4_gap']} ({r['h4_adj']})" if isinstance(r.get("h4_gap"), str) else "")
            lines.append(f"| {NAMES_OF[r['race']]} | {int(r['names']) if pd.notna(r['names']) else ''} | {pg} | "
                         f"{r.get('price_adj', '') if isinstance(r.get('price_adj'), str) else ''} | {h4} | {hg} |")
        o = om.get(m)
        if o and "F" in o:
            lines += ["", f"Omnibus (exploratory): F({o['df1']}, {o['df2']}) = {o['F']:.2f}, permutation p = "
                      f"{o['p_perm']:.4f} ({o['perm_hits']:,} of {o['n_perm']:,} shuffles at least as large), "
                      f"classical F p = {o['p_F']:.4f}; {o['n_names']} names."]
        elif o:
            lines += ["", f"Omnibus: {o['note']}."]
        lines.append("")
    (tabdir / "race_headline.md").write_text("\n".join(lines))


def run(n_perm: int = N_PERM) -> dict:
    import addon_analysis as X
    df, _ = X.load()
    om = {m: omnibus(df, m, n_perm) for m in MODELS if (df["model"] == m).any()}
    OMNIBUS.write_text(json.dumps({"note": TAG + " One test per model; not part of any other family.",
                                   **om}, indent=1, default=A._json_default))
    return om


if __name__ == "__main__":
    om = run()
    print(json.dumps({m: {k: o.get(k) for k in ("names", "F", "df1", "df2", "p_perm", "p_F", "note")}
                      for m, o in om.items()}, indent=1, default=str))
