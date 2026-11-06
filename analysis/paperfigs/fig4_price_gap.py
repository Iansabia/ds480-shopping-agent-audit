"""Figure 4: confirmatory price tests H1 and H2 per model, with the dollar translation.

Dot and 95% CI whisker per test (asterisk = gap detected after Holm), dotted segments for each
model's equivalence margin, short gray ticks above the row for the pre-registered detectable gap (Haiku only),
and a right-hand table of the same gap in dollars. All numbers from paper/figures/fig4_price_gap.csv.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd  # noqa: E402
from paperfigs.style import *  # noqa: E402,F401,F403
from paperfigs.style import FIGDATA, FULL, MODEL, MARKER, GRAY, save, plt, signed, mstyle  # noqa: E402

NAME = "fig4_price_gap"
HYP = {"H1": "Black vs White names", "H2": "Women vs men"}


def usd(v):
    """Dollar string with true minus, 2 significant digits under $1, else whole dollars."""
    s = "−" if v < 0 else ""
    a = abs(v)
    if a < 1:
        nd = max(2, -int(math.floor(math.log10(a))) + 1) if a else 2
        return f"{s}\\${a:.{nd}f}"
    return f"{s}\\${a:,.0f}"


def num(v, nd):
    return f"{'−' if v < 0 else '+'}{abs(v):.{nd}f}"


def make():
    pr = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig = plt.figure(figsize=(FULL, 2.0))
    ax = fig.add_axes([0.19, 0.2, 0.43, 0.72])

    ys, labels, heads, y = [], [], [], 0.0
    rows = []
    for k, h in enumerate(("H1", "H2")):
        if k:
            y += 0.35
        heads.append((-y, HYP[h]))
        y += 0.85
        for m in ("haiku", "luna"):
            r = pr[(pr.model == m) & (pr.hypothesis == h)].iloc[0]
            rows.append((-y, r))
            ys.append(-y)
            labels.append(MODEL[m])
            y += 1

    ax.axvline(0, color=GRAY["mid"], lw=0.6, zorder=0)
    for yy, r in rows:
        mar = r.margin_log
        for xm in (100 * (math.exp(-mar) - 1), 100 * (math.exp(mar) - 1)):
            ax.plot([xm, xm], [yy - 0.45, yy + 0.45], ls=(0, (1, 1.5)), color=GRAY["mid"], lw=0.8, zorder=1)
        if pd.notna(r.mde_holm_pct):  # detectable gap: short tick just above the row, clear of the whisker
            for xm in (-r.mde_holm_pct, r.mde_holm_pct):
                ax.plot([xm, xm], [yy + 0.2, yy + 0.42], color=GRAY["mid"], lw=1.0,
                        solid_capstyle="butt", zorder=1)
        ax.plot([r.ci_pct_lo, r.ci_pct_hi], [yy, yy], color=GRAY["dark"], lw=0.9, zorder=2)
        ax.plot(r.gap_pct, yy, ls="none", zorder=3, **{**mstyle(r.model, ms=4.2), "color": None})
        if r.p_holm < 0.05:
            ax.text(r.ci_pct_hi, yy, " *", ha="left", va="center", fontsize=9, color=GRAY["dark"])

    ax.set_yticks(ys, labels)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    for yy, txt in heads:
        ax.text(-0.025, yy, txt, transform=ax.get_yaxis_transform(), ha="right", va="center",
                style="italic", fontsize=7.5)
    ticks = [-4, -2, 0, 2, 4]
    ax.set_xlim(-5.6, 5.6)
    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter(signed(0))
    ax.set_ylim(min(ys) - 0.6, 0.5)
    ax.set_xlabel("Gap in price paid (%)")

    # dollar table, aligned to the forest rows via the axes' y transform
    tr = ax.get_yaxis_transform()
    c1, c2 = 1.5, 1.84   # axes-fraction x positions (right edges) of the two columns
    head_y = 0.5
    ax.text(c1, head_y, r"\$ per purchase (range)", transform=tr, ha="right", va="center", fontsize=7.5)
    ax.text(c2, head_y, r"\$ per \$1M spent", transform=tr, ha="right", va="center", fontsize=7.5)
    for yy, r in rows:
        ax.text(c1, yy, f"{usd(r.usd_per_purchase)} ({num(r.usd_ci_lo, 2)}, {num(r.usd_ci_hi, 2)})",
                transform=tr, ha="right", va="center", fontsize=7.5)
        ax.text(c2, yy, usd(r.usd_per_1m), transform=tr, ha="right", va="center", fontsize=7.5)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
