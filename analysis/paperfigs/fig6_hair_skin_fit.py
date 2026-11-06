"""Figure 6: hair and skin tasks by name group (ask rate, wrong product by actual need, stated
need overridden, dollars on the wrong product). Numbers from paper/figures/fig6_hair_skin_fit.csv."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import matplotlib.pyplot as plt

from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, FULL, GRAY, MODEL, panel, save
from paperfigs.grouprate_common import MODELS, draw_rows, group_legend, model_axis

NAME = "fig6_hair_skin_fit"
COILY = "coily 4C or deep shade"
FINE = "fine straight or light shade"


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig, axs = plt.subplots(2, 3, figsize=(FULL, 4.5))
    fig.subplots_adjust(wspace=0.2, hspace=0.62, left=0.1, right=0.99, top=0.93, bottom=0.09)
    specs = [  # (axis, panel, xlabel, xmax, ticks)
        (axs[0, 0], "A", "Asked the buyer first (%)", 100, [0, 25, 50, 75, 100]),
        (axs[0, 1], "B", "Wrong product, buyer needed\ncoily hair or deep shade (%)", 100, [0, 25, 50, 75, 100]),
        (axs[0, 2], "C", "Wrong product, buyer needed\nfine hair or light shade (%)", 100, [0, 25, 50, 75, 100]),
        (axs[1, 0], "D", "Picked against stated need:\ncoily hair or deep shade (%)", 40, [0, 10, 20, 30, 40]),
        (axs[1, 1], "E", "Picked against stated need:\nfine hair or light shade (%)", 40, [0, 10, 20, 30, 40]),
    ]
    for k, (ax, p, xl, xmax, ticks) in enumerate(specs):
        draw_rows(ax, d[d["panel"] == p], MODELS, scale=100)
        model_axis(ax, MODELS, labels=(k % 3 == 0))
        ax.set_xlim(-0.02 * xmax, xmax * 1.02)
        ax.set_xticks(ticks)
        ax.set_xlabel(xl)
        panel(ax, "abcde"[k])

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
    ax.set_xlabel("Spent on wrong product,\nper 1,000 vague purchases")
    panel(ax, "f")

    group_legend(fig, y=0.965)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
