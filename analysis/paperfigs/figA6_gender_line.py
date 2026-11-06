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
from paperfigs.style import FIGDATA, FULL, GRAY, MARKER, MODEL, save, key, ci_handle

NAME = "figA6_gender_line"
MODELS = ["haiku", "luna", "flashlite"]
OFF = {"haiku": 0.2, "luna": 0.0, "flashlite": -0.2}
COL = {"haiku": GRAY["dark"], "luna": GRAY["dark"], "flashlite": GRAY["mid"]}
OPEN = {"flashlite"}
ROWS_AB = ["Men's names", "Gender-neutral names", "Women's names", "No-name accounts"]
LAB_AB = ["Men's names", "Gender-neutral\nnames", "Women's names", "No-name\naccounts"]
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


def title_left(fig, ax, text):
    """Panel title '(a) ...' starting at the left edge of the panel's tick labels (as in Figure 1)."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    tb = ax.get_tightbbox(r, bbox_extra_artists=[])
    x = ax.transAxes.inverted().transform((tb.x0, 0))[0]
    ax.set_title(text, loc="left", x=x, fontsize=8.5, pad=6)


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig = plt.figure(figsize=(FULL, 2.45))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 0.55, 1], wspace=0.1, left=0.12, right=0.97,
                          top=0.88, bottom=0.31)
    axa, axb, axc = (fig.add_subplot(gs[0, k]) for k in (0, 1, 3))
    for ax, arm in ((axa, "S0"), (axb, "V")):
        draw(ax, d[d["panel"] == arm], ROWS_AB)
        ax.set_yticklabels(LAB_AB[::-1], linespacing=1.0)
        ax.set_xlim(-2, 102)
        ax.set_xticks([0, 25, 50, 75, 100])
    axb.set_yticklabels([])
    # One x label shared by (a) and (b), centred under the pair.
    axa.set_xlabel("Women's version picked (%), in (a) and (b)\n"
                   "0 = always the men's version, 100 = always the women's version", linespacing=1.3)
    axa.xaxis.set_label_coords(1.05, -0.16)
    axa.xaxis.label.set_va("top")
    draw(axc, d[d["panel"] == "stated"], ROWS_C)
    axc.set_yticklabels(LAB_C[::-1], fontsize=7, linespacing=1.0)
    axc.set_xlim(-0.1, 4)
    axc.set_xticks([0, 1, 2, 3, 4])
    axc.xaxis.set_label_coords(0.5, -0.16)
    axc.xaxis.label.set_va("top")
    axc.set_xlabel("Wrong version picked (%)\n0 = always the version asked for",
                   linespacing=1.3)
    title_left(fig, axa, "(a) Clear request, either version OK")
    title_left(fig, axb, "(b) Vague request")
    title_left(fig, axc, "(c) Request names the version")
    h = [Line2D([], [], marker=MARKER[m], ms=3.2, ls="none", color=COL[m], mec=COL[m], mew=0.7,
                mfc="white" if m in OPEN else COL[m],
                label=MODEL[m] + (" (open = exploratory)" if m in OPEN else "")) for m in MODELS]
    star = Line2D([], [], ls="none", marker="$*$", ms=4.5, color=GRAY["dark"],
                  label="* asks for the other gender's version")
    blank = Line2D([], [], ls="none", label="No triangle: Gemini not run")
    key(fig, h + [ci_handle("Bar: 95% interval"), star, blank], ncol=3)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
