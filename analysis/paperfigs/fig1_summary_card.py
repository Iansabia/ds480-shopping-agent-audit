"""Figure 1: forest plot of the 8 pre-registered confirmatory tests (H1 to H4, Haiku and Luna).

(a) price gaps in percent (H1, H2); (b) rate gaps in percentage points (H3, H4).
No key (Ian 11/7: a reader should never have to look up a key). The row labels name each model and
both models use the same dot, so shape carries nothing. Each panel names its two reference lines
once, in small gray text in a strip above the first heading row (so no label sits on a result
row): "large gap" over the dotted line on the side of the panel's finding (left in (a), right in
(b)) and "no gap" on the other side of the solid zero line. The caption says what the bars and
the asterisk mean.
Bar: 95% interval. Asterisk: gap detected after Holm (p_holm < 0.05). Dotted segments: each test's
equivalence margin (the gap size set in advance as large; the same for every row of a panel).
Numbers come straight from paper/figures/fig4_price_gap.csv (price) and results/confirmatory.json
(rates).

Ian 11/8 (visual review, rank 5 and its CHALLENGE MISSED note): name groups are "Black-associated"
wherever the figure names them, as in the body and Table 1, so the headings in (a) name the two
comparisons and the headings in (b) use Table 1's short names ("Need stated", "Need guessed"). A row
whose whole 95% interval fits inside its dot (Luna's stated-need row) gets a small gray "range
smaller than the dot" under the dot, so it does not read as missing data. No verdict words are
printed; the asterisk marks Table 1's "Different" rows, and the caption says so.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd  # noqa: E402
from paperfigs.style import *  # noqa: E402,F401,F403
from paperfigs.style import FIGDATA, RESULTS, FULL, MODEL, GRAY, save, plt, signed  # noqa: E402

NAME = "fig1_summary_card"
HYP = {"H1": "Black- vs White-associated", "H2": "Women's vs men's",
       "H3": "Need stated", "H4": "Need guessed"}
MODELS = ["haiku", "luna"]

DOT = dict(marker="o", ms=4.2, mfc=GRAY["dark"], mec=GRAY["dark"], mew=0.7)  # one dot for every model
BAR_LW = 0.9     # interval bar width (pt); its default projecting caps reach BAR_LW / 2 past each end
REF_TEXT = dict(fontsize=7, color=GRAY["mid"])  # small muted labels for the reference lines
ZERO_LABEL, MARGIN_LABEL = "no gap", "large gap"
HIDDEN_LABEL = "range smaller than the dot"
SIDES = {"a": "lo", "b": "hi"}  # which dotted line gets the label: where each panel's finding is
STRIP = 1.0      # y of the reference-label strip; the first heading row is at y = 0, rows 1 unit apart
PITCH = 0.179    # inches per row unit (the row spacing the figure had with its old key)
GROUP_GAP = 0.8  # extra space between the two question groups of a panel (room for HIDDEN_LABEL)
BOTTOM_IN, TOP_IN = 0.70, 0.23  # room for the tick labels and three-line x label; for the panel title
XLABEL = {"a": "Gap in price paid (%)\nleft of 0 = Black-associated\nor women's names paid less",
          "b": "Gap in picks (percentage points)\nright of 0 = picked more often\nfor Black-associated names"}


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


def rows_of(d):
    """y of each model row and each italic heading: a heading row, then one row per model."""
    ys, heads, y = [], [], 0.0
    for i, r in d.iterrows():
        if i == 0 or r.h != d.h[i - 1]:
            if i:
                y += GROUP_GAP
            heads.append((-y, HYP[r.h]))
            y += 0.85
        ys.append(-y)
        y += 1
    return ys, heads


def hidden(ax, r):
    """True when the row's whole interval bar, caps included, sits inside its dot at print size."""
    fig = ax.figure
    pts_per_unit = ax.get_position().width * fig.get_figwidth() * 72 / (ax.get_xlim()[1] - ax.get_xlim()[0])
    reach = max(r.hi - r.est, r.est - r.lo) * pts_per_unit + BAR_LW / 2
    return reach < DOT["ms"] / 2


