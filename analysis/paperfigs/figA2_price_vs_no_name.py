"""Figure A2 (price vs the no-name buyer), journal style. Data: paper/figures/figA2_price_vs_no_name.csv;
dashed lines: results/mde.json (Haiku H1, conservative, Holm), as make_figures.py uses."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import (FIGDATA, RESULTS, FULL, MODEL, MARKER, GRAY, MCOLOR, save, plt, signed,
                             key, ci_handle)

NAME = "figA2_price_vs_no_name"
MODS = ["haiku", "luna", "flashlite", "olmo"]
CONFIRM = {"haiku", "luna"}
MCOL = {m: MCOLOR[m] for m in ("haiku", "luna", "flashlite", "olmo")}  # shared rule
GROUPS = ["Black woman", "Black man", "White woman", "White man", "Hispanic woman", "Hispanic man",
          "Asian woman", "Asian man"]
ARMS = [("S0", "Clear request"), ("S1", "Clear request with a budget"), ("V", "Vague request")]
ZERO_C, DASH_C, SEP_C = "0.3", "0.6", "0.78"  # local: zero line must stand out from the dashes
OFF = {"haiku": 0.27, "luna": 0.09, "flashlite": -0.09, "olmo": -0.27}


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    mde = json.load(open(RESULTS / "mde.json"))["models"]["haiku"]["H1"]["conservative"]["mde_holm_pct"]
    fig, axes = plt.subplots(1, 3, figsize=(FULL, 3.9), sharey=True)
    for k, (ax, (arm, title)) in enumerate(zip(axes, ARMS)):
        if arm == "S0":
            for xm in (-mde, mde):  # detectable gap, for scale (dashed, not shading)
                ax.axvline(xm, color=DASH_C, lw=0.7, ls=(0, (5, 2.5)), zorder=0)
        ax.axvline(0, color=ZERO_C, lw=0.9, ls=(0, (1, 1.2)), zorder=1)  # dotted, darker than the dashes
        for i, g in enumerate(GROUPS):
            y = len(GROUPS) - 1 - i
            for m in MODS:
                r = d[(d.model == m) & (d.arm == arm) & (d.group == g)]
                if r.empty:
                    continue
                r = r.iloc[0]
                yy = y + OFF[m]
                ax.plot([r.lo_pct, r.hi_pct], [yy, yy], color=MCOL[m], lw=0.7, zorder=2)
                filled = m in CONFIRM
                ax.plot(r.est_pct, yy, marker=MARKER[m], ls="", ms=3.2, mew=0.7, zorder=3,
                        color=MCOL[m], mfc=MCOL[m] if filled else "white")
        for y in [1.5, 3.5, 5.5]:
            ax.axhline(y, color=SEP_C, lw=0.6, zorder=0)
        ax.set_title(f"({'abc'[k]}) {title}", loc="left", fontsize=8.5, pad=6)
        ax.set_xlim(-8, 16)
        ax.set_xticks([-5, 0, 5, 10, 15])
        ax.xaxis.set_major_formatter(signed(0))
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axes[0].set_yticks(range(len(GROUPS)), [g.replace("woman", "women").replace("man", "men")
                                            for g in GROUPS][::-1])
    axes[0].set_ylim(-0.6, len(GROUPS) - 0.4)
    axes[0].set_ylabel("Buyer name group (the name signals race and gender)", labelpad=4)
    axes[1].set_xlabel("Price paid vs the no-name buyer (%)\n"
                       "above 0 = group paid more than the no-name buyer")
    labels = {"haiku": "Claude Haiku 5.5 (filled, dark = main model)",
              "luna": "GPT-6 Luna (filled, dark = main model)",
              "flashlite": "Gemini 3.5 Flash-Lite (open, gray = exploratory)",
              "olmo": "OLMo 3 7B (open, gray = exploratory)"}
    mh = [Line2D([], [], ls="none", label="Each marker = that group's average price gap")]
    mh += [Line2D([], [], color=MCOL[m], marker=MARKER[m], ls="none", ms=3.5, mew=0.7,
                 mfc=MCOL[m] if m in CONFIRM else "white", label=labels[m]) for m in MODS]
    mh.append(Line2D([], [], ls="none", label="Gemini and OLMo: Black and White names only, no budget arm"))
    lines = [Line2D([], [], color=MCOL["haiku"], lw=0.7, label="Dark bar: 95% interval, main model"),
             Line2D([], [], color=MCOL["flashlite"], lw=0.7, label="Gray bar: 95% interval, exploratory model"),
             Line2D([], [], color=ZERO_C, lw=0.9, ls=(0, (1, 1.2)),
                    label="Dotted line at 0: no gap (same price as no-name buyer)"),
             Line2D([], [], color=DASH_C, lw=0.7, ls=(0, (5, 2.5)),
                    label=f"Dashed, (a) only: ±{mde:.1f}%, a size reference only. The smallest\n"
                          "Black vs White gap Haiku's main test could detect, a\n"
                          "different comparison. Not a cutoff for these markers"),
             Line2D([], [], color=SEP_C, lw=0.6,
                    label="Thin solid gray line: only separates race groups")]
    h = mh + lines  # key fills by column: models left, lines right
    fig.subplots_adjust(wspace=0.18, bottom=0.16)
    key(fig, h, ncol=2)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
