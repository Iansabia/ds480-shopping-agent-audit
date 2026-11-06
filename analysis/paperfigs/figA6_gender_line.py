"""Figure A6: women's-version pick on twin tasks by name gender (S0, V) and wrong-version pick
when the request names the version. Numbers from paper/figures/figA6_gender_line.csv
(pooled shares with 95% Wilson intervals)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, FULL, GRAY, MARKER, MODEL, panel, save

NAME = "figA6_gender_line"
MODELS = ["haiku", "luna", "flashlite"]
OFF = {"haiku": 0.2, "luna": 0.0, "flashlite": -0.2}
COL = {"haiku": GRAY["dark"], "luna": GRAY["dark"], "flashlite": GRAY["mid"]}
OPEN = {"flashlite"}
ROWS_AB = ["Men's names", "Gender-neutral names", "Women's names", "No-name accounts"]
LAB_AB = ["Men's names", "Gender-neutral", "Women's names", "No name"]
ROWS_C = ["Asked for men's: men's names", "Asked for men's: women's names",
          "Asked for women's: men's names", "Asked for women's: women's names"]
LAB_C = ["Men's version,\nmen's names", "Men's version,\nwomen's names*",
         "Women's version,\nmen's names*", "Women's version,\nwomen's names"]


def draw(ax, sub, rows, scale=100):
    n = len(rows)
    for i, row in enumerate(rows):
        yc = n - 1 - i
        for m in MODELS:
            r = sub[(sub["row"] == row) & (sub["model"] == m)]
            if r.empty:
                continue
            r = r.iloc[0]
            y = yc + OFF[m]
            c = COL[m]
            ax.plot([r["wilson_lo"] * scale, r["wilson_hi"] * scale], [y, y], color=c, lw=0.7,
                    solid_capstyle="butt", zorder=2)
            ax.plot(r["rate"] * scale, y, marker=MARKER[m], ms=2.8, mec=c, mew=0.7,
                    mfc="white" if m in OPEN else c, ls="none", zorder=3)
    ax.set_ylim(-0.5, n - 0.5)
    ax.set_yticks(range(n))
    ax.tick_params(axis="y", length=0)
    for k in range(1, n):
        ax.axhline(k - 0.5, color=GRAY["faint"], lw=0.5, zorder=0)


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig = plt.figure(figsize=(FULL, 1.95))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 0.5, 1], wspace=0.1, left=0.12, right=0.99,
                          top=0.86, bottom=0.21)
    axa, axb, axc = (fig.add_subplot(gs[0, k]) for k in (0, 1, 3))
    for ax, arm, letter in ((axa, "S0", "a"), (axb, "V", "b")):
        draw(ax, d[d["panel"] == arm], ROWS_AB)
        ax.set_yticklabels(LAB_AB[::-1])
        ax.set_xlim(-2, 102)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel("Women's version picked (%)")
        ax.set_title("Clear request" if arm == "S0" else "Vague request", fontsize=7.5, pad=3)
        panel(ax, letter)
    axb.set_yticklabels([])
    draw(axc, d[d["panel"] == "stated"], ROWS_C)
    axc.set_yticklabels(LAB_C[::-1], fontsize=7, linespacing=1.0)
    axc.set_xlim(-0.1, 4)
    axc.set_xticks([0, 1, 2, 3, 4])
    axc.set_xlabel("Wrong version picked (%)")
    axc.set_title("Version stated", fontsize=7.5, pad=3)
    panel(axc, "c")
    h = [Line2D([], [], marker=MARKER[m], ms=3.2, ls="-", lw=0.7, color=COL[m], mec=COL[m], mew=0.7,
                mfc="white" if m in OPEN else COL[m]) for m in MODELS]
    fig.legend(h, [MODEL[m] for m in MODELS], loc="lower center", bbox_to_anchor=(0.55, 0.93), ncol=3,
               handletextpad=0.4, handlelength=1.5, columnspacing=1.2, borderaxespad=0.0)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
