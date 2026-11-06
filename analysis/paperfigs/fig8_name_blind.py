"""Figure 8: race gap without and with the name-blind instruction (journal style)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, FULL, MODEL, MARKER, GRAY, pm, pval, panel, save, plt, signed

NAME = "fig8_name_blind"


def make():
    df = pd.read_csv(FIGDATA / f"{NAME}.csv")
    models = ["haiku", "luna"]
    specs = [("logp", ("S0", "M1S0"), "Price paid, Black vs White names (%)"),
             ("asked", ("V", "M1V"), "Asked first, Black vs White names (points)")]
    fig, axes = plt.subplots(1, 2, figsize=(FULL, 1.55), sharey=True,
                             gridspec_kw={"wspace": 0.42})
    for k, (ax, (outc, arms, xlab)) in enumerate(zip(axes, specs)):
        d = df[df.outcome == outc]
        yt, ylab = [], []
        for i, m in enumerate(models):
            base_y = 1 - i
            for j, (arm, col, face) in enumerate([(arms[0], GRAY["light"], GRAY["light"]),
                                                   (arms[1], GRAY["dark"], GRAY["dark"])]):
                r = d[(d.model == m) & (d.arm == arm)].iloc[0]
                y = base_y + (0.13 if j == 0 else -0.13)
                ax.plot([r.lo, r.hi], [y, y], color=col, lw=0.9, solid_capstyle="butt")
                ax.plot(r.est, y, marker=MARKER[m], ms=4, mfc=face, mec=col, mew=0.9, ls="none")
            ch = d[(d.model == m) & (d.arm.str.startswith("change"))].iloc[0]
            ax.text(1.03, base_y, f"Change\n{pm(ch.est)}", transform=ax.get_yaxis_transform(),
                    ha="left", va="center", fontsize=7, color=GRAY["dark"], linespacing=1.1)
            yt.append(base_y); ylab.append(MODEL[m])
        ax.axvline(0, color=GRAY["light"], lw=0.6, zorder=0)
        ax.set_yticks(yt, ylab)
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
        ax.set_ylim(-0.5, 1.5)
        ax.set_xlim(-5, 3.5)
        ax.set_xticks([-4, -2, 0, 2])
        ax.xaxis.set_major_formatter(signed(0))
        ax.set_xlabel(xlab)
        panel(ax, "ab"[k], x=-0.02 if k else -0.36)
    h = [Line2D([], [], color=GRAY["light"], marker="o", mfc=GRAY["light"], mec=GRAY["light"], ms=4, lw=0.9,
                label="Standard prompt"),
         Line2D([], [], color=GRAY["dark"], marker="o", mfc=GRAY["dark"], ms=4, lw=0.9,
                label="With name-blind instruction")]
    fig.legend(handles=h, loc="lower center", bbox_to_anchor=(0.5, 0.98), ncol=2, handlelength=1.6,
               columnspacing=1.5, borderaxespad=0)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
