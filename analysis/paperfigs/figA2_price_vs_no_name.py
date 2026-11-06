"""Figure A2 (price vs the no-name buyer), journal style. Data: paper/figures/figA2_price_vs_no_name.csv;
dashed lines: results/mde.json (Haiku H1, conservative, Holm), as make_figures.py uses."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, RESULTS, FULL, MODEL, MARKER, GRAY, MCOLOR, panel, save, plt, signed

NAME = "figA2_price_vs_no_name"
MODS = ["haiku", "luna", "flashlite", "olmo"]
CONFIRM = {"haiku", "luna"}
MCOL = {m: MCOLOR[m] for m in ("haiku", "luna", "flashlite", "olmo")}  # shared rule
GROUPS = ["Black woman", "Black man", "White woman", "White man", "Hispanic woman", "Hispanic man",
          "Asian woman", "Asian man"]
ARMS = [("S0", "Clear request"), ("S1", "Clear request, budget"), ("V", "Vague request")]
OFF = {"haiku": 0.27, "luna": 0.09, "flashlite": -0.09, "olmo": -0.27}


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    mde = json.load(open(RESULTS / "mde.json"))["models"]["haiku"]["H1"]["conservative"]["mde_holm_pct"]
    fig, axes = plt.subplots(1, 3, figsize=(FULL, 3.4), sharey=True)
    for k, (ax, (arm, title)) in enumerate(zip(axes, ARMS)):
        if arm == "S0":
            for xm in (-mde, mde):  # detectable gap, for scale (dashed, not shading)
                ax.axvline(xm, color=GRAY["mid"], lw=0.6, ls=(0, (3, 2)), zorder=0)
        ax.axvline(0, color=GRAY["mid"], lw=0.6, zorder=1)
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
            ax.axhline(y, color=GRAY["faint"], lw=0.5, zorder=0)
        ax.set_title(title, fontsize=8, pad=4)
        ax.set_xlim(-8, 16)
        ax.set_xticks([-5, 0, 5, 10, 15])
        ax.xaxis.set_major_formatter(signed(0))
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
        panel(ax, "abc"[k], x=-0.02, y=1.02)
    axes[0].set_yticks(range(len(GROUPS)), [g.replace("woman", "women").replace("man", "men")
                                            for g in GROUPS][::-1])
    axes[0].set_ylim(-0.6, len(GROUPS) - 0.4)
    axes[1].set_xlabel("Price paid vs no-name accounts (%)")
    h = [Line2D([], [], color=MCOL[m], marker=MARKER[m], ls="-", lw=0.7, ms=3.5, mew=0.7,
                mfc=MCOL[m] if m in CONFIRM else "white") for m in MODS]
    fig.subplots_adjust(wspace=0.18)
    fig.legend(h, [MODEL[m] for m in MODS], loc="lower center", ncol=4, bbox_to_anchor=(0.55, 0.96),
               handlelength=1.6, columnspacing=1.4)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
