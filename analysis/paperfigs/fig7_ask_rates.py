"""Figure 7: ask rate (top row) and no-purchase rate (bottom row) by request type, model and
name group. Numbers from paper/figures/fig7_ask_rates.csv; the q value is read from
results/exploratory.json (same rule as make_figures.py: printed only where q < 0.10)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import matplotlib.pyplot as plt

from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, FULL, GRAY, MODEL_SHORT, RESULTS, panel, save
from paperfigs.grouprate_common import MODELS, band_y, draw_rows, group_legend, model_axis

NAME = "fig7_ask_rates"
ARMS = [("S0", "Clear request"), ("S1", "Clear request,\nbudget"), ("V", "Vague request"),
        ("M1S0", "Clear request,\nname-blind"), ("M1V", "Vague request,\nname-blind")]
WORD = {"asked": "ask rate", "nonpurchase": "no purchase"}


def qnotes():
    q = {}
    for e in json.load(open(RESULTS / "exploratory.json"))["tests"]:
        for a, _ in ARMS:
            for y, w in WORD.items():
                if e["test"] in (f"race: {a} {w}", f"gender: {a} {w}") and e["q_bh"] < 0.10:
                    q.setdefault((e["model"], a, y), []).append((e["test"].split(":")[0], e["q_bh"]))
    return q


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    q = qnotes()
    fig, axs = plt.subplots(2, 5, figsize=(FULL, 3.9), sharey=True)
    fig.subplots_adjust(wspace=0.2, hspace=0.55, left=0.1, right=0.995, top=0.88, bottom=0.11)
    yc = band_y(MODELS)
    for i, (y, xmax, ticks) in enumerate((("asked", 100, [0, 50, 100]), ("nonpurchase", 15, [0, 5, 10, 15]))):
        for j, (a, title) in enumerate(ARMS):
            ax = axs[i, j]
            sub = d[(d["arm"] == a) & (d["y"] == y)]
            draw_rows(ax, sub, MODELS, scale=100, ms=2.4)
            model_axis(ax, MODELS, labels=True)
            ax.set_xlim(-0.03 * xmax, xmax * 1.03)
            ax.set_xticks(ticks)
            for m in MODELS:
                if sub[sub["model"] == m].empty:
                    ax.text(xmax / 2, yc[m], "not run", ha="center", va="center", fontsize=7,
                            color=GRAY["mid"], style="italic")
                for kind, qq in q.get((m, a, y), []):
                    ax.text(xmax * 0.6, yc[m], f"{kind} gap",
                            ha="left", va="center", fontsize=7, color=GRAY["dark"])
            if i == 0:
                ax.set_title(title, fontsize=7.5, pad=3, va="bottom", linespacing=1.0)
            if j == 2:
                ax.set_xlabel("Asked the buyer first (%)" if y == "asked" else "Did not buy (%)")
        panel(axs[i, 0], "ab"[i], x=-0.3)
    group_legend(fig, y=0.945)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
