"""Figure A8: dollar price level by name group and gender cell, clear request (S0)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from paperfigs.style import *  # noqa

NAME = "figA8_dollars_by_cell"
CELLS = ["Black woman", "Black man", "White woman", "White man", "No name"]
LABEL = {"Black woman": "Black women", "Black man": "Black men", "White woman": "White women",
         "White man": "White men", "No name": "No name"}


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig, axes = plt.subplots(1, 2, figsize=(FULL, 2.2), sharey=True, gridspec_kw=dict(wspace=0.1))
    fig.subplots_adjust(bottom=0.3, top=0.9)
    for ax, m, letter in zip(axes, ["haiku", "luna"], "ab"):
        for i, c in enumerate(CELLS):
            r = d[(d.model == m) & (d.group == c)].iloc[0]
            col = GROUP.get(LABEL[c], GRAY["mid"])
            ax.plot([r.adj_lo, r.adj_hi], [i, i], color=col, lw=0.9, solid_capstyle="butt", zorder=2)
            ax.plot([r.adj_usd], [i], ls="none", marker=MARKER[m], ms=3.8 if m == "haiku" else 3.4,
                    mfc=col, mec=col, mew=0.8, zorder=4)
            # raw mean: tall thin tick drawn over the marker so it is never hidden
            ax.plot([r.raw_usd] * 2, [i - 0.3, i + 0.3], color=GRAY["mid"], lw=0.9,
                    solid_capstyle="butt", zorder=5)
        ax.set_title(f"{MODEL[m]}: price paid, by name group", fontsize=8.5, pad=4)
        ax.set_xlabel("Average price paid per purchase ($)\nfurther right = paid more")
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}"))
        panel(ax, letter)
    # same $3.50 span on both panels so the spreads are comparable
    axes[0].set_xlim(25.0, 28.5); axes[0].set_xticks([25, 26, 27, 28])
    axes[1].set_xlim(29.4, 32.9); axes[1].set_xticks([30, 31, 32])
    axes[0].set_yticks(range(len(CELLS)))
    axes[0].set_yticklabels([LABEL[c] for c in CELLS])
    axes[0].set_ylim(len(CELLS) - 0.5, -0.5)
    axes[0].tick_params(axis="y", length=0)
    axes[1].tick_params(axis="y", length=0)
    from matplotlib.lines import Line2D
    marks = [Line2D([], [], ls="none", label=f"{MODEL[m]}: average after evening out task mix",
                    **{**mstyle(m), "color": None}) for m in ["haiku", "luna"]]
    tick = Line2D([], [], ls="none", marker="|", ms=8, mew=0.9, color=GRAY["mid"],
                  label="Gray tick: raw average, before evening out")
    leg = key(fig, marks + [tick, ci_handle("Line: 95% interval across names")], ncol=2)
    # axis note under the key: the two panels start at different prices
    fig.canvas.draw()
    lb = leg.get_window_extent(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
    fig.text(0.5, lb.y0 - 0.01, "Colors only repeat the row label. Both price axes span $3.50 "
             "but start at different prices.", ha="center", va="top", fontsize=7.5)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
