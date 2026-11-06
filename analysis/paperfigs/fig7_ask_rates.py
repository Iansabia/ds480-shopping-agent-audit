"""Figure 7: ask rate (top row) and no-purchase rate (bottom row) by request type, model and
name group. Numbers from paper/figures/fig7_ask_rates.csv; the q value is read from
results/exploratory.json (same rule as make_figures.py: printed only where q < 0.10).

Key (Ian 11/6): every mark is named under the figure. Shape = model (filled = main model,
open = extra model), color = name group, line = 95% interval, plus the "race gap" and
"not run" labels and what the column headings mean."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, FULL, GRAY, MODEL, RESULTS, save, mstyle
from paperfigs.grouprate_common import GCOLOR, GLABEL, GROUPS, MODELS, band_y, draw_rows, model_axis

NAME = "fig7_ask_rates"
ARMS = [("S0", "Clear request"), ("S1", "Clear request,\nwith budget"), ("V", "Vague request"),
        ("M1S0", "Clear request,\nname-blind"), ("M1V", "Vague request,\nname-blind")]
WORD = {"asked": "ask rate", "nonpurchase": "no purchase"}
ROWS = {"asked": "(a) Asked the buyer a question before buying",
        "nonpurchase": "(b) Bought nothing"}


def qnotes():
    q = {}
    for e in json.load(open(RESULTS / "exploratory.json"))["tests"]:
        for a, _ in ARMS:
            for y, w in WORD.items():
                if e["test"] in (f"race: {a} {w}", f"gender: {a} {w}") and e["q_bh"] < 0.10:
                    q.setdefault((e["model"], a, y), []).append((e["test"].split(":")[0], e["q_bh"]))
    return q


def stack_keys(fig, blocks, notes, gap_pt=4):
    """Stack titled one-row key blocks under the figure, then plain note lines; each block's top
    sits just under the previous one (measured after drawing, so nothing overlaps)."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    y = min(t.get_window_extent(r).y0 for ax in fig.axes for t in [ax.xaxis.label] if t.get_text())
    y = inv.transform((0, y))[1] - gap_pt / 72 / fig.get_figheight()
    for title, handles in blocks:
        lg = fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, y), ncol=len(handles),
                        frameon=False, handlelength=1.8, columnspacing=1.3, handletextpad=0.5,
                        title=title, title_fontsize=7.5, fontsize=7.5, borderaxespad=0.0)
        fig.canvas.draw()
        y = inv.transform((0, lg.get_window_extent(r).y0))[1] - gap_pt / 72 / fig.get_figheight()
    fig.text(0.5, y, "\n".join(notes), ha="center", va="top", fontsize=7.5, linespacing=1.4)


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    q = qnotes()
    fig, axs = plt.subplots(2, 5, figsize=(FULL, 4.5), sharey=True)
    fig.subplots_adjust(wspace=0.2, hspace=0.95, left=0.1, right=0.985, top=0.86, bottom=0.08)
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
            ax.set_title(title, fontsize=7.5, pad=3, va="bottom", linespacing=1.0)
            if j == 2:
                ax.set_xlabel("Asked the buyer first (% of requests)" if y == "asked"
                              else "Bought nothing (% of requests)")
        # row title with its panel letter, flush with the left edge of the model labels
        top = axs[i, 0].get_position().y1
        letter, words = ROWS[y].split(" ", 1)
        t = fig.text(0.005, top + 0.075, letter, ha="left", va="bottom", fontsize=8.5,
                     fontweight="bold", fontfamily="STIXGeneral")
        fig.canvas.draw()
        x1 = fig.transFigure.inverted().transform((t.get_window_extent().x1, 0))[0]
        fig.text(x1 + 0.006, top + 0.075, words, ha="left", va="bottom", fontsize=8.5)

    shapes = [Line2D([], [], ls="none", label=MODEL[m], **mstyle(m)) for m in MODELS]
    colors = [Line2D([], [], ls="none", marker="o", ms=3.6, mfc=GCOLOR[g], mec=GCOLOR[g],
                     label=GLABEL[g] if g != "No name" else "No name on the account") for g in GROUPS]
    blocks = [("Shape = model (filled = main model, open = extra model for comparison)", shapes),
              ("Color = names on the account", colors)]
    stack_keys(fig, blocks, [
        "Line through a marker = 95% interval.   name-blind = agent told to ignore the name.   "
        "not run = model not tested on this request.",
        "race gap = Black and White names got different rates, beyond chance (a further look, not a planned test)."])
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
