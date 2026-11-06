"""Figure A3: OLMo name frequency in pretraining data vs price gap (journal style).

Key (Ian 11/6): every mark is named under the figure. Each diamond is one first name, all priced
by OLMo 3 7B, so the shape is OLMo's diamond from the paper-wide rule; color = name group
(style.GROUP); open diamond = the name is also a common English word; gray line = average name.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from paperfigs.style import FIGDATA, HALF, GRAY, GROUP, save, key, plt

NAME = "figA3_training_data_link"
GRP = {"Black woman": "Black women", "Black man": "Black men", "White woman": "White women",
       "White man": "White men"}
KEYLAB = {lab: lab.replace("women", "women's").replace(" men", " men's") + " names"
          for lab in GRP.values()}


def make():
    df = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig, ax = plt.subplots(figsize=(HALF + 0.9, 2.9))
    ax.axhline(0, color=GRAY["light"], lw=0.6, zorder=0)
    for g, lab in GRP.items():
        d = df[df.grp == g]
        c = GROUP[lab]
        n = d[~d.word_flagged.astype(bool)]
        f = d[d.word_flagged.astype(bool)]
        # filled diamonds get a thin white rim so touching names stay separate; open diamonds
        # are hollow and drawn underneath, so no filled mark is ever hidden by an open one
        ax.scatter(n.log_count, n.gap_pct, s=10, marker="D", facecolor=c, edgecolor="white",
                   lw=0.45, label=lab, zorder=4)
        ax.scatter(f.log_count, f.gap_pct, s=12, marker="D", facecolor="none", edgecolor=c,
                   lw=0.8, zorder=3)
    rho, p = df.spearman_rho.iloc[0], df.spearman_p.iloc[0]
    ax.text(0.03, 0.97,
            f"Rank correlation, all names = {rho:.2f}".replace("-", "−")
            + "\n(0 = no link; this size is likely chance, "
            + f"$p$ = {p:.3f})".replace("0.", "."),
            transform=ax.transAxes, ha="left", va="top", fontsize=7.5, linespacing=1.3)
    ax.set_title("Is a more common name in the training text priced differently?",
                 fontsize=8.5, loc="left", pad=22)
    ax.set_xlabel("How often the first name appears in OLMo 3 training text\n"
                  "(natural log of the count; right = more common name)")
    ax.set_ylabel("Price paid vs the average name (%)\nabove 0 = paid more, below 0 = paid less")
    ax.set_xlim(7.8, 18.7)
    ax.set_ylim(-6.8, 7.6)
    ax.set_yticks([-6, -4, -2, 0, 2, 4, 6], ["−6", "−4", "−2", "0", "+2", "+4", "+6"])
    # top axis: the same counts in plain numbers (labels only, same positions)
    top = ax.secondary_xaxis("top")
    cnt = [(1e4, "10 thousand"), (1e5, "100 thousand"), (1e6, "1 million"), (1e7, "10 million"),
           (1e8, "100 million")]
    top.set_xticks([math.log(v) for v, _ in cnt], [t for _, t in cnt], fontsize=6.5)
    top.set_xlabel("Times the name appears in OLMo 3 training text", fontsize=7, labelpad=2)
    h = [Line2D([], [], marker="D", ls="none", ms=3.2, mfc=GROUP[l], mec=GROUP[l], label=KEYLAB[l])
         for l in GRP.values()]
    h.append(Line2D([], [], marker="D", ls="none", ms=3.2, mfc="none", mec=GRAY["mid"],
                    mew=0.8, label="Open diamond (edge = group color): name is also a common word"))
    h.append(Line2D([], [], color=GRAY["light"], lw=0.8, label="Gray line: average name"))
    leg = key(fig, h, ncol=3, title="Each diamond = one first name, priced by OLMo 3 7B (diamond = OLMo, as in other figures)")
    leg._legend_box.align = "center"
    fig.subplots_adjust(bottom=0.215)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
