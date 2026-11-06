"""Figure 6: hair and skin tasks by name group (ask rate, wrong product by actual need, stated
need overridden, dollars on the wrong product). Numbers from paper/figures/fig6_hair_skin_fit.csv."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import matplotlib.pyplot as plt

from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, FULL, GRAY, MODEL, MARKER, save, mstyle, ci_handle
from paperfigs.grouprate_common import (MODELS, GROUPS, GCOLOR, GLABEL, OFFS, band_y, draw_rows,
                                        model_axis)

NAME = "fig6_hair_skin_fit"
COILY = "coily 4C or deep shade"
FINE = "fine straight or light shade"


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig, axs = plt.subplots(2, 3, figsize=(FULL, 5.1))
    fig.subplots_adjust(wspace=0.2, hspace=0.75, left=0.1, right=0.965, top=0.95, bottom=0.145)
    # (axis, panel, title (2 lines), xlabel, xmax, ticks)
    specs = [
        (axs[0, 0], "A", "(a) Asked before buying\n(vague request)",
         "% of vague requests where it\nasked the buyer first", 100, [0, 25, 50, 75, 100]),
        (axs[0, 1], "B", "(b) Wrong guess, buyer needed\ncoily-hair or deep-shade item",
         "% wrong, of buys made without\nasking (right = more wrong)", 100, [0, 25, 50, 75, 100]),
        (axs[0, 2], "C", "(c) Wrong guess, buyer needed\nfine-hair or light-shade item",
         "% wrong, of buys made without\nasking (right = more wrong)", 100, [0, 25, 50, 75, 100]),
        (axs[1, 0], "D", "(d) Ignored a stated need:\ncoily hair or deep shade",
         "% of buys that went against\nwhat the buyer said", 40, [0, 10, 20, 30, 40]),
        (axs[1, 1], "E", "(e) Ignored a stated need:\nfine hair or light shade",
         "% of buys that went against\nwhat the buyer said", 40, [0, 10, 20, 30, 40]),
    ]
    for k, (ax, p, title, xl, xmax, ticks) in enumerate(specs):
        draw_rows(ax, d[d["panel"] == p], MODELS, scale=100)
        mark_small_n(ax, d[d["panel"] == p], xmax)
        model_axis(ax, MODELS, labels=(k % 3 == 0))
        ax.set_xlim(-0.02 * xmax, xmax * 1.02)
        ax.set_xticks(ticks)
        ax.set_xlabel(xl)
        ax.set_title(title, loc="left", fontsize=8.5, x=0.0, pad=5, linespacing=1.05)

    # (f) dollars on the wrong product, rows = model x actual need (confirmatory models only)
    ax = axs[1, 2]
    pos = ax.get_position()  # make room for (f)'s own row labels so they clear panel (e)
    ax.set_position([pos.x0 + 0.075, pos.y0, pos.width - 0.075, pos.height])
    f = d[d["panel"] == "F"].copy()
    rows = [("haiku", COILY), ("haiku", FINE), ("luna", COILY), ("luna", FINE)]
    f["model_need"] = f["model"] + "|" + f["need"]
    keys = [f"{m}|{n}" for m, n in rows]
    sub = f.assign(model=f["model_need"])
    draw_rows(ax, sub, keys, scale=1 / 1000, base=lambda k: k.split("|")[0])
    model_axis(ax, keys, labels=False)
    short = {"haiku": "Haiku", "luna": "Luna"}
    ax.set_yticklabels([f"{short[m]}, needed\n{'coily or deep' if n == COILY else 'fine or light'}"
                        for m, n in rows], fontsize=7, linespacing=1.0)
    ax.set_xlim(0, 13)
    ax.set_xticks([0, 4, 8, 12])
    ax.set_xticklabels(["$0", "$4k", "$8k", "$12k"])
    ax.set_xlabel("Dollars spent on the wrong\nproduct, per 1,000 buys\nmade without asking", linespacing=1.0)
    ax.set_title("(f) Dollars spent on wrong\nguesses (Haiku, Luna only)", loc="left", fontsize=8.5,
                 x=-0.62, pad=5, linespacing=1.05)

    fig_key(fig)
    return save(fig, NAME)


SMALL_N = 10  # points resting on fewer buys than this get an "n=" tag


def mark_small_n(ax, sub, xmax):
    """Write 'n=2' beside any point that rests on fewer than SMALL_N buys, so a 0% from 2 buys
    does not read as a confident 0%."""
    yc = band_y(MODELS)
    for _, r in sub[sub["episodes"] < SMALL_N].iterrows():
        y = yc[r["model"]] + OFFS[GROUPS.index(r["group"])]
        x = max(r["est"], r["hi"] if pd.notna(r["hi"]) else r["est"]) * 100
        ax.text(x + 0.03 * xmax, y, f"n={int(r['episodes'])}", fontsize=6.5, va="center",
                ha="left", color=GCOLOR[r["group"]])


def fig_key(fig):
    """Key under the figure, one legend per row so each row is evenly spaced:
    row 1 = name-group colors, row 2 = marker shape per model, row 3 = filled vs open,
    row 4 = whisker and missing whisker, row 5 = small-n tag."""
    from matplotlib.lines import Line2D
    from matplotlib.legend_handler import HandlerTuple
    kw = dict(loc="upper center", frameon=False, handlelength=1.6, columnspacing=1.3,
              handletextpad=0.4, fontsize=7.5, borderaxespad=0.0)
    row1 = [Line2D([], [], marker="o", ms=3.4, ls="-", lw=0.7, color=GCOLOR[g], mfc=GCOLOR[g],
                   mec=GCOLOR[g], label=GLABEL[g] if g != "No name" else "No name on account")
            for g in GROUPS]
    row2 = [Line2D([], [], ls="none", label=MODEL[m], **{**mstyle(m, ms=4), "color": None})
            for m in MODELS]

    def mk(m, filled):
        c = GRAY["mid"]
        return Line2D([], [], ls="none", marker=MARKER[m], ms=4, mew=0.7, mec=c,
                      mfc=c if filled else "white")
    row3 = [(mk("haiku", True), mk("luna", True)), (mk("flashlite", False), mk("olmo", False))]
    lab3 = ["Filled: main models (Haiku, Luna), tested for name gaps",
            "Open: exploratory models, estimate only"]
    blank = Line2D([], [], ls="none")
    row4 = [ci_handle("Line: 95% interval"), blank]
    lab4 = ["Line: 95% interval", "No line: interval hidden by the marker or all zero"]
    row5 = [blank]
    lab5 = ["n=#: number of buys behind the point (shown when under 10)"]
    lab1 = ["Color = name on account: " + row1[0].get_label()] + [x.get_label() for x in row1[1:]]
    lab2 = ["Shape: " + MODEL[MODELS[0]]] + [MODEL[m] for m in MODELS[1:]]
    y, dy = 0.0, 0.034
    for i, (h, lab) in enumerate([(row1, lab1), (row2, lab2), (row3, lab3), (row4, lab4), (row5, lab5)]):
        leg = fig.legend(h, lab, ncol=len(h), bbox_to_anchor=(0.5, y - i * dy),
                         handler_map={tuple: HandlerTuple(ndivide=None, pad=0.6)}, **kw)
    return leg


if __name__ == "__main__":
    print(make())
