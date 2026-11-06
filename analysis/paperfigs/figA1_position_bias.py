"""Figure A1: share of purchases by displayed position, forward vs reversed order (journal style)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter
from paperfigs.style import FIGDATA, FULL, MODEL, GRAY, panel, save, plt, key

NAME = "figA1_position_bias"
MODELS = ["haiku", "luna", "flashlite", "olmo"]


def make():
    df = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig, axes = plt.subplots(1, 4, figsize=(FULL, 1.75), gridspec_kw={"wspace": 0.38})
    style = {"forward": dict(color=GRAY["dark"], mfc=GRAY["dark"], dx=-0.12),
             "reversed": dict(color=GRAY["mid"], mfc="white", dx=0.12)}
    for k, (ax, m) in enumerate(zip(axes, MODELS)):
        d = df[df.model == m]
        for order, s in style.items():
            o = d[d.order == order].sort_values("position")
            x = o.position + s["dx"]
            ax.vlines(x, 100 * o.wilson_lo, 100 * o.wilson_hi, color=s["color"], lw=0.8)
            ax.plot(x, 100 * o.share, color=s["color"], lw=0.5, marker="o", ms=2.8,
                    mfc=s["mfc"], mec=s["color"], mew=0.8)
        ax.axhline(12.5, color=GRAY["light"], lw=0.7, ls=(0, (3, 2)), zorder=0)
        ax.set_xticks(range(1, 9))
        ax.set_xlim(0.5, 8.5)
        ax.set_ylim(0, 80 if m == "olmo" else 40)
        ax.set_title(MODEL[m] + ("\n(axis runs to 80%)" if m == "olmo" else "\n "), pad=4, fontsize=8,
                     linespacing=1.1)

        if k == 0:
            ax.set_ylabel("Share of purchases (%)")
        panel(ax, "abcd"[k], x=-0.1, y=1.06)
    fig.supxlabel("Displayed position on the results page (1 = top, 8 = bottom)", y=-0.12, fontsize=8.5)
    # Key: circles here mark product ORDER, not a model (each panel title names the model).
    from matplotlib.legend_handler import HandlerTuple
    tick = dict(ls="none", marker="|", ms=7, mew=0.9)
    h = [Line2D([], [], color=GRAY["dark"], marker="o", mfc=GRAY["dark"], ms=3.2, lw=0.5,
                label="Filled circle: products in the task's usual list order"),
         Line2D([], [], color=GRAY["mid"], marker="o", mfc="white", ms=3.2, lw=0.5,
                label="Open circle: the same products listed in reverse"),
         (Line2D([], [], color=GRAY["dark"], **tick), Line2D([], [], color=GRAY["mid"], **tick)),
         Line2D([], [], color=GRAY["light"], lw=0.7, ls=(0, (3, 2)),
                label="Dashed line: 12.5%, no preference (1 in 8 spots)")]
    labels = [h[0].get_label(), h[1].get_label(),
              "Short vertical line: 95% interval, same shade as its dot (often hidden by it)",
              h[3].get_label()]
    lg = fig.legend(h, labels, loc="upper center", ncol=2, frameon=False, handlelength=1.8,
                    columnspacing=1.4, handletextpad=0.5, fontsize=7.5, borderaxespad=0.2,
                    handler_map={tuple: HandlerTuple(ndivide=None, pad=0.6)})
    lg.set_bbox_to_anchor((0.5, -0.165), transform=fig.transFigure)
    fig.text(0.5, -0.40, "Circles here show list order, not the model; each panel title names the model.\n"
             "The two dots at each position are nudged apart left and right so both stay visible; "
             "both belong to that position.", ha="center", va="top", fontsize=7.5, linespacing=1.3)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
