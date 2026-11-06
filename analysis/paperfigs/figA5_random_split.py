"""Figure A5 (random split check), journal style. Data: paper/figures/figA5_random_split.csv
(binned null distributions) and paper/figures/figA5_random_split.json (observed gaps)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, FULL, GRAY, key, patch_handle, save, pm, plt

NAME = "figA5_random_split"
PANELS = [("H1", "(a) GPT-6 Luna: Black vs White names",
           "Price gap, Black minus White names (%)\nbelow 0 = Black names paid less"),
          ("H2", "(b) GPT-6 Luna: women's vs men's names",
           "Price gap, women's minus men's names (%)\nbelow 0 = women's names paid less")]


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    js = json.load(open(FIGDATA / f"{NAME}.json"))
    fig, axes = plt.subplots(1, 2, figsize=(FULL, 2.9), sharey=True)
    for ax, (h, title, xl) in zip(axes, PANELS):
        s = d[(d.model == "luna") & (d.hypothesis == h)]
        rel = s[s.distribution == "random relabeling"]
        half = s[s.distribution == "same-group halves"]
        ax.bar(rel.bin_lo_pct, rel.share_pct, width=rel.bin_hi_pct - rel.bin_lo_pct, align="edge",
               color=GRAY["light"], lw=0)
        xs = np.r_[half.bin_lo_pct.to_numpy(), half.bin_hi_pct.iloc[-1]]
        ys = np.r_[half.share_pct.to_numpy(), half.share_pct.iloc[-1]]
        ax.step(xs, ys, where="post", color=GRAY["dark"], lw=0.7)
        real = js[f"luna {h}"]["real_gap_pct"]
        ax.axvline(real, color="k", lw=1.1)
        ax.text(real + 0.06, 10.6, f"Real gap\n{pm(real, 2)}%", va="top", ha="left", fontsize=7)
        ax.set_xlim(-2.7, 2.7)
        ax.set_xticks([-2, -1, 0, 1, 2], ["−2", "−1", "0", "+1", "+2"])
        ax.set_ylim(0, 11)
        ax.set_yticks([0, 2, 4, 6, 8, 10])
        ax.set_xlabel(xl)
        ax.set_title(title, loc="left", fontsize=8.5, pad=6)
    axes[0].set_ylabel("Share of random splits (%)")
    fig.subplots_adjust(wspace=0.12, bottom=0.25, top=0.9)
    key(fig, [patch_handle(GRAY["light"], "Gray bars: all 40 names shuffled into two random groups of 20 (10,000 shuffles)"),
              Line2D([], [], color=GRAY["dark"], lw=0.7,
                     label="Step line: one name group split into two random halves, 10 vs 10\n(each group in turn, e.g. Black names alone, then White names alone; 2,000 splits)"),
              Line2D([], [], color="k", lw=1.1, label="Thick vertical line: real gap")], ncol=1)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
