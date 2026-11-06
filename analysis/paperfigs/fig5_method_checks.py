"""Figure 5 (method checks), journal style. Data: paper/figures/fig5_method_checks.csv and
results/checks.json (planted shift only, for the caption check). Numbers are plotted as given."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
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
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    fig = plt.figure(figsize=(FULL, 4.5))
    gs = fig.add_gridspec(2, 6, height_ratios=[1.25, 0.75], hspace=1.0, wspace=1.3,
                          bottom=0.15, top=0.93)
    axa = fig.add_subplot(gs[0, 0:2])
    axb = fig.add_subplot(gs[0, 2:4], sharey=axa)
    axe = fig.add_subplot(gs[0, 4:6])
    axc = fig.add_subplot(gs[1, 0:3])
    axd = fig.add_subplot(gs[1, 3:6], sharey=axc)

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
        ax = axc
        ax.plot([r.ci_lo_pct, r.ci_hi_pct], [y, y], color=MCOL[m], lw=0.9, zorder=2)
        ax.plot(r.est_pct, y, marker=MARKER[m], color=MCOL[m], ms=4.5, ls="", zorder=4)
        # expected diluted gap: short gray tick above the row so it never hides the estimate
        ax.plot([r.expected_pct] * 2, [y + 0.2, y + 0.45], color=GRAY["mid"], lw=1.2,
                solid_capstyle="butt", zorder=3)
    axc.axvline(0, color=GRAY["light"], lw=0.6, zorder=0)
    axc.set_yticks([1, 0], [MODEL[m] for m in MODS])
    axc.set_ylim(-0.6, 1.6)
    axc.set_xlim(-22, 3)
    axc.set_xticks([-20, -15, -10, -5, 0])
    axc.xaxis.set_major_formatter(signed(0))
    axc.set_xlabel("Price gap, Black vs White names (%)\nleft of 0 = Black names paid less")
    axc.spines["left"].set_visible(False)
    axc.tick_params(axis="y", length=0)
    title(axc, "(d) Does the main price test catch\nthe planted gap from (a, b)?", -0.42)

    # (d): best quality minus cheapest that fits
    dd = d[d.panel == "D"]
    official = json.load(open(RESULTS / "checks.json"))["arm_p"]  # Table A1 values
    rng = np.random.default_rng(0)
    for i, m in enumerate(MODS):
        v = dd[dd.model == m].pq_minus_pc_pct.to_numpy()
        y = 1 - i
        axd.scatter(v, y + rng.uniform(-0.18, 0.18, len(v)), s=5, color=GRAY["light"], lw=0,
                    zorder=2)
        axd.plot(official[m]["pct"], y, marker=MARKER[m], color=MCOL[m], ms=4.5, ls="", zorder=3)
    plt.setp(axd.get_yticklabels(), visible=False)
    axd.set_xlim(250, 400)
    axd.set_xticks([250, 300, 350, 400])
    axd.xaxis.set_major_formatter(signed(0))
    axd.set_xlabel("Extra paid for “best quality” over\n“cheapest that fits” (%)")
    axd.spines["left"].set_visible(False)
    axd.tick_params(axis="y", length=0)
    title(axd, "(e) Price follows what the buyer asked for", -0.04)

    # (e): shuffled labels, false positive rate
    e = d[d.panel == "E"]
    hyps = ["H1", "H2", "H3", "H4"]
    HLAB = {"H1": "Price, race", "H2": "Price, gender", "H3": "Need stated\nin prompt",
            "H4": "Need guessed\nfrom name"}
    for j, m in enumerate(MODS):
        s = e[e.model == m].set_index("hypothesis")
        # Haiku a little above the label's line, Luna a little below, so close values stay apart
        ys = [len(hyps) - 1 - k + (0.13 if m == "haiku" else -0.13) for k in range(len(hyps))]
        axe.plot(s.loc[hyps, "share_p_lt_05_pct"], ys, marker=MARKER[m], color=MCOL[m], ls="",
                 ms=4.0, mec="white", mew=0.4, zorder=4, label=MODEL[m])
    axe.axvline(5, color="k", ls="--", lw=0.6, ymax=4.0 / 4.5, zorder=1)
    axe.axvline(8.5, color=GRAY["mid"], lw=0.8, ymax=4.0 / 4.5, zorder=1)
    axe.text(5, 3.55, "Expected", ha="center", va="bottom", fontsize=7)
    axe.text(8.5, 3.55, "Limit", ha="center", va="bottom", fontsize=7, color=GRAY["mid"])
    axe.set_yticks(range(len(hyps)), [HLAB[h] for h in hyps[::-1]])
    axe.set_ylim(-0.5, 4.0)
    axe.set_xlim(0, 10)
    axe.set_xticks([0, 2, 4, 6, 8, 10])
    axe.set_xlabel("Tests that found a gap by chance (%)\nmust stay left of the limit")
    axe.spines["left"].set_visible(False)
    axe.tick_params(axis="y", length=0)
    title(axe, "(c) False alarms when names\nare shuffled at random", -0.62)

    # One key naming every mark (Ian 11/6).
    nomk = dict(ls="none", color=None)

    def both(**kw):
        """Two swatches side by side: circle as drawn in (a), square as drawn in (b)."""
        return (Line2D([], [], marker="o", **kw), Line2D([], [], marker="s", **kw))

    entries = [
        Line2D([], [], label="Claude Haiku 5.5", **{**mstyle("haiku"), **nomk}),
        Line2D([], [], label="GPT-6 Luna", **{**mstyle("luna"), **nomk}),
        both(color=GROUP["Black women"], lw=0.7, ms=2.5),
        both(color=GROUP["Black men"], lw=0.7, ms=2.5),
        both(color="k", ls=":", lw=1.1, ms=4),
        Line2D([], [], color="k", ls="--", lw=0.6, label="(c) Dashed: expected by chance, 5%"),
        Line2D([], [], color=GRAY["mid"], lw=0.8, label="(c) Gray line: limit, 8.5%"),
        both(ls="none", color=GRAY["dark"], ms=4.5),
        ci_handle("(d) Bar: 95% interval"),
        Line2D([], [], ls="none", marker="|", color=GRAY["mid"], ms=6, mew=1.2,
               label="(d) Gray tick: gap it should find\nonce the (a, b) runs are swapped in"),
        Line2D([], [], color=GRAY["light"], lw=0.6, label="(d) Light line: no gap"),
        Line2D([], [], ls="none", marker="o", ms=2.2, color=GRAY["light"],
               label="(e) Gray dot: one name"),
        both(ls="none", color=GRAY["dark"], ms=4.5),
    ]
    labels = [h.get_label() for h in entries[:2]] + [
        "(a, b) One Black woman's name\n(small circle in a, square in b)",
        "(a, b) One Black man's name\n(small circle in a, square in b)",
        "(a, b) Dotted line, large black circle (a)\nor square (b): average of the 5 names",
    ] + [h.get_label() for h in entries[5:7]] + [
        "(d) Large circle (Haiku) or\nsquare (Luna): measured gap",
    ] + [h.get_label() for h in entries[8:12]] + [
        "(e) Large circle (Haiku) or\nsquare (Luna): model overall",
    ]
    # Same look as style.key(), plus a tuple handler so (a) and (b) markers sit side by side.
    fig.legend(entries, labels, loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3,
               frameon=False, handlelength=2.6, columnspacing=1.4, handletextpad=0.5,
               fontsize=7.5, borderaxespad=0.2,
               handler_map={tuple: HandlerTuple(ndivide=None, pad=0.4)})
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
