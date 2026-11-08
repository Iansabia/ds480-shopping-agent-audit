"""Figure 3 in the paper: the planted-bias check as a test with a known answer, one panel.
Data: paper/figures/fig5_method_checks.csv, panel C (one row per model). Numbers are plotted as
given, after a cross-check against results/checks.json ("planted"), the file the CSV was made from.

Ian 11/8 (visual review, rank 7): one panel about a quarter page tall. For each model an open ring
marks the gap the price test should find (the planted shift x 5 / 20 on the log scale), and a filled
dot with its 95% interval bar marks what the frozen H1 test found with the planted runs swapped in.
Panels (a, b) of the 11/7 version (each planted name's price before and after) are dropped; Table A1
prints the planted shifts (-22.7% and -34.6%), and the three steps of the check are in the caption,
not in the image.

Read without a key (Ian 11/7): the row label names the model, and every mark is named once, in
words, next to it: "should find" over each ring, "found" at the left end of each bar, "no gap" at
the top of the zero line and "95% interval" under one bar. The ring is mid gray and open, the found
mark is a small dark dot, so the two stay apart in a grayscale print even where they meet (Haiku)."""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from paperfigs.style import *  # noqa: F401,F403
from paperfigs.style import FIGDATA, RESULTS, FULL, MODEL, GRAY, save, plt, signed, pm

NAME = "fig5_method_checks"
MODS = ["haiku", "luna"]  # top to bottom, the order of Figure 1 and Table 1
FOUND_TEXT = dict(fontsize=7.5, color="k")        # labels naming the found mark: tick-label size
TARGET_TEXT = dict(fontsize=7.5, color=GRAY["mid"])  # the ring's label, in the ring's gray
REF_TEXT = dict(fontsize=7, color=GRAY["mid"])     # small muted labels on reference marks (Figure 1)
RING = dict(marker="o", ms=11, mfc="none", mec=GRAY["mid"], mew=1.0, ls="none")
DOT = dict(marker="o", ms=4.5, mfc=GRAY["dark"], mec=GRAY["dark"], mew=0.7, ls="none")


def pct(x):
    """Log-scale gap to a percent gap."""
    return 100 * (math.exp(x) - 1)


def load():
    """Panel C rows, checked against results/checks.json before anything is drawn."""
    d = pd.read_csv(FIGDATA / f"{NAME}.csv")
    c = d[d.panel == "C"].set_index("model").loc[MODS]
    planted = json.loads((RESULTS / "checks.json").read_text())["planted"]
    for m in MODS:
        p, r = planted[m], c.loc[m]
        e = p["estimated"]
        assert len(p["planted_names"]) == 5 and e["n_a"] == 20 and e["n_b"] == 20, m
        assert abs(p["expected_group_gap_log"] - p["planted_shift_log"] * 5 / 20) < 1e-12, m
        for col, v in (("est_pct", e["est"]), ("ci_lo_pct", e["ci_lo"]), ("ci_hi_pct", e["ci_hi"]),
                       ("expected_pct", p["expected_group_gap_log"])):
            assert abs(r[col] - pct(v)) < 1e-6, (m, col, r[col], pct(v))
        assert p["ci_covers_expected"] and r.ci_lo_pct <= r.expected_pct <= r.ci_hi_pct, m
    return c


def note(ax, xy, offset, text, style, **kw):
    """A short direct label set `offset` points away from the data point `xy`."""
    return ax.annotate(text, xy=xy, xytext=offset, textcoords="offset points",
                       annotation_clip=False, **style, **kw)


def make():
    c = load()
    fig, ax = plt.subplots(figsize=(FULL, 1.95))
    fig.subplots_adjust(left=0.16, right=0.985, bottom=0.32, top=0.95)
    ys = {"haiku": 1, "luna": 0}
    for m in MODS:
        r, y = c.loc[m], ys[m]
        ax.plot([r.ci_lo_pct, r.ci_hi_pct], [y, y], color=GRAY["dark"], lw=1.0,
                solid_capstyle="butt", zorder=2)
        ax.plot(r.expected_pct, y, zorder=3, **RING)
        ax.plot(r.est_pct, y, zorder=4, **DOT)
        # "should find" over the ring, "found" just left of the bar's left end
        note(ax, (r.expected_pct, y), (0, 7.5), f"should find {pm(r.expected_pct)}%", TARGET_TEXT,
             ha="center", va="bottom")
        note(ax, (r.ci_lo_pct, y), (-4, 0), f"found {pm(r.est_pct)}%", FOUND_TEXT,
             ha="right", va="center")
    # the bar named once, under Luna's bar, right of its ring
    lu = c.loc["luna"]
    note(ax, ((lu.expected_pct + lu.ci_hi_pct) / 2 + 0.6, ys["luna"]), (0, -5), "95% interval",
         REF_TEXT, ha="center", va="top")
    ax.axvline(0, color=GRAY["mid"], lw=0.6, zorder=0)
    ax.text(0, 1.62, " no gap", ha="left", va="center", **REF_TEXT)
    ax.set_yticks([ys[m] for m in MODS], [MODEL[m] for m in MODS])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_ylim(-0.55, 1.75)
    ax.set_xlim(-24.5, 1.5)
    ax.set_xticks([-20, -15, -10, -5, 0])
    ax.xaxis.set_major_formatter(signed(0))
    ax.set_xlabel("Gap in price paid, Black- vs White-associated names (%)\n"
                  "left of 0 = Black-associated names paid less")
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
