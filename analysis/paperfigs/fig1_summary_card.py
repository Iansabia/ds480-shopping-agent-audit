"""Figure 1: forest plot of the 8 pre-registered confirmatory tests (H1 to H4, Haiku and Luna).

(a) price gaps in percent (H1, H2); (b) rate gaps in percentage points (H3, H4).
Asterisk: gap detected after Holm (p_holm < 0.05). Filled markers: confirmatory models.
Faint dotted segments: each test's equivalence margin. Numbers come straight from
paper/figures/fig4_price_gap.csv (price) and results/confirmatory.json (rates).
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd  # noqa: E402
from paperfigs.style import *  # noqa: E402,F401,F403
from paperfigs.style import FIGDATA, RESULTS, FULL, MODEL, MARKER, GRAY, panel, save, plt, signed, mstyle  # noqa: E402

NAME = "fig1_summary_card"
HYP = {"H1": "Price, Black vs White", "H2": "Price, women vs men",
       "H3": "Need stated, Black vs White", "H4": "Need guessed, Black vs White"}
MODELS = ["haiku", "luna"]


def load():
    pr = pd.read_csv(FIGDATA / "fig4_price_gap.csv")
    conf = json.loads((RESULTS / "confirmatory.json").read_text())
    rows = []
    for h in ("H1", "H2"):
        for m in MODELS:
            r = pr[(pr.model == m) & (pr.hypothesis == h)].iloc[0]
            mar = r.margin_log
            rows.append(dict(h=h, m=m, est=r.gap_pct, lo=r.ci_pct_lo, hi=r.ci_pct_hi,
                             sig=r.p_holm < 0.05,
                             mlo=100 * (math.exp(-mar) - 1), mhi=100 * (math.exp(mar) - 1)))
    for h in ("H3", "H4"):
        for m in MODELS:
            r = next(x for x in conf["rows"] if x["model"] == m and x["hypothesis"] == h)
            rows.append(dict(h=h, m=m, est=100 * r["r_est"], lo=100 * r["r_ci_lo"],
                             hi=100 * r["r_ci_hi"], sig=r["p_holm"] < 0.05,
                             mlo=-100 * r["tost_margin"], mhi=100 * r["tost_margin"]))
    return pd.DataFrame(rows)


def draw(ax, d, xlabel, lim, ticks):
    d = d.reset_index(drop=True)
    # each hypothesis gets an italic header row, then one row per model
    ys, labels, heads, y = [], [], [], 0.0
    for i, r in d.iterrows():
        if i == 0 or r.h != d.h[i - 1]:
            if i:
                y += 0.35
            heads.append((-y, HYP[r.h]))
            y += 0.85
        ys.append(-y)
        labels.append(MODEL[r.m])
        y += 1
    ax.axvline(0, color=GRAY["mid"], lw=0.6, zorder=0)
    for yy, r in zip(ys, d.itertuples()):
        for xm in (r.mlo, r.mhi):
            ax.plot([xm, xm], [yy - 0.45, yy + 0.45], ls=(0, (1, 1.5)), color=GRAY["mid"], lw=0.8, zorder=1)
        ax.plot([r.lo, r.hi], [yy, yy], color=GRAY["dark"], lw=0.9, zorder=2)
        ax.plot(r.est, yy, ls="none", zorder=3, **{**mstyle(r.m, ms=4.2), "color": None})
        if r.sig:
            ax.text(r.hi, yy, " *", ha="left", va="center", fontsize=9, color=GRAY["dark"])
    ax.set_yticks(ys, labels)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    for yy, txt in heads:
        ax.text(-0.025, yy, txt, transform=ax.get_yaxis_transform(), ha="right", va="center",
                style="italic", fontsize=7.5)
    ax.set_xlim(-lim, lim)
    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(signed(0))
    ax.set_ylim(min(ys) - 0.6, 0.5)
    ax.set_xlabel(xlabel)


def make():
    d = load()
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL, 1.9))
    fig.subplots_adjust(left=0.2, right=0.99, wspace=0.62, bottom=0.24, top=0.9)
    draw(a, d[d.h.isin(["H1", "H2"])], "Gap in price paid (%)", 5.6, [-4, -2, 0, 2, 4])
    draw(b, d[d.h.isin(["H3", "H4"])], "Gap in coily or deep-shade pick (points)", 12.5, [-10, -5, 0, 5, 10])
    panel(a, "a", x=-0.2)
    panel(b, "b", x=-0.2)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
