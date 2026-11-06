"""Figure 3: price and identity-linked pick gaps vs White names, six name groups."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from paperfigs.style import *  # noqa
from paperfigs.race_common import RACES, MODELS, OFFSET, dot, ylabels, shade, zero, legend_handles
from paperfigs.race_common import mstyle as mstyle_rc

NAME = "fig3_race_groups"


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    races = [r for r in RACES if r != "White"]
    fig, axes = plt.subplots(1, 2, figsize=(FULL, 3.0), sharey=True,
                             gridspec_kw=dict(wspace=0.12))
    specs = [("gap_usd", "usd_lo", "usd_hi",
              "Price gap vs White names\n($ per purchase)\nleft of 0 = this group paid less",
              "(a) Price paid"),
             ("h4_gap_pts", "h4_gap_lo", "h4_gap_hi",
              "Coily or deep-shade pick, gap vs White names\n(percentage points of picks)\nright of 0 = picked more for this group",
              "(b) Product picked when the shopper did not\nstate hair type or shade (agent guessed)")]
    for ax, (c, lo, hi, xl, title), letter in zip(axes, specs, "ab"):
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
        ax.set_title(title, loc="left", fontsize=8.5, pad=6)
    ylabels(axes[0], races)
    axes[0].xaxis.set_major_formatter(plt.FuncFormatter(
        lambda v, _: "0" if abs(v) < 1e-9 else f"{'−' if v < 0 else '+'}{abs(v):.2f}"))
    axes[0].set_xlim(-1.0, 1.0)
    axes[0].set_xticks([-1, -0.5, 0, 0.5, 1])
    axes[1].set_xlim(-6, 12)
    axes[1].set_xticks([-5, 0, 5, 10])
    axes[1].xaxis.set_major_formatter(plt.FuncFormatter(
        lambda v, _: "0" if abs(v) < 1e-9 else f"{'−' if v < 0 else '+'}{abs(v):.0f}"))
    # Key: every mark in the figure. Marker handles come from race_common so they match the dots.
    from matplotlib.lines import Line2D
    marks = [Line2D([], [], label=h.get_label() + (" (gray):\nexploratory; Black and White names only" if m == "flashlite" else ""),
                    ls="-", lw=0.8, **mstyle_rc(m)) for h, m in zip(legend_handles(), MODELS)]
    key(fig, marks + [
        ci_handle("Bar, black or gray:\n95% interval"),
        Line2D([], [], color=GRAY["light"], lw=0.8, label="Thin vertical line: no gap"),
        patch_handle(GRAY["faint"], "Shaded: planned\nBlack vs White test"),
        Line2D([], [], ls="none", label="(20) = number of\nnames in group"),
    ], ncol=3)
    fig.subplots_adjust(bottom=0.255)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
