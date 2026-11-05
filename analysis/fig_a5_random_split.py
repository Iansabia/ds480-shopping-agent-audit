"""Figure A5: is the Luna price gap more than chance? (descriptive appendix figure)

Uses two checks that the frozen plan already has (PLAN 5.2), no new test:

  Random relabeling   the permutation test's draws, kept instead of only
                      counted: the focal label (Black/White for H1,
                      woman/man for H2) is shuffled across the 40 core names
                      within the other axis, so every draw splits the names
                      into two random groups of 20, and the frozen primary
                      model (same residualized name means, same design
                      matrix, same frequency rule) is refit. Statistic = b.
  Same-group floor    analyze.noise_floor's draws: the gap between two
                      random halves of names from the same group (2,000
                      splits, within each focal level), as pre-registered.

Reports for Luna H1, Luna H2 and Haiku H1 (contrast): the real gap, the share
of random relabelings with a gap at least as large (two-sided), the SD of the
random gaps, the ratio, and the same three numbers against the same-group
floor. Fixed seed (analyze.SEED), so a rerun gives the same numbers.

Run alone (writes paper/figures/figA5_random_split.{png,svg,html,csv} and the
figA5 entry in CAPTIONS.md) or from make_figures.build (figA5 is then part of
the normal caption file):

  .venv/bin/python analysis/fig_a5_random_split.py --outcomes logs/main_haiku.outcomes.csv logs/main_luna.outcomes.csv
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import analyze as A  # noqa: E402
import figstyle as S  # noqa: E402

N_RELABEL = 10000
N_FLOOR = A.N_BOOT_NOISE          # 2,000 splits, as in PLAN 5.2 and analyze.noise_floor
PANELS = [("luna", "H1"), ("luna", "H2")]
CONTRAST = [("haiku", "H1")]
AXIS_TEXT = {"H1": "Black minus White names", "H2": "Women minus men names"}
PANEL_TEXT = {"H1": "H1: names associated with Black vs White buyers",
              "H2": "H2: names associated with women vs men"}


def pct(x):
    return 100.0 * (np.exp(np.asarray(x, float)) - 1.0)


def relabel_draws(nm: pd.DataFrame, focal: str, other: str, n: int = N_RELABEL, seed: int = A.SEED):
    """Same loop as the permutation test in analyze.name_level_test (shuffle
    within the other axis, refit with the primary design matrix), but every
    draw's b is kept."""
    nm = nm.dropna(subset=["mean"]).reset_index(drop=True)
    y = nm["mean"].to_numpy(float)
    use_freq, _ = A.freq_rule(nm, focal)
    X = A.design_matrix(nm, focal, other, use_freq)
    rng = np.random.default_rng(seed)
    strata = nm[other].to_numpy()
    lab = nm[focal].to_numpy(float)
    out = np.empty(n)
    for i in range(n):
        perm = lab.copy()
        for sv in np.unique(strata):
            idx = np.where(strata == sv)[0]
            perm[idx] = rng.permutation(perm[idx])
        Xp = X.copy()
        Xp[:, 1] = perm
        out[i] = np.linalg.lstsq(Xp, y, rcond=None)[0][1]
    return out


