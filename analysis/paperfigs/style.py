"""Shared look for the journal-style paper figures (Ian 11/6: "make our charts how it would be
in a normal research paper").

Rules for every figure:
- Data comes only from the CSVs make_figures.py already writes (paper/figures/<name>.csv) or
  from results/ JSON; numbers never change, only the look.
- No title, subtitle, footnote or legend essay inside the image: the caption in DRAFT.md says it.
- Serif text (STIX Two, Times-like, matching the PDF body), 8 to 9 pt at print size.
- Black and grays first; one restrained palette (GROUP colors below) only where groups must be
  told apart. Thin axes, no top/right spines, light or no grid.
- Full width = 6.5 in, half width = 3.2 in. Panel letters (a), (b) in bold (STIXGeneral, which has a bold face) at the
  left edge of each panel's tick labels.
- Save vector PDF (used by the paper build) plus a 300 dpi PNG preview.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIGDATA = ROOT / "paper" / "figures"
OUT = ROOT / "paper" / "figures" / "paper"
RESULTS = ROOT / "results"

FULL, HALF = 6.5, 3.2

MODEL = {"haiku": "Claude Haiku 5.5", "luna": "GPT-6 Luna", "flashlite": "Gemini 3.5 Flash-Lite",
         "olmo": "OLMo 3 7B"}
MODEL_SHORT = {"haiku": "Haiku", "luna": "Luna", "flashlite": "Gemini", "olmo": "OLMo"}
MARKER = {"haiku": "o", "luna": "s", "flashlite": "^", "olmo": "D"}
GRAY = {"dark": "0.15", "mid": "0.45", "light": "0.75", "faint": "0.9"}
# Name groups: muted, colorblind-safe, also distinct in grayscale.
GROUP = {"Black women": "#1b3a5c", "Black men": "#5b8db8", "White women": "#8c3b1a",
         "White men": "#d9a066"}

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["STIX Two Text", "Times New Roman", "Times"],
    "mathtext.fontset": "stix", "font.size": 8.5, "axes.labelsize": 8.5, "axes.titlesize": 8.5,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5, "lines.linewidth": 0.9,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
    "legend.frameon": False, "axes.unicode_minus": True,
    "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.02, "pdf.fonttype": 42,
})


def pm(v, nd=1):
    """Signed number with a true minus sign."""
    return f"{'−' if v < 0 else '+'}{abs(v):.{nd}f}"


def signed(nd=0, suffix=""):
    """Tick formatter for gap axes: '+2', '−2', bare '0'."""
    from matplotlib.ticker import FuncFormatter
    return FuncFormatter(lambda v, _: "0" + suffix if abs(v) < 1e-9 else pm(v, nd) + suffix)


def pval(v, nd=2):
    """'.715' style p or q value (no leading zero); '< .001' below 0.001."""
    if v < 0.001:
        return "< .001"
    return f"{v:.{nd}f}".lstrip("0")


# One marker rule for every figure: shape = model; filled = confirmatory model (Haiku, Luna),
# open = exploratory model (Gemini, OLMo) shown as an estimate only.
EXPLORATORY = {"flashlite", "olmo"}
MCOLOR = {"haiku": GRAY["dark"], "luna": GRAY["dark"], "flashlite": GRAY["mid"], "olmo": GRAY["mid"]}
MSIZE = {"haiku": 3.6, "luna": 3.2, "flashlite": 3.8, "olmo": 3.2}


def mstyle(m, color=None, ms=None):
    """Line2D kwargs (marker, colors, size) for model m under the shared rule."""
    c = color or MCOLOR[m]
    return dict(marker=MARKER[m], mec=c, mfc="white" if m in EXPLORATORY else c,
                ms=ms or MSIZE[m], mew=0.7, color=c)


def model_handles(models, lw=0.8):
    """Legend handles (marker with a short whisker) for the given models, labelled with MODEL."""
    from matplotlib.lines import Line2D
    return [Line2D([], [], ls="-", lw=lw, label=MODEL[m], **mstyle(m)) for m in models]


# Keys (Ian 11/6: "each visual has some sort of identifying key"). Every mark a reader sees
# (marker shape, fill, whisker, star, dotted line, color, shading) gets one entry, so a quick
# look explains the figure without the caption. The key sits in one row under the figure.
def ci_handle(label="Line: 95% interval"):
    from matplotlib.lines import Line2D
    return Line2D([], [], color=GRAY["dark"], lw=0.9, label=label)


def star_handle(label="* real gap (survives correction)"):
    from matplotlib.lines import Line2D
    return Line2D([], [], ls="none", marker="$*$", ms=5, color=GRAY["dark"], label=label)


def dotted_handle(label, color=None):
    from matplotlib.lines import Line2D
    return Line2D([], [], ls=(0, (1, 1.5)), lw=0.8, color=color or GRAY["mid"], label=label)


def patch_handle(color, label, hatch=None, edge=None):
    from matplotlib.patches import Patch
    return Patch(facecolor=color, edgecolor=edge or color, hatch=hatch, lw=0.6, label=label)


def key(fig, handles, ncol=None, title=None):
    """One shared key row centred under the whole figure (below the x labels)."""
    return fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.0),
                      ncol=ncol or len(handles), frameon=False, handlelength=1.8,
                      columnspacing=1.4, handletextpad=0.5, title=title,
                      title_fontsize=7.5, fontsize=7.5, borderaxespad=0.2)


def panel(ax, letter, x=None, y=None):
    """Mark a panel '(a)'. Placed at save time: left edge of the panel's tick labels, just above
    the axes (or level with the panel title), so every figure uses the same position.
    x and y are accepted for old calls and ignored."""
    fig = ax.figure
    if not hasattr(fig, "_panels"):
        fig._panels = []
    fig._panels.append((ax, letter))


def _place_panels(fig):
    if not getattr(fig, "_panels", None):
        return
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    for ax, letter in fig._panels:
        tb = ax.get_tightbbox(r, bbox_extra_artists=[])
        pos = ax.get_position()
        x0 = inv.transform((tb.x0, 0))[0]
        title = ax.title.get_text()
        if title:
            tbb = ax.title.get_window_extent(r)
            yc = inv.transform((0, (tbb.y0 + tbb.y1) / 2))[1]
            fig.text(x0, yc, f"({letter})", ha="left", va="center", fontfamily="STIXGeneral",
                     fontweight="bold", fontsize=8.5)
        else:
            y = pos.y1 + 3 / 72 / fig.get_figheight()
            fig.text(x0, y, f"({letter})", ha="left", va="bottom", fontfamily="STIXGeneral",
                     fontweight="bold", fontsize=8.5)
    fig._panels = []


def save(fig, name, width=FULL):
    """Write OUT/<name>.pdf and OUT/<name>.png; return the PNG path.

    The tight crop is widened (white space, centred) to exactly `width` inches, so the paper build,
    which scales every figure to the text width, never enlarges a figure and text stays at the
    size drawn here."""
    from matplotlib.transforms import Bbox
    OUT.mkdir(parents=True, exist_ok=True)
    _place_panels(fig)
    fig.canvas.draw()
    tb = fig.get_tightbbox(fig.canvas.get_renderer())
    pad = plt.rcParams["savefig.pad_inches"]
    x0, x1, y0, y1 = tb.x0 - pad, tb.x1 + pad, tb.y0 - pad, tb.y1 + pad
    if x1 - x0 < width:
        extra = (width - (x1 - x0)) / 2
        x0, x1 = x0 - extra, x1 + extra
    elif x1 - x0 > width + 0.01:
        print(f"warning: {name} is {x1 - x0:.2f} in wide, more than {width} in")
    bb = Bbox([[x0, y0], [x1, y1]])
    fig.savefig(OUT / f"{name}.pdf", bbox_inches=bb)
    fig.savefig(OUT / f"{name}.png", bbox_inches=bb)
    plt.close(fig)
    return OUT / f"{name}.png"
