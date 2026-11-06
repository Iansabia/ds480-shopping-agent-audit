"""Figure A5 (random split check), journal style. Data: paper/figures/figA5_random_split.csv
(binned null distributions) and paper/figures/figA5_random_split.json (observed gaps)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, FULL, GRAY, panel, save, pm, plt

NAME = "figA5_random_split"
PANELS = [("H1", "Black minus White names (%)"), ("H2", "Women minus men names (%)")]


def make():
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    js = json.load(open(FIGDATA / f"{NAME}.json"))
    fig, axes = plt.subplots(1, 2, figsize=(FULL, 2.1), sharey=True)
    for k, (ax, (h, xl)) in enumerate(zip(axes, PANELS)):
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
        ax.text(real + 0.06, 10.6, f"Observed\n{pm(real, 2)}%", va="top", ha="left", fontsize=7)
        ax.set_xlim(-2.7, 2.7)
        ax.set_xticks([-2, -1, 0, 1, 2], ["−2", "−1", "0", "+1", "+2"])
        ax.set_ylim(0, 11)
        ax.set_yticks([0, 2, 4, 6, 8, 10])
        ax.set_xlabel(xl)
        panel(ax, "ab"[k], x=0.0, y=1.02)
    axes[0].set_ylabel("Share of draws (%)")
    axes[0].legend([Patch(color=GRAY["light"], lw=0), Line2D([], [], color=GRAY["dark"], lw=0.7)],
                   ["Random 20 vs 20 relabeling", "Same-group halves"], loc="upper right", bbox_to_anchor=(1.02, 1.02),
                   fontsize=7, handlelength=1.4, borderaxespad=0.1)
    fig.subplots_adjust(wspace=0.12)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
