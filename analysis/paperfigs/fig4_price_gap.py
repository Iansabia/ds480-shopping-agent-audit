"""Figure 4: confirmatory price tests H1 and H2 per model, with the dollar translation.

Dot and 95% interval whisker per test (asterisk = gap detected after correction), dotted segments for each
model's equivalence margin, short gray ticks above the row for the pre-registered detectable gap (Haiku only; none set for Luna),
and a right-hand table of the same gap in dollars. All numbers from paper/figures/fig4_price_gap.csv.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd  # noqa: E402
from paperfigs.style import *  # noqa: E402,F401,F403
from paperfigs.style import FIGDATA, FULL, MODEL, MARKER, GRAY, save, plt, signed, mstyle, key, ci_handle, dotted_handle  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.legend_handler import HandlerBase  # noqa: E402
from matplotlib.text import Text  # noqa: E402
from matplotlib.legend import Legend  # noqa: E402

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
    return f"{'−' if v < 0 else '+'}\\${abs(v):.{nd}f}"


class TextStarHandler(HandlerBase):
    """Key entry drawn as the same small text asterisk the plot uses."""

    def create_artists(self, legend, orig, xd, yd, width, height, fontsize, trans):
        t = Text(xd + width / 2, yd + height / 2, "*", ha="center", va="center",
                 fontsize=9, color=GRAY["dark"], transform=trans)
        return [t]


class StarKey(Line2D):
    """Marker-less key entry that TextStarHandler draws as a text asterisk."""


Legend.update_default_handler_map({StarKey: TextStarHandler()})


def make():
    pr = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig = plt.figure(figsize=(FULL, 2.35))
    ax = fig.add_axes([0.19, 0.27, 0.43, 0.6])

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
    ax.set_xlabel("Gap in price paid (%)\nbelow 0 = Black or women's names paid less")
    ax.text(-0.4, 1.17, "(a) Gap in percent", transform=ax.transAxes, ha="left", va="bottom", fontsize=8.5)

    # dollar table, aligned to the forest rows via the axes' y transform
    tr = ax.get_yaxis_transform()
    c1, c2 = 1.5, 1.84   # axes-fraction x positions (right edges) of the two columns
    head_y = 0.5
    ax.text(c1, head_y, "per purchase\n(95% interval)", transform=tr, ha="right", va="center", fontsize=7.5)
    ax.text(c2, head_y, "per \\$1 million\nof agent spending\n(best estimate only)", transform=tr, ha="right", va="center", fontsize=7.5)
    # panel (b) title, level with panel (a)'s title
    ax.text(1.09, 1.17, "(b) Same gap in dollars", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=8.5)
    # direction note under the table, level with panel (a)'s axis label
    ax.text(c2, min(ys) - 0.6, "\n\nminus = Black or women's\nnames paid less", transform=tr,
            ha="right", va="top", fontsize=7.5)
    for yy, r in rows:
        ax.text(c1, yy, f"{num(r.usd_per_purchase, 3)} ({num(r.usd_ci_lo, 3)}, {num(r.usd_ci_hi, 3)})",
                transform=tr, ha="right", va="center", fontsize=7.5)
        ax.text(c2, yy, usd(r.usd_per_1m), transform=tr, ha="right", va="center", fontsize=7.5)

    star = StarKey([], [], ls="none", label="Real gap (holds after correcting\nfor running several tests)")
    zero = Line2D([], [], color=GRAY["mid"], lw=0.6, label="Solid line: no gap")
    tick = Line2D([], [], ls="none", marker="|", ms=5, mew=1.0, color=GRAY["mid"],
                  label="Gray tick pair (\u00b11.4%), drawn just above the Haiku\nrows: smallest gap that test could reliably catch\n(none was set in advance for Luna)")
    key(fig, [Line2D([], [], ls="none", label="Claude Haiku 5.5", **{**mstyle("haiku"), "color": None}),
              Line2D([], [], ls="none", label="GPT-6 Luna", **{**mstyle("luna"), "color": None}),
              ci_handle("Whisker: 95% interval"), zero,
              dotted_handle("Dotted line pair: largest gap still counted as\nsmall, set in advance (Haiku within \u00b13%,\nLuna within \u00b15%)"),
              star,
              tick], ncol=2)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
