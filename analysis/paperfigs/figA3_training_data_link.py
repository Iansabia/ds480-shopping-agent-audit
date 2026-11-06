"""Figure A3: OLMo name frequency in pretraining data vs price gap (journal style)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from paperfigs.style import FIGDATA, HALF, GRAY, GROUP, save, plt

NAME = "figA3_training_data_link"
GRP = {"Black woman": "Black women", "Black man": "Black men", "White woman": "White women",
       "White man": "White men"}


def make():
    df = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig, ax = plt.subplots(figsize=(HALF, 2.45))
    ax.axhline(0, color=GRAY["light"], lw=0.6, zorder=0)
    for g, lab in GRP.items():
        d = df[df.grp == g]
        c = GROUP[lab]
        n = d[~d.word_flagged.astype(bool)]
        f = d[d.word_flagged.astype(bool)]
        ax.scatter(n.log_count, n.gap_pct, s=11, color=c, lw=0, label=lab, zorder=3)
        ax.scatter(f.log_count, f.gap_pct, s=13, facecolor="white", edgecolor=c, lw=0.8, zorder=3)
    rho, p = df.spearman_rho.iloc[0], df.spearman_p.iloc[0]
    ax.text(0.03, 0.97, f"Spearman ρ = {rho:.2f}".replace("-", "−") + f", $p$ = {p:.3f}".replace("0.", "."),
            transform=ax.transAxes, ha="left", va="top", fontsize=7.5)
    ax.set_xlabel("Log count of first name in OLMo 3 pretraining data")
    ax.set_ylabel("Price vs average name (%)")
    ax.set_xlim(7.5, 19)
    ax.set_ylim(-7, 8)
    ax.set_yticks([-6, -4, -2, 0, 2, 4, 6], ["−6", "−4", "−2", "0", "+2", "+4", "+6"])
    h = [Line2D([], [], marker="o", ls="none", ms=3.4, mfc=GROUP[l], mec=GROUP[l], label=l) for l in GRP.values()]
    h.append(Line2D([], [], marker="o", ls="none", ms=3.4, mfc="white", mec=GRAY["mid"], label="Also a common word"))
    ax.legend(handles=h, loc="upper left", bbox_to_anchor=(1.02, 1.0), ncol=1, handletextpad=0.2,
              fontsize=7, labelspacing=0.25, borderaxespad=0.2)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
