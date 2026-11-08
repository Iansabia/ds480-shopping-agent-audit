"""Paper Figure 4: the flip chart (a further look).

For each planned model, three tested gaps from the exploratory family, Black-associated minus
White-associated names, in percentage points with the 95% interval (name-level tests, the 40 core
names; Technical Appendix B1 and B4). Numbers are read from
paper/tables/tableB2_exploratory_family.csv:
  1. asked before buying, vague requests, all 40 tasks ("race: V ask rate");
  2. hair and skin tasks, purchases made without asking: the other need's product when the buyer's
     real (hidden) need was coily hair or a deep shade ("... hidden need identity-linked");
  3. the same when the real need was fine hair or a light shade ("... hidden need other").
Luna's rows 2 and 3 point opposite ways: the name decided who got the wrong product.

Ian 11/8 (visual review rank 4 and its challenge verdict): this replaces the three-panel chart of
raw shares by name group (four groups and no name). That chart is dropped, not moved to the
appendix; paper/figures/fig6_hair_skin_fit.csv (make_figures.py) still holds its numbers.

Look: Figure 1's model order (Haiku, then Luna, as in Table 1), its filled dark dot and its bar for
both models (open markers would mean an exploratory model in style.py), so the models are told
apart by their bold block headings, each tagged "a further look". No key (Ian 11/7): rows are named
on the left, a short words column on the right says what each gap means, one zero line has
direction words under the axis, and one curved arrow joins Luna's two wrong-product rows. All text
is black, and Haiku's rows are drawn exactly like Luna's. A bar narrower than the dot gets the label
"range smaller than the dot" (none does with these numbers).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from matplotlib.textpath import TextPath  # noqa: E402
from matplotlib.transforms import blended_transform_factory as blend  # noqa: E402

from paperfigs.style import *  # noqa: E402,F401,F403
from paperfigs.style import ROOT, FULL, MODEL, GRAY, save, plt, signed  # noqa: E402

NAME = "fig6_hair_skin_fit"
SRC = ROOT / "paper" / "tables" / "tableB2_exploratory_family.csv"
MODELS = ["haiku", "luna"]  # the order of Figure 1 and Table 1

ASK = "race: V ask rate"
COILY = "race: V wrong-need pick when assumed, hidden need identity-linked"
FINE = "race: V wrong-need pick when assumed, hidden need other"
TESTS = [ASK, COILY, FINE]
LABEL = {ASK: "Asked before buying\n(all 40 tasks)",
         COILY: "Wrong product, buyer needed\ncoily hair or a deep shade",
         FINE: "Wrong product, buyer needed\nfine hair or a light shade"}
# Words column: what a clear gap means for Black-associated names, by the side it falls on.
# make() checks each gap's interval against these words before drawing.
WORDS = {(ASK, -1): "asked Black-associated names\na little less often",
         (COILY, -1): "the guess from the name fit them",
         (FINE, +1): "the guess from the name missed them"}
NO_GAP = "no clear gap"
TAG = "(a further look)"
ARROW_TEXT = "flips with the buyer's real need"
BAR_TEXT = "95% interval"
SMALL_BAR_TEXT = "range smaller than the dot"
# STIX Two Text has no arrow glyphs, so the direction words draw theirs with mathtext (STIX).
LEFT_WORDS = r"$\leftarrow$ less often for Black-associated names"
RIGHT_WORDS = r"more often $\rightarrow$"

# Figure 1 draws this one filled dot for both models (11/8). If Figure 1 goes back to the
# style.MARKER shapes (circle Haiku, square Luna), give each model its MARKER here as well.
DOT = dict(marker="o", ms=4.2, mfc=GRAY["dark"], mec=GRAY["dark"], mew=0.7)  # Figure 1's dot
BAR = dict(color=GRAY["dark"], lw=0.9, solid_capstyle="butt")                # Figure 1's bar
TEXT = dict(fontsize=7.5, color="black")                                     # row labels, words
HEAD = dict(fontsize=8.5, color="black")

# Vertical layout in inches: the y axis is drawn in inches, 0 at its top, rows going down.
# Both blocks use the same spacing, so Haiku's rows line up with Luna's.
TOP_PAD = 0.10          # above the first heading
HEAD_TO_ASK = 0.24      # heading row to the asked row
ASK_TO_COILY = 0.30
COILY_TO_FINE = 0.40    # room for the arrow and its words between the two wrong-product rows
BLOCK_GAP = 0.31        # last row of one model to the next heading
BOTTOM_PAD = 0.16       # below the last row
BOTTOM_IN = 0.66        # under the axis: tick labels, axis title, direction words
# Horizontal layout in inches across the 6.5 in figure.
LABEL_RIGHT = 1.42      # right edge of the row labels
AX_LEFT = LABEL_RIGHT + 0.08
WORDS_GAP = 0.14        # axis right edge to the words column
XLIM = (-15, 15)
XTICKS = [-15, -10, -5, 0, 5, 10, 15]


def load():
    """The six tested gaps in points, with their 95% intervals and BH q values."""
    fam = pd.read_csv(SRC)
    rows = []
    for m in MODELS:
        for t in TESTS:
            r = fam[(fam.model == m) & (fam.test == t)]
            assert len(r) == 1, (m, t)
            r = r.iloc[0]
            assert r.kind == "rate", (m, t)
            rows.append(dict(m=m, t=t, est=100 * r.est, lo=100 * r.ci_lo, hi=100 * r.ci_hi,
                             q=r.q_bh, flag=bool(r.discovery_q10)))
    return pd.DataFrame(rows)


def words_for(r):
    """'no clear gap' when the interval covers zero; otherwise the words for that side, which
    must exist (so a change in the data can never leave stale words on the figure)."""
    if r.lo <= 0 <= r.hi:
        assert not r.flag, f"{r.m} {r.t}: flagged but its interval covers zero"
        return NO_GAP
    side = 1 if r.lo > 0 else -1
    assert r.flag, f"{r.m} {r.t}: interval clears zero but the row is not flagged at q < .10"
    assert (r.t, side) in WORDS, f"{r.m} {r.t}: no words for a gap on side {side}"
    return WORDS[(r.t, side)]


def layout():
    """y (inches, negative downward) of each model heading and each row, and the axis bottom."""
    heads, ys, y = {}, {}, -TOP_PAD
    for i, m in enumerate(MODELS):
        if i:
            y -= BLOCK_GAP
        heads[m] = y
        y -= HEAD_TO_ASK
        ys[(m, ASK)] = y
        y -= ASK_TO_COILY
        ys[(m, COILY)] = y
        y -= COILY_TO_FINE
        ys[(m, FINE)] = y
    return heads, ys, y - BOTTOM_PAD


def build():
    d = load()
    heads, ys, bottom = layout()
    ax_h = -bottom
    fig_h = ax_h + BOTTOM_IN
    fig = plt.figure(figsize=(FULL, fig_h))
    # Axis width: whatever the words column leaves, measured on the real text.
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    probes = [fig.text(0, 0, w, linespacing=1.0, **TEXT) for w in list(WORDS.values()) + [NO_GAP]]
    words_w = max(p.get_window_extent(rend).width for p in probes) / fig.dpi
    for p in probes:
        p.remove()
    ax_w = FULL - AX_LEFT - WORDS_GAP - words_w - 0.06
    ax = fig.add_axes([AX_LEFT / FULL, BOTTOM_IN / fig_h, ax_w / FULL, ax_h / fig_h])
    words_x = (AX_LEFT + ax_w + WORDS_GAP) / FULL
    ax.set_xlim(*XLIM)
    ax.set_ylim(bottom, 0)
    tr = blend(fig.transFigure, ax.transData)  # x in figure fraction, y in inches down the axis
    per_unit_pt = ax_w * 72 / (XLIM[1] - XLIM[0])  # points per percentage point on the x axis

    ax.axvline(0, color=GRAY["mid"], lw=0.6, zorder=0)  # Figure 1's zero line
    for r in d.itertuples():
        y = ys[(r.m, r.t)]
        ax.plot([r.lo, r.hi], [y, y], zorder=2, **BAR)
        ax.plot(r.est, y, ls="none", zorder=3, **DOT)
        if (r.hi - r.lo) * per_unit_pt < DOT["ms"]:  # the bar hides under the dot
            ax.annotate(SMALL_BAR_TEXT, (r.est, y), xytext=(DOT["ms"] / 2 + 2.5, 0),
                        textcoords="offset points", ha="left", va="center", **TEXT)
        fig.text(LABEL_RIGHT / FULL, y, LABEL[r.t], transform=tr, ha="right", va="center",
                 linespacing=1.0, **TEXT)
        fig.text(words_x, y, words_for(r), transform=tr, ha="left", va="center", linespacing=1.0,
                 **TEXT)

    # Bold model name, then the tag in plain type, flush left on the heading row. The tag starts
    # one space after the name's ink (a text box would add the digit's wide advance after "5.5").
    bold = FontProperties(family="STIXGeneral", weight="bold", size=HEAD["fontsize"])
    for m, y in heads.items():
        fig.text(0, y, MODEL[m], transform=tr, ha="left", va="center", fontproperties=bold,
                 color=HEAD["color"])
        ink_right_pt = TextPath((0, 0), MODEL[m], prop=bold).get_extents().x1
        fig.text((ink_right_pt + 3.0) / 72 / FULL, y, TAG, transform=tr, ha="left", va="center",
                 **HEAD)

    # Name the bar once: right of the widest bar in the first block, on its own row.
    first = d[d.m == MODELS[0]]
    wide = first.loc[(first.hi - first.lo).idxmax()]
    ax.annotate(BAR_TEXT, (wide.hi, ys[(wide.m, wide.t)]), xytext=(4, 0),
                textcoords="offset points", ha="left", va="center", **TEXT)

    # The flip: an S-shaped arrow from Luna's coily-need dot down to its fine-need dot. It leaves
    # the first dot straight down and lands on the second from straight above, so it never runs
    # along either bar.
    lu = d[d.m == "luna"].set_index("t")
    x0, y0 = lu.loc[COILY, "est"], ys[("luna", COILY)]
    x3, y3 = lu.loc[FINE, "est"], ys[("luna", FINE)]
    gap = (DOT["ms"] / 2 + 2.0) / 72          # inches between a dot's edge and the arrow
    hand = (y0 - y3) * 0.42
    path = MPath([(x0, y0 - gap), (x0, y0 - gap - hand), (x3, y3 + gap + hand), (x3, y3 + gap)],
                 [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
    ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=8, lw=0.7,
                                 color="black", zorder=4))
    # Its words sit just right of the zero line, above the arrow's second half, where Luna's
    # coily-need row is empty.
    ax.text(0.8, y0 - 0.24 * (y0 - y3), ARROW_TEXT, ha="left", va="center", style="italic",
            zorder=5, **TEXT)

    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xticks(XTICKS)
    ax.xaxis.set_major_formatter(signed(0))
    ax.set_xlabel("Gap, Black-associated minus White-associated names (points)", labelpad=3)
    # Direction words under the axis title, split at the zero line.
    fig.canvas.draw()
    lab = ax.xaxis.label.get_window_extent(rend)
    yd = fig.transFigure.inverted().transform((0, lab.y0 - 2))[1]
    trd = blend(ax.transData, fig.transFigure)
    ax.annotate(LEFT_WORDS, (0, yd), xycoords=trd, xytext=(-4, 0), textcoords="offset points",
                ha="right", va="top", **TEXT)
    ax.annotate(RIGHT_WORDS, (0, yd), xycoords=trd, xytext=(4, 0), textcoords="offset points",
                ha="left", va="top", **TEXT)
    return fig, d


def make():
    fig, d = build()
    for r in d.itertuples():
        print(f"  {r.m:5s} {r.t[:62]:62s} {r.est:+6.2f} ({r.lo:+6.2f} to {r.hi:+6.2f}) q={r.q:.3f}")
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
