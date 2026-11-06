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
    panels = [("price gap vs White (%)", "Price gap vs White names (%)", True),
              ("h3 gap vs White (points)", "Pick gap vs White names (points)", True),
              ("h4", "Identity-linked pick when guessing (%)", False),
              ("ask", "Asked a question (%)", False)]
    fig, axes = plt.subplots(2, 2, figsize=(FULL, 4.3), sharey=True,
                             gridspec_kw=dict(wspace=0.12, hspace=0.42))
    for ax, (key, xl, is_gap), letter in zip(axes.flat, panels, "abcd"):
        sub = d[d.panel == key]
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
        panel(ax, letter)
    a, b, c, e = axes.flat
    a.set_xlim(-3, 3); a.set_xticks([-3, -2, -1, 0, 1, 2, 3]); a.xaxis.set_major_formatter(signed(0))
    b.set_xlim(-1, 1); b.set_xticks([-1, -0.5, 0, 0.5, 1]); b.xaxis.set_major_formatter(signed(1))
    for ax in (c, e):
        ax.set_xlim(40, 85) if ax is c else ax.set_xlim(40, 80)
    for ax in (a, c):
        ylabels(ax, RACES)
    fig.subplots_adjust(top=0.925)
    fig.legend(handles=legend_handles(), loc="lower center", ncol=3, bbox_to_anchor=(0.55, 0.955),
               handlelength=1.6, columnspacing=1.5)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