def floor_draws(nm: pd.DataFrame, focal: str, n: int = N_FLOOR, seed: int = A.SEED):
    """Same draws as analyze.noise_floor (its SD is the reported noise floor)."""
    rng = np.random.default_rng(seed)
    gaps, lvl = [], []
    for lv in (0, 1):
        g = nm[nm[focal] == lv]["mean"].dropna().to_numpy()
        if len(g) < 4:
            continue
        for _ in range(n // 2):
            p = rng.permutation(len(g))
            h = len(g) // 2
            gaps.append(g[p[:h]].mean() - g[p[h:2 * h]].mean())
            lvl.append(lv)
    return np.asarray(gaps), np.asarray(lvl)


def compute(df: pd.DataFrame, cases=PANELS + CONTRAST) -> dict:
    res = {}
    for model, h in cases:
        if model not in set(df["model"]):
            continue
        spec = A.HYPOTHESES[h]
        r, nm = A.run_hypothesis(df, model, h)
        if not np.isfinite(r.est):
            continue
        rel = relabel_draws(nm, spec["focal"], spec["other"])
        flo, flv = floor_draws(nm, spec["focal"])
        nf = A.noise_floor(nm, spec["focal"], spec["other"])
        assert abs(float(np.std(flo)) - nf) < 1e-12, "floor draws must match analyze.noise_floor"
        est = float(r.est)
        share_rel = float(np.mean(np.abs(rel) >= abs(est) - 1e-12))
        share_flo = float(np.mean(np.abs(flo) >= abs(est) - 1e-12))
        res[(model, h)] = dict(
            model=model, hypothesis=h, names=int(r.n_a + r.n_b), real_gap_log=est, real_gap_pct=float(pct(est)),
            relabel_draws=len(rel), relabel_share_at_least_real=share_rel,
            relabel_count_at_least_real=int(np.sum(np.abs(rel) >= abs(est) - 1e-12)),
            relabel_sd_log=float(np.std(rel)), relabel_sd_pct=float(np.std(pct(rel))),
            relabel_ratio=abs(est) / float(np.std(rel)),
            relabel_mean_pct=float(np.mean(pct(rel))),
            floor_draws=len(flo), floor_share_at_least_real=share_flo,
            floor_sd_log=float(np.std(flo)), floor_sd_pct=float(np.std(pct(flo))),
            floor_ratio=abs(est) / float(np.std(flo)),
            perm_p_confirmatory_note="permutation p in results/confirmatory.json uses 20,000 draws",
            _rel=rel, _flo=flo, _flv=flv)
    return res


def _bins(lo, hi, w):
    return np.arange(math.floor(lo / w) * w, math.ceil(hi / w) * w + w / 2, w)


def build_figure(res: dict):
    ps = [k for k in PANELS if k in res]
    if not ps:
        return None, None
    fig = make_subplots(rows=len(ps), cols=1, vertical_spacing=0.2)
    w = 0.1   # bin width, percent
    allv = np.concatenate([np.concatenate([pct(res[k]["_rel"]), pct(res[k]["_flo"]), [res[k]["real_gap_pct"]]])
                           for k in ps])
    lim = max(abs(allv.min()), abs(allv.max())) + 0.3
    edges = _bins(-lim, lim, w)
    mids = (edges[:-1] + edges[1:]) / 2
    rows = []
    for i, k in enumerate(ps, start=1):
        r = res[k]
        rel, flo = pct(r["_rel"]), pct(r["_flo"])
        hr = 100 * np.histogram(rel, edges)[0] / len(rel)
        hf = 100 * np.histogram(flo, edges)[0] / len(flo)
        fig.add_trace(go.Bar(x=mids, y=hr, width=w * 0.92, marker=dict(color=S.MUTED_SERIES, line=dict(width=0)),
                             hovertemplate="%{x:.2f}%: %{y:.1f}% of random relabelings<extra></extra>"), row=i, col=1)
        fig.add_trace(go.Scatter(x=edges, y=np.append(hf, hf[-1]), mode="lines", line=dict(color=S.MUTED, width=1.6,
                                 shape="hv"), hovertemplate="%{x:.2f}%: %{y:.1f}% of same-group splits<extra></extra>"),
                      row=i, col=1)
        S.vline(fig, r["real_gap_pct"], i, 1, layer="above", color=S.ACCENT, width=2.5)
        S.vline(fig, 0, i, 1, layer="below", color=S.AXIS, width=1)
        ymax = max(hr.max(), hf.max())
        fig.update_yaxes(range=[0, ymax * 1.32], showgrid=True, gridcolor=S.GRID, ticksuffix="%",
                         tickfont=dict(color=S.MUTED), row=i, col=1)
        fig.update_xaxes(range=[edges[0], edges[-1]], showgrid=False, ticksuffix="%", dtick=0.5,
                         showline=True, linecolor=S.AXIS, ticks="outside",
                         title_text=f"Price gap, {AXIS_TEXT[k[1]]}", row=i, col=1)
        share = r["relabel_count_at_least_real"]
        share_txt = (f"0 of {r['relabel_draws']:,} random splits as large" if share == 0 else
                     f"{share:,} of {r['relabel_draws']:,} random splits as large")
        fig.add_annotation(xref=f"x{'' if i == 1 else i}", yref=f"y{'' if i == 1 else i} domain",
                           x=r["real_gap_pct"], y=0.98, xanchor="left", yanchor="top", xshift=6, align="left",
                           text=(f"<b>Real gap {r['real_gap_pct']:+.2f}%</b><br>{share_txt}<br>"
                                 f"{r['relabel_ratio']:.1f}x the typical random gap"),
                           font=dict(size=S.BASE - 3, color=S.ACCENT))
        xd, yd = fig.get_subplot(i, 1).xaxis.domain, fig.get_subplot(i, 1).yaxis.domain
        fig.add_annotation(text=f"<span style='font-weight:600'>{S.label(k[0])}, {PANEL_TEXT[k[1]]}</span>",
                           xref="paper", yref="paper", x=xd[0], y=yd[1], xanchor="left", yanchor="bottom", yshift=8,
                           showarrow=False, align="left", font=dict(size=S.BASE - 1, color=S.INK))
        # direct labels for the two distributions, top right of the panel
        for yy, txt in ((0.97, f"Bars: random split into two groups of 20 (SD {r['relabel_sd_pct']:.2f}%)"),
                        (0.86, f"Line: random halves within one group (SD {r['floor_sd_pct']:.2f}%)")):
            fig.add_annotation(xref=f"x{'' if i == 1 else i} domain", yref=f"y{'' if i == 1 else i} domain",
                               x=1, y=yy, xanchor="right", yanchor="top", text=txt, align="right",
                               font=dict(size=S.BASE - 3, color=S.MUTED))
        for lab, arr in (("random relabeling", hr), ("same-group halves", hf)):
            for x0, x1, v in zip(edges[:-1], edges[1:], arr):
                rows.append({"model": k[0], "hypothesis": k[1], "distribution": lab, "bin_lo_pct": round(x0, 4),
                             "bin_hi_pct": round(x1, 4), "share_pct": v})
    fig.update_layout(bargap=0, barmode="overlay")
    foot = ("Gray bars: the gap from the frozen primary model after the group label is shuffled across the 40 core "
            "names (within the other axis), 10,000 shuffles. Gray line: the gap between two random halves of names "
            "from the same group, 2,000 splits (10 names per half, so conservative; the 20 vs 20 shuffle is the "
            "like-for-like baseline). Blue line: the real gap. Same name averages as the confirmatory test; "
            "fixed seed. Descriptive; uses checks fixed in the plan, not a new test.")
    S.layout(fig, "GPT-6 Luna's price gaps are larger than almost every random split of the names",
             "Price gap for the same clear request when names are put into two random groups, vs the real gap.",
             False, 300 * len(ps) + 140 + S.footer_margin(foot), bottom=S.footer_margin(foot), left=60, gap=42)
    S.footer(fig, foot)
    return fig, pd.DataFrame(rows)


def ratio(x: float) -> str:
    """One decimal at 1 or above, two below 1 (so 0.145 prints 0.15, not 0.1)."""
    return f"{x:.1f}" if abs(x) >= 1 else f"{x:.2f}"


def caption(res: dict) -> str:
    def part(k):
        r = res[k]
        return (f"{S.label(k[0])} {k[1]}: real gap {r['real_gap_pct']:+.2f}%; {r['relabel_count_at_least_real']:,} of "
                f"{r['relabel_draws']:,} random relabelings had a gap at least as large; typical random gap (SD) "
                f"{r['relabel_sd_pct']:.2f}%, so the real gap is {ratio(r['relabel_ratio'])} times it; same-group "
                f"halves SD {r['floor_sd_pct']:.2f}% ({ratio(r['floor_ratio'])} times)")
    parts = "; ".join(part(k) for k in PANELS + CONTRAST if k in res)
    return ("Figure A5. Is the GPT-6 Luna price gap more than chance? For the same clear request (S0, core names), "
            "the 40 name averages used in the confirmatory test are split into two random groups of 20 by shuffling "
            "the group label within the other axis, and the frozen primary model is refit (10,000 shuffles, fixed "
            "seed; gray bars). The gray line is the gap between two random halves of names from the same group "
            "(2,000 splits); each half has only 10 names, so this spread is wider than a 20 vs 20 comparison and the "
            "check is conservative. The random 20 vs 20 relabeling is the like-for-like baseline. The blue line is the "
            "real gap. Both checks were set in the plan before the main run; "
            "this figure only draws them. " + parts + ". Claude Haiku 5.5 H1 is given for contrast and not drawn.")


def write_caption_entry(figdir: Path, rec: dict, cap: str) -> Path:
    """Insert or replace the figA5 section in CAPTIONS.md (standalone run)."""
    p = figdir / "CAPTIONS.md"
    text = p.read_text() if p.exists() else "# Figure captions\n\n"
    entry = (f"## figA5\n\n`{Path(rec['png']).name}` (interactive: `{Path(rec['html']).name}`)\n\n{cap}\n\n")
    lines = text.split("\n")
    start = next((i for i, ln in enumerate(lines) if ln.strip() == "## figA5"), None)
    if start is not None:
        end = next((j for j in range(start + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
        lines[start:end] = entry.rstrip("\n").split("\n") + [""]
        text = "\n".join(lines)
    else:
        anchor = text.find("\n## figA3 (not drawn)")
        text = (text[:anchor + 1] + entry + text[anchor + 1:]) if anchor >= 0 else text.rstrip("\n") + "\n\n" + entry
    p.write_text(text)
    return p


def summary(res: dict) -> dict:
    return {f"{m} {h}": {k: v for k, v in r.items() if not k.startswith("_")} for (m, h), r in res.items()}


def figA5_random_split(out, df: pd.DataFrame, conf: list[str]):
    """Hook for make_figures.build: main runs only (never on pilot data)."""
    if out.pilot or "luna" not in conf:
        return out.skip("figA5", "needs GPT-6 Luna main-run results")
    res = compute(df)
    fig, data = build_figure(res)
    if fig is None:
        return out.skip("figA5", "no Luna price data")
    out.fig("figA5", fig, "figA5_random_split", caption(res), data)
    (out.figdir / "figA5_random_split.json").write_text(json.dumps(summary(res), indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outcomes", nargs="+", required=True)
    ap.add_argument("--figdir", default=str(ROOT / "paper" / "figures"))
    a = ap.parse_args(argv)
    df = A.load_outcomes(a.outcomes)
    res = compute(df)
    fig, data = build_figure(res)
    figdir = Path(a.figdir)
    made: list = []
    rec = S.save(fig, figdir, "figA5_random_split", False, made)
    data.to_csv(figdir / "figA5_random_split.csv", index=False)
    (figdir / "figA5_random_split.json").write_text(json.dumps(summary(res), indent=1))
    cap = write_caption_entry(figdir, rec, caption(res))
    print(json.dumps({"numbers": summary(res), "files": rec, "captions": str(cap)}, indent=1))


if __name__ == "__main__":
    main()
