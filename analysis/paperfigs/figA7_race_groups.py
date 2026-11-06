"""Figure A7: six name groups, four outcomes (two gaps vs White names, two pooled shares)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from paperfigs.style import *  # noqa
from paperfigs.race_common import RACES, MODELS, OFFSET, dot, ylabels, shade, zero, legend_handles

NAME = "figA7_race_groups"


def signed(nd, suffix=""):
    return plt.FuncFormatter(
        lambda v, _: "0" + suffix if abs(v) < 1e-9 else f"{'−' if v < 0 else '+'}{abs(v):.{nd}f}{suffix}")


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    panels = [("price gap vs White (%)",
               "Gap in price paid vs White names (%)\nbelow 0 = paid less than White names", True,
               "Price paid, clear request"),
              ("h3 gap vs White (points)",
               "Gap in coily or deep-shade pick (percentage points)\nabove 0 = picked more than for White names",
               True, "Coily or deep-shade pick, need stated"),
              ("h4", "Share of guessed buys that were\ncoily or deep-shade (%)", False,
               "Coily or deep-shade pick, agent guessed"),
              ("ask", "Share of vague requests where\nthe agent asked a question first (%)", False,
               "Asked before buying, vague request")]
    fig, axes = plt.subplots(2, 2, figsize=(FULL, 4.3), sharey=True,
                             gridspec_kw=dict(wspace=0.12, hspace=0.75))
    for ax, (pkey, xl, is_gap, title), letter in zip(axes.flat, panels, "abcd"):
        sub = d[d.panel == pkey]
        if letter in "ac":  # pre-registered Black vs White tests: H1 (a), H4 (c)
            shade(ax, RACES.index("Black"))
        if is_gap:
            zero(ax)
            ax.text(0, 0, "reference", ha="center", va="center", fontsize=7, color=GRAY["mid"],
                    bbox=dict(fc="white", ec="none", pad=0.6))
        for i, r in enumerate(RACES):
            for m in MODELS:
                row = sub[(sub.model == m) & (sub.race == r)]
                if row.empty or pd.isna(row.est.iloc[0]):
                    continue
                row = row.iloc[0]
                dot(ax, i + OFFSET[m], row.est, row.lo, row.hi, m)
        ax.set_xlabel(xl)
        ax.set_title(f"({letter}) {title}", loc="left", fontsize=8.5, pad=6,
                     x=-0.54 if letter in "ac" else 0.0)
    a, b, c, e = axes.flat
    a.set_xlim(-3, 3); a.set_xticks([-3, -2, -1, 0, 1, 2, 3]); a.xaxis.set_major_formatter(signed(0))
    b.set_xlim(-1, 1); b.set_xticks([-1, -0.5, 0, 0.5, 1]); b.xaxis.set_major_formatter(signed(1))
    for ax in (c, e):
        ax.set_xlim(40, 85) if ax is c else ax.set_xlim(40, 80)
    for ax in (a, c):
        ylabels(ax, RACES)
    # Gemini has no estimate in (b): its name means did not vary, so no gap exists (not a drawing error)
    b.text(0.97, RACES.index("Black") + 0.1, "no Gemini point:\nits names all\ngave one result",
           ha="right", va="center", fontsize=6.5, color=GRAY["mid"], style="italic")
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    h = legend_handles()
    h[2].set_label("Gemini 3.5 Flash-Lite (open: exploratory, White and\nBlack names only; no point in (b), see note there)")
    # ncol=2 fills column by column: models and the name-count note left, the lines right
    h += [Line2D([], [], ls="none", label="(20) after a group = number of names in it"),
          ci_handle("Bar: 95% interval"),
          Line2D([], [], color=GRAY["light"], lw=0.6, label="Line at 0 in (a), (b): White names (reference)"),
          Patch(facecolor=GRAY["faint"], edgecolor="none",
                label="Gray band in (a), (c): planned Black vs White test")]
    fig.subplots_adjust(bottom=0.13)
    key(fig, h, ncol=2)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