def hidden_label(ax, x, y):
    """HIDDEN_LABEL just under the dot at (x, y), below the ends of the row's dotted segments. When
    the dot sits on the zero line, the label is split at its middle space so the line runs through
    the gap between the words, not through a letter."""
    kw = dict(xy=(x, y), textcoords="offset points", va="top", zorder=4, **REF_TEXT)
    lo, hi = ax.get_xlim()
    if abs(x) < 0.02 * (hi - lo):
        words = HIDDEN_LABEL.split()
        k = len(words) // 2
        kw["xy"] = (0, y)
        ax.annotate(" ".join(words[:k]), xytext=(-1.6, -6.5), ha="right", **kw)
        ax.annotate(" ".join(words[k:]), xytext=(1.6, -6.5), ha="left", **kw)
    else:
        ax.annotate(HIDDEN_LABEL, xytext=(0, -6.5), ha="center", **kw)


def align_titles(fig, titled):
    """Start each panel title at the left edge of that panel's leftmost row label (heading or model
    name), as the panel letters do in every other figure."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    for ax, text in titled:
        labels = [t for t in ax.get_yticklabels() if t.get_text()] + \
                 [t for t in ax.texts if t.get_transform() != ax.transData and t.get_style() == "italic"]
        x0 = min(t.get_window_extent(r).x0 for t in labels)
        xa = ax.transAxes.inverted().transform((x0, 0))[0]
        ax.set_title(text, loc="left", fontsize=8.5, x=xa, pad=6)


def draw(ax, d, xlabel, lim, ticks, margin_side="lo"):
    d = d.reset_index(drop=True)
    ys, heads = rows_of(d)
    ax.set_xlim(-lim, lim)  # set first: hidden() needs the final x scale
    ax.axvline(0, color=GRAY["mid"], lw=0.6, zorder=0)
    for yy, r in zip(ys, d.itertuples()):
        for xm in (r.mlo, r.mhi):
            ax.plot([xm, xm], [yy - 0.45, yy + 0.45], ls=(0, (1, 1.5)), color=GRAY["mid"], lw=0.8, zorder=1)
        ax.plot([r.lo, r.hi], [yy, yy], color=GRAY["dark"], lw=BAR_LW, zorder=2)
        ax.plot(r.est, yy, ls="none", zorder=3, **DOT)
        if r.sig:
            ax.text(r.hi, yy, " *", ha="left", va="center", fontsize=9, color=GRAY["dark"])
        if hidden(ax, r):
            hidden_label(ax, r.est, yy)
    # Name each reference line once, above the rows: "large gap" centred over the dotted line on
    # the side where the panel's finding is (its twin mirrors it), "no gap" on the other side of
    # the zero line, so the strip reads outward from zero.
    assert d.mlo.nunique() == 1 and d.mhi.nunique() == 1, "dotted lines differ between rows"
    side = 1 if margin_side == "hi" else -1
    ax.text(d.mhi[0] if side > 0 else d.mlo[0], STRIP, MARGIN_LABEL, ha="center", va="center", **REF_TEXT)
    ax.annotate(ZERO_LABEL, xy=(0, STRIP), xytext=(-2.5 * side, 0), textcoords="offset points",
                ha="right" if side > 0 else "left", va="center", **REF_TEXT)
    ax.set_yticks(ys, [MODEL[m] for m in d.m])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    for yy, txt in heads:
        ax.text(-0.025, yy, txt, transform=ax.get_yaxis_transform(), ha="right", va="center",
                style="italic", fontsize=7.5)
    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(signed(0))
    ax.set_ylim(min(ys) - 0.6, STRIP + 0.45)
    ax.set_xlabel(xlabel)


def build():
    d = load()
    span = (STRIP + 0.45) - (min(rows_of(d[d.h.isin(["H1", "H2"])].reset_index(drop=True))[0]) - 0.6)
    height = BOTTOM_IN + span * PITCH + TOP_IN
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL, height))
    fig.subplots_adjust(left=0.2, right=0.99, wspace=0.62, bottom=BOTTOM_IN / height,
                        top=1 - TOP_IN / height)
    draw(a, d[d.h.isin(["H1", "H2"])], XLABEL["a"], 5.6, [-4, -2, 0, 2, 4], margin_side=SIDES["a"])
    draw(b, d[d.h.isin(["H3", "H4"])], XLABEL["b"], 12.5, [-10, -5, 0, 5, 10], margin_side=SIDES["b"])
    align_titles(fig, [(a, "(a) Price paid"), (b, "(b) Coily-hair or deep-shade product picked")])
    return fig


def make():
    return save(build(), NAME)


if __name__ == "__main__":
    print(make())
