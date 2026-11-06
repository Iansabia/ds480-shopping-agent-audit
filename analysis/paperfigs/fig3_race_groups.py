"""Figure 3: price and identity-linked pick gaps vs White names, six name groups."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from paperfigs.style import *  # noqa
from paperfigs.race_common import RACES, MODELS, OFFSET, dot, ylabels, shade, zero, legend_handles

NAME = "fig3_race_groups"


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    races = [r for r in RACES if r != "White"]
    fig, axes = plt.subplots(1, 2, figsize=(FULL, 2.2), sharey=True,
                             gridspec_kw=dict(wspace=0.12))
    specs = [("gap_usd", "usd_lo", "usd_hi", "Price paid vs White names ($ per purchase)"),
             ("h4_gap_pts", "h4_gap_lo", "h4_gap_hi", "Coily or deep-shade pick when guessing,\nvs White names (points out of 100)")]
    for ax, (c, lo, hi, xl), letter in zip(axes, specs, "ab"):
        shade(ax, races.index("Black"))
        zero(ax)
        for i, r in enumerate(races):
            for m in MODELS:
                row = d[(d.model == m) & (d.race == r)]
                if row.empty or pd.isna(row[c].iloc[0]):
                    continue
                row = row.iloc[0]
                dot(ax, i + OFFSET[m], row[c], row[lo], row[hi], m)
        ax.set_xlabel(xl)
        panel(ax, letter)
    ylabels(axes[0], races)
    axes[0].xaxis.set_major_formatter(plt.FuncFormatter(
        lambda v, _: "0" if abs(v) < 1e-9 else f"{'−' if v < 0 else '+'}{abs(v):.2f}"))
    axes[0].set_xlim(-1.0, 1.0)
    axes[0].set_xticks([-1, -0.5, 0, 0.5, 1])
    axes[1].set_xlim(-6, 12)
    axes[1].set_xticks([-5, 0, 5, 10])
    axes[1].xaxis.set_major_formatter(plt.FuncFormatter(
        lambda v, _: "0" if abs(v) < 1e-9 else f"{'−' if v < 0 else '+'}{abs(v):.0f}"))
    fig.legend(handles=legend_handles(), loc="lower center", ncol=3, bbox_to_anchor=(0.55, 0.97),
               handlelength=1.6, columnspacing=1.5)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
