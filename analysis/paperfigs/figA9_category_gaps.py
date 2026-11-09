"""Figure A4 in the appendix (file figA9): Luna's race price gap on each of the 40 product categories.

Added 11/8 (Ian): shows the keyboard pair in Analyze comes from the most lopsided category, and
where that category sits next to the other 39 and the planned test's overall gap.
Each dot: clear requests (S0), core names, Black-associated minus White-associated names, each
name's average log price ratio on that category, then the group means (as in the price test,
without its task, wording and order adjustment). Dashed line: Luna's planned H1 gap
(results/confirmatory.json, gap_pct).
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from paperfigs.style import FIGDATA, HALF, GRAY, GROUP, ROOT, RESULTS, save, plt

NAME = "figA9_category_gaps"


def data():
    d = pd.read_csv(ROOT / "logs" / "main_luna.outcomes.csv", low_memory=False)
    c = d[(d.arm == "S0") & (d.tier == "core") & (d.outcome == "bought") & d.race.isin(["Black", "White"])]
    by_name = c.groupby(["task_id", "race", "profile_id"]).log_price_ratio.mean().reset_index()
    g = by_name.groupby(["task_id", "race"]).log_price_ratio.mean().unstack()
    out = pd.DataFrame({"gap_pct": (g.Black - g.White).map(lambda v: (math.exp(v) - 1) * 100)})
    out = out.sort_values("gap_pct").reset_index()
    out.to_csv(FIGDATA / f"{NAME}.csv", index=False)
    return out


def make():
    df = data()
    h1 = next(r for r in json.load(open(RESULTS / "confirmatory.json"))["rows"]
              if r["model"] == "luna" and r["hypothesis"] == "H1")["gap_pct"]
    fig, ax = plt.subplots(figsize=(HALF + 0.9, 3.0))
    x = range(1, len(df) + 1)
    ax.axhline(0, color=GRAY["light"], lw=0.6, zorder=0)
    ax.axhline(h1, color=GRAY["mid"], lw=0.8, ls=(0, (3, 2)), zorder=1)
    ax.text(len(df) + 0.6, h1, f"All 40 categories\n(planned price test): {h1:.1f}%".replace("-", "−"),
            fontsize=6.5, va="center", ha="left", color=GRAY["dark"])
    ax.scatter(x, df.gap_pct, s=12, color=GROUP["Black women"], edgecolor="white", lw=0.4, zorder=3)
    k = df.index[df.task_id == "neutral_keyboard"][0]
    kx, ky = k + 1, df.gap_pct.iloc[k]
    ax.scatter([kx], [ky], s=70, facecolor="none", edgecolor=GRAY["dark"], lw=0.9, zorder=4)
    ax.annotate(f"Keyboards: {ky:.1f}%\n(the pair in Analyze)".replace("-", "−"), (kx, ky),
                xytext=(kx + 7, ky + 1.0), fontsize=6.8, va="bottom",
                arrowprops=dict(arrowstyle="-", color=GRAY["mid"], lw=0.6))
    ax.set_xlim(0, len(df) + 1)
    ax.set_xticks([1, 10, 20, 30, 40])
    ax.set_xlabel("The 40 product categories, sorted by gap")
    ax.set_ylabel("Price paid, Black-associated vs\nWhite-associated names (%)")
    lo = math.floor(df.gap_pct.min()) - 1
    hi = math.ceil(df.gap_pct.max()) + 1
    ax.set_ylim(lo, hi)
    ax.text(1, hi - 0.4, "Below 0: Black-associated names paid less", fontsize=6.5,
            color=GRAY["mid"], va="top")
    ticks = list(range(int(lo // 5 * 5), int(hi) + 1, 5))
    ax.set_yticks(ticks, [("+" if t > 0 else "") + str(t).replace("-", "−") for t in ticks])
    ax.set_title("GPT-6 Luna, clear requests: the keyboard category is the most lopsided",
                 fontsize=8.5, loc="left")
    fig.subplots_adjust(right=0.78)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
