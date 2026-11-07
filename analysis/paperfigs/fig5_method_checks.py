"""Figure 3 in the paper (method checks), journal style. Data: paper/figures/fig5_method_checks.csv
(panels A to C). Numbers are plotted as given."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerTuple
from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, RESULTS, FULL, MODEL, MARKER, GRAY, GROUP, save, plt, signed, mstyle, key, ci_handle

NAME = "fig5_method_checks"
MODS = ["haiku", "luna"]
MCOL = {"haiku": GRAY["dark"], "luna": GRAY["dark"]}  # shared rule: confirmatory models dark, filled
GRP = {"BW": "Black women", "BM": "Black men", "WW": "White women", "WM": "White men"}


def _planted(ax, d, m):
    d = d[(d.model == m)]
    for pid, g in d.groupby("profile_id"):
        g = g.set_index("cond")
        ax.plot([0, 1], [g.loc["S0", "pct_over_cheapest"], g.loc["PB", "pct_over_cheapest"]],
                color=GROUP[GRP[pid[:2]]], lw=0.7, marker=MARKER[m], ms=2.5, alpha=0.9)
    mean = d.groupby("cond").pct_over_cheapest.mean()
    ax.plot([0, 1], [mean["S0"], mean["PB"]], color="k", ls=":", lw=1.1, marker=MARKER[m], ms=4,
            zorder=5)
    ax.set_xlim(-0.3, 1.3)
    ax.set_xticks([0, 1], ["Normal\nprompt", "Told to buy\ncheapest"])
    ax.set_ylim(0, 70)
    ax.set_yticks(range(0, 71, 20))


def title(ax, text, x):
    """Panel letter plus a plain-words title, left aligned like Figure 1."""
    ax.set_title(text, loc="left", fontsize=8.5, x=x, pad=6, linespacing=1.1)


def make():
    """Three panels (Ian 11/6, round 2): the planted check on each model and its recovery by the
    frozen H1 test. The shuffled-label and best-quality checks are reported in Table A1 only."""
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig = plt.figure(figsize=(FULL, 2.55))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.55], wspace=0.45, bottom=0.30, top=0.86)
    axa = fig.add_subplot(gs[0, 0])
    axb = fig.add_subplot(gs[0, 1], sharey=axa)
    axc = fig.add_subplot(gs[0, 2])

    # (a), (b): planted cheapest preference
    _planted(axa, d[d.panel == "A"], "haiku")
    _planted(axb, d[d.panel == "B"], "luna")
    axa.set_ylabel("Paid above cheapest\nfitting product (%)")
    plt.setp(axb.get_yticklabels(), visible=False)
    title(axa, "(a) Haiku: 5 names told\nto buy the cheapest", -0.42)
    title(axb, "(b) Luna: the\nsame test", -0.1)

    # (c): recovery by the frozen H1 test
    c = d[d.panel == "C"].set_index("model")
    for i, m in enumerate(MODS):
        y = 1 - i
        r = c.loc[m]
        axc.plot([r.ci_lo_pct, r.ci_hi_pct], [y, y], color=MCOL[m], lw=0.9, zorder=2)
        axc.plot(r.est_pct, y, marker=MARKER[m], color=MCOL[m], ms=4.5, ls="", zorder=4)
        # expected diluted gap: short gray tick above the row so it never hides the estimate
        axc.plot([r.expected_pct] * 2, [y + 0.2, y + 0.45], color=GRAY["mid"], lw=1.2,
                 solid_capstyle="butt", zorder=3)
    axc.axvline(0, color=GRAY["light"], lw=0.6, zorder=0)
    axc.set_yticks([1, 0], ["Claude\nHaiku 5.5", "GPT-6\nLuna"])
    axc.set_ylim(-0.6, 1.6)
    axc.set_xlim(-22, 3)
    axc.set_xticks([-20, -15, -10, -5, 0])
    axc.xaxis.set_major_formatter(signed(0))
    axc.set_xlabel("Price gap, Black vs White names (%)\nleft of 0 = Black names paid less")
    axc.spines["left"].set_visible(False)
    axc.tick_params(axis="y", length=0)
    title(axc, "(c) Does the main price test catch\nthe planted gap from (a, b)?", -0.30)

    # One short key naming every mark (Ian 11/6).
    nomk = dict(ls="none", color=None)

    def both(**kw):
        """Two swatches side by side: circle as drawn in (a), square as drawn in (b)."""
        return (Line2D([], [], marker="o", **kw), Line2D([], [], marker="s", **kw))

    entries = [
        Line2D([], [], **{**mstyle("haiku"), **nomk}),
        Line2D([], [], **{**mstyle("luna"), **nomk}),
        both(color=GROUP["Black women"], lw=0.7, ms=2.5),
        both(color=GROUP["Black men"], lw=0.7, ms=2.5),
        both(color="k", ls=":", lw=1.1, ms=4),
        ci_handle("x"),
        Line2D([], [], ls="none", marker="|", color=GRAY["mid"], ms=6, mew=1.2),
        Line2D([], [], color=GRAY["light"], lw=0.6),
    ]
    labels = [
        "Claude Haiku 5.5", "GPT-6 Luna",
        "(a, b) One Black woman's name", "(a, b) One Black man's name",
        "(a, b) Dotted: average of the 5 names", "(c) Bar: 95% interval",
        "(c) Gray tick: gap it should find", "(c) Light line: no gap",
    ]
    fig.legend(entries, labels, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3,
               frameon=False, handlelength=2.6, columnspacing=1.2, handletextpad=0.5,
               fontsize=7.5, borderaxespad=0.2,
               handler_map={tuple: HandlerTuple(ndivide=None, pad=0.4)})
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
