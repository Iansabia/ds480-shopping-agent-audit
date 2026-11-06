"""Figure A1: share of purchases by displayed position, forward vs reversed order (journal style)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import PercentFormatter
from paperfigs.style import FIGDATA, FULL, MODEL, GRAY, panel, save, plt

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
        ax.set_title(MODEL[m], pad=6, fontsize=8)

        if k == 0:
            ax.set_ylabel("Share of purchases (%)")
        panel(ax, "abcd"[k], x=-0.1, y=1.06)
    fig.supxlabel("Displayed position (1 = top of the page)", y=-0.12, fontsize=8.5)
    h = [Line2D([], [], color=GRAY["dark"], marker="o", mfc=GRAY["dark"], ms=2.8, lw=0.5, label="Forward order"),
         Line2D([], [], color=GRAY["mid"], marker="o", mfc="white", ms=2.8, lw=0.5, label="Reversed order"),
         Line2D([], [], color=GRAY["light"], lw=0.7, ls=(0, (3, 2)), label="No preference (12.5%)")]
    fig.legend(handles=h, loc="lower center", bbox_to_anchor=(0.5, 1.03), ncol=3, columnspacing=1.5,
               handlelength=1.8, borderaxespad=0)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
