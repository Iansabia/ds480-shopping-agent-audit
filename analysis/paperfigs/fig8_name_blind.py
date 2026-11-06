"""Figure 8: race gap without and with the name-blind instruction (journal style).

Shape = model (circle Haiku, square Luna). Light gray = standard prompt, dark = with the added
name-blind line. Bars are 95% intervals. "Change" = dark estimate minus gray estimate, in the x-axis unit.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, FULL, MODEL, MARKER, GRAY, pm, save, plt, signed, key, patch_handle

NAME = "fig8_name_blind"


def make():
    df = pd.read_csv(FIGDATA / f"{NAME}.csv")
    models = ["haiku", "luna"]
    specs = [("logp", ("S0", "M1S0"), "(a) Price paid", "%",
              "Gap in price paid, Black vs White names (%)\nleft of 0 = Black names paid less"),
             ("asked", ("V", "M1V"), "(b) Asked a question before buying", " pts",
              "Gap in share of runs that asked (percentage points, pts)\nleft of 0 = agent asked fewer questions for Black names")]
    fig, axes = plt.subplots(1, 2, figsize=(FULL, 2.05), sharey=False,
                             gridspec_kw={"wspace": 0.95})
    fig.subplots_adjust(bottom=0.33, top=0.88, left=0.16, right=0.92)
    for k, (ax, (outc, arms, title, unit, xlab)) in enumerate(zip(axes, specs)):
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
            ax.text(1.03, base_y, f"Change\n{pm(ch.est)}{unit}", transform=ax.get_yaxis_transform(),
                    ha="left", va="center", fontsize=7, color=GRAY["dark"], linespacing=1.1)
            yt.append(base_y); ylab.append(MODEL[m])
        ax.axvline(0, color=GRAY["mid"], lw=0.6, zorder=0)
        ax.set_yticks(yt, ylab)
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
        ax.set_ylim(-0.5, 1.5)
        ax.set_xlim(-5, 3.5)
        ax.set_xticks([-4, -2, 0, 2])
        ax.xaxis.set_major_formatter(signed(0))
        ax.set_xlabel(xlab)
        ax.set_title(title, loc="left", fontsize=8.5, x=-0.42, pad=6)

    def mk(marker, c, label):
        return Line2D([], [], ls="none", marker=marker, ms=4, mfc=c, mec=c, mew=0.9, label=label)
    h = [mk(MARKER["haiku"], GRAY["dark"], "Circle: Claude Haiku 5.5"),
         mk(MARKER["luna"], GRAY["dark"], "Square: GPT-6 Luna"),
         Line2D([], [], color=GRAY["dark"], lw=0.9, label="Bar (light or dark): 95% interval"),
         patch_handle(GRAY["light"], "Light gray: standard prompt"),
         patch_handle(GRAY["dark"], "Dark: told to ignore the name"),
         Line2D([], [], color=GRAY["mid"], lw=0.6, label="Solid line: no gap"),
         Line2D([], [], ls="none", label="Change = dark minus light gray (% in a, pts in b)")]
    key(fig, h, ncol=3)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
