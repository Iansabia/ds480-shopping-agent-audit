"""Helpers shared by fig3_race_groups and figA7_race_groups (dot-and-whisker by name group)."""
from paperfigs.style import GRAY, MARKER, MODEL

RACES = ["White", "Black", "Hispanic", "Asian", "MENA", "South Asian"]
RACE_LABEL = {"White": "White", "Black": "Black", "Hispanic": "Hispanic", "Asian": "Asian",
              "MENA": "Arab or Middle Eastern", "South Asian": "South Asian"}
NAMES = {"White": 20, "Black": 20, "Hispanic": 12, "Asian": 12, "MENA": 10, "South Asian": 8}
MODELS = ["haiku", "luna", "flashlite"]
OFFSET = {"haiku": -0.22, "luna": 0.0, "flashlite": 0.22}


def mstyle(m):
    if m == "flashlite":
        return dict(marker=MARKER[m], mfc="white", mec=GRAY["mid"], color=GRAY["mid"], ms=3.8, mew=0.7)
    return dict(marker=MARKER[m], mfc=GRAY["dark"], mec=GRAY["dark"], color=GRAY["dark"],
                ms=3.2 if m == "luna" else 3.6, mew=0.5)


def dot(ax, y, est, lo, hi, m):
    st = mstyle(m)
    if lo == lo and hi == hi:  # not NaN
        ax.plot([lo, hi], [y, y], color=st["color"], lw=0.8, solid_capstyle="butt", zorder=2)
    ax.plot([est], [y], ls="none", zorder=3, **{k: v for k, v in st.items() if k != "color"})


def ylabels(ax, races, with_n=True):
    ax.set_yticks(range(len(races)))
    ax.set_yticklabels([f"{RACE_LABEL[r]} ({NAMES[r]})" if with_n else RACE_LABEL[r] for r in races])
    ax.set_ylim(len(races) - 0.5, -0.5)
    ax.tick_params(axis="y", length=0)


def shade(ax, row):
    ax.axhspan(row - 0.5, row + 0.5, color=GRAY["faint"], lw=0, zorder=0)


def zero(ax):
    ax.axvline(0, color=GRAY["light"], lw=0.6, zorder=1)


def legend_handles():
    import matplotlib.lines as mlines
    out = []
    for m in MODELS:
        st = mstyle(m)
        out.append(mlines.Line2D([], [], ls="-", lw=0.8, label=MODEL[m], **st))
    return out
