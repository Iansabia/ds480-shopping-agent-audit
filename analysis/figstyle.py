"""Shared drawing rules for the paper figures (paper/STYLE_REF.md).

One look for every figure, borrowed from the clean charts in public model
system cards: white canvas, light gridlines on the value axis only, no extra
axis lines, a left-aligned title that states the takeaway, a gray subtitle
with the method and n, direct labels instead of legends, thin dark error
bars and one highlighted series against muted gray where that fits.

Color means name group in the figures that use color, the same hex in each
of them (Ian approved these colors). Figures 3, A6 and A7 use ink markers
only, with name groups shown by position and label (PLAN D13), so color is
never the only cue for a group. The core ramp (STYLE_REF section 4) splits
names associated with Black and White buyers by hue (blue vs orange) and
spaces the five groups about 16 L* apart, so they stay apart in grayscale
print and for color-blind readers. Model is shown by panel or by marker
shape, never by color. Text is always in ink colors.

Engines (--engine in make_figures.py):
  plotly      PNG (scale 3), SVG and an interactive HTML page (default)
  matplotlib  the same figure object drawn by analysis/mpl_render.py, saved as
              <stem>_mpl.png (300 dpi) and <stem>_mpl.svg; it reads every
              position, range and font from the Plotly figure, so both
              engines give the same picture

Pilot watermark (--watermark): "corner" (default) puts a small "PILOT DATA,
NOT RESULTS" mark at the top right; "diagonal" puts a large light diagonal
stamp in every panel (or one stamp on cards). Either way the subtitle says
the figure is a pilot preview, and the file name and caption carry the
pilot label.
"""
from __future__ import annotations

import copy
import math
import re
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio

from paper_calc import MODEL_LABEL, WATERMARK, group_label

# ----------------------------------------------------------------------------- tokens (STYLE_REF section 4)

INK = "#1f1f1c"          # titles, data labels, error bars
MUTED = "#6b6a63"        # subtitles, tick labels, notes
FAINT = "#8a8983"        # pilot corner mark, quiet notes
AXIS = "#b5b4ad"         # axis lines and ticks
GRID = "#e6e5e0"         # value-axis gridlines
SURFACE = "#ffffff"
PANEL = "#f7f6f2"        # card and diagram boxes
BAND = "#efeee9"         # light band fill
MUTED_SERIES = "#c9c7be"  # context series next to the highlighted one
ACCENT = "#3365ad"       # the one highlighted series; detectable-gap ticks
STAMP = AXIS             # diagonal pilot stamp
STAMP_OPACITY = 0.2      # light enough that a dot or interval under the stamp stays readable
ALERT = ACCENT           # kept for old imports; no red text any more
FONT = "Inter, 'Source Sans 3', 'Helvetica Neue', Helvetica, Arial, sans-serif"
FONT_LIST = ["Inter", "Source Sans 3", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]
WIDTH = 900              # px; PNG export at scale 3 gives 2,700 px across
SCALE = 3
BASE = 15                # base font px
TITLE_SIZE = BASE + 7    # 22 px, weight 600
TITLE_WEIGHT = 600
SUB_SIZE = BASE          # gray subtitle

# Core name groups: STYLE_REF ramp. Exploratory groups: two more hues
# (purple, green), dark and light, kept away from the core lightness steps.
GROUP_COLORS = {
    "Black woman": "#1f3a5f", "White woman": "#9a4a1c", "Black man": "#5b8fd0", "White man": "#edb47a",
    "Hispanic woman": "#5e3f86", "Hispanic man": "#a48cc8", "Asian woman": "#2e6b4f", "Asian man": "#86bf9f",
    "No name": "#e4e2da",
}
# a very light fill needs a darker outline and interval line to be seen on white
EDGE = {"#e4e2da": "#6b6a63"}
LINEC = {"#e4e2da": "#9b9a93"}
MODEL_SYMBOL = {"haiku": "circle", "luna": "square", "flashlite": "diamond", "olmo": "triangle-up",
                "synth_a": "circle", "synth_b": "square"}

# set by make_figures.build (command-line flags)
ENGINE = "plotly"        # or "matplotlib"
WM_STYLE = "corner"      # or "diagonal"
ENGINES = ("plotly", "matplotlib")
WM_STYLES = ("corner", "diagonal")

try:                       # dollar signs are text, never LaTeX
    pio.defaults.mathjax = None
except AttributeError:     # older plotly
    pio.kaleido.scope.mathjax = None

_AX = dict(zeroline=False, showline=False, linecolor=AXIS, linewidth=1, ticks="", tickcolor=AXIS, ticklen=4,
           tickwidth=1, gridcolor=GRID, gridwidth=1, automargin=False,
           tickfont=dict(family=FONT, size=BASE - 2, color=MUTED),
           title=dict(font=dict(family=FONT, size=BASE - 1, color=MUTED)))
pio.templates["paper"] = go.layout.Template(
    layout=dict(
        font=dict(family=FONT, size=BASE, color=INK),
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        colorway=[ACCENT, MUTED_SERIES],
        # dot charts here are horizontal: the value axis is x, so the grid is on x only
        xaxis=dict(_AX, showgrid=True),
        yaxis=dict(_AX, showgrid=False, ticklabelstandoff=6, tickfont=dict(family=FONT, size=BASE - 2, color=INK)),
        bargap=0.28, bargroupgap=0.06, barmode="group",
        hoverlabel=dict(bgcolor="white", bordercolor=AXIS, font=dict(family=FONT, size=13, color=INK), align="left"),
        legend=dict(font=dict(size=BASE - 2), bgcolor="rgba(0,0,0,0)", title=dict(text="")),
        annotationdefaults=dict(font=dict(family=FONT, color=INK), showarrow=False),
        showlegend=False,
    ),
    data=dict(
        bar=[go.Bar(marker=dict(line=dict(width=0)),
                    error_y=dict(type="data", thickness=1.2, width=4, color=INK),
                    textfont=dict(family=FONT, size=BASE - 3, color=INK), cliponaxis=False)],
        scatter=[go.Scatter(cliponaxis=False, textfont=dict(family=FONT, size=BASE - 3, color=INK))],
    ))
pio.templates.default = "plotly_white+paper"


def gcolor(g):
    return GROUP_COLORS.get(g, INK)


def gline(g):
    """Line color for a group's interval or connecting line (the no-name fill is
    too light to be a line)."""
    c = gcolor(g)
    return LINEC.get(c, c)


def glabel(g, br=True):
    lab = group_label(g) if " " in g or g == "No name" else g
    if g.split()[0] in ("Hispanic", "Asian"):
        lab = f"Names associated with {g.split()[0]} {'women' if g.endswith('woman') else 'men'}"
    return lab.replace("associated with ", "associated with<br>") if br and "associated" in lab else lab


def label(m):
    return MODEL_LABEL.get(m, m)


def symbol(m):
    return MODEL_SYMBOL.get(m, "circle")


def wrap(text, chars):
    """Greedy word wrap with <br>, keeping existing <br> breaks and never
    breaking inside an HTML tag."""
    out = []
    for para in text.split("<br>"):
        line, n = "", 0
        for w in para.split(" "):
            vis = len(re.sub(r"<[^>]+>", "", w))
            if line and n + 1 + vis > chars:
                out.append(line)
                line, n = w, vis
            else:
                line, n = (line + " " + w if line else w), n + (1 if line else 0) + vis
        out.append(line)
    return "<br>".join(out)


TITLE_TOP = 28           # px above the title block; the corner mark sits in it
MARGIN_X = 18
LINE = 1.3               # Plotly line spacing (em)
PILOT_NOTE = "Pilot preview: built only to test the figure code, not a finding."


def title_block(title, subtitle, pilot, width=WIDTH):
    """Takeaway title (semibold), then a gray subtitle with the method and n and,
    on pilot data, a pilot note. Returns (title text, subtitle text, title
    lines, subtitle lines)."""
    t_ = wrap(title, int((width - 2 * MARGIN_X) / (0.56 * TITLE_SIZE)))
    s_ = wrap(subtitle, int((width - 2 * MARGIN_X) / (0.53 * SUB_SIZE)))
    if pilot:
        s_ += "<br>" + PILOT_NOTE
    return t_, s_, t_.count("<br>") + 1, s_.count("<br>") + 1


def layout(fig, title, subtitle, pilot, height, top=None, bottom=70, left=None, right=30, width=WIDTH, gap=22):
    """Title band: TITLE_TOP clear px (corner mark), the title, the gray
    subtitle, then `gap` px before the plot area. Title and subtitle are
    left-aligned annotations (Plotly's own title shifts multi-line titles
    upward), so both engines place them the same way. Margins are fixed (no
    automargin), so the matplotlib engine can place everything from the same
    numbers."""
    t_, sub, tl, sl = title_block(title, subtitle, pilot, width)
    sub_top = TITLE_TOP + LINE * TITLE_SIZE * tl + 2
    top = top or int(sub_top + LINE * SUB_SIZE * sl + gap)
    l_ = left if left is not None else 20
    fig.update_layout(title=dict(text=""), width=width, height=height,
                      margin=dict(t=top, b=bottom, l=l_, r=right),
                      showlegend=fig.layout.showlegend if fig.layout.showlegend is not None else False)
    pw, ph = width - l_ - right, height - top - bottom
    fig.add_annotation(text=t_, xref="paper", yref="paper", x=-(l_ - MARGIN_X) / pw, y=(height - TITLE_TOP - bottom) / ph,
                       xanchor="left", yanchor="top", align="left", showarrow=False, name="title",
                       font=dict(family=FONT, size=TITLE_SIZE, color=INK, weight=TITLE_WEIGHT))
    fig.add_annotation(text=sub, xref="paper", yref="paper", x=-(l_ - MARGIN_X) / pw, y=(height - sub_top - bottom) / ph,
                       xanchor="left", yanchor="top", align="left", showarrow=False, name="subtitle",
                       font=dict(family=FONT, size=SUB_SIZE, color=MUTED))
    return fig


FOOT_LINE = LINE * (BASE - 3)


def foot_chars(width=WIDTH):
    return int((width - 2 * MARGIN_X) / (0.5 * (BASE - 3)))


def footer_margin(text, axis_px=64, width=WIDTH):
    """Bottom margin that fits the x axis plus the wrapped footer lines."""
    return int(axis_px + FOOT_LINE * (wrap(text, foot_chars(width)).count("<br>") + 1) + 12)


def footer(fig, text):
    """Source, sign convention and marker key at the very bottom, flush with the
    title's left edge, in muted ink. The bottom margin must come from
    footer_margin(text)."""
    W = fig.layout.width or WIDTH
    m = fig.layout.margin
    b, l_, r = m.b or 70, m.l or 0, m.r or 0
    t = wrap(text, foot_chars(W))
    lines = t.count("<br>") + 1
    fig.add_annotation(text=t, xref="paper", yref="paper", x=-(l_ - MARGIN_X) / (W - l_ - r), y=0, yanchor="top",
                       xanchor="left", showarrow=False, align="left", font=dict(size=BASE - 3, color=MUTED),
                       yshift=-(b - FOOT_LINE * lines - 10))


GLYPH = {"circle": "●", "square": "■", "diamond": "◆", "triangle-up": "▲"}


def marker_key(models, open_note=False):
    """'Marker shape = model: ● Claude Haiku 5.5  ◆ Gemini 3.5 Flash-Lite' for the footer
    (the only place the figures name the marker key)."""
    if len(models) < 2:
        return ""
    return ("Marker shape = model: " + "   ".join(f"{GLYPH.get(symbol(m), '?')} {label(m)}" for m in models) + "."
            + ("  Open marker: exploratory model, estimate only." if open_note else ""))


def _refs(fig, row, col):
    if row is None:
        return "x", "y"
    sp = fig.get_subplot(row, col)
    return sp.xaxis.plotly_name.replace("axis", ""), sp.yaxis.plotly_name.replace("axis", "")


def vline(fig, x, row=None, col=None, layer="below", **line):
    """Full-height vertical line in one panel (works before any trace exists).
    layer "between" draws it over the gridlines, "above" over the data."""
    xr, yr = _refs(fig, row, col)
    fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=1, xref=xr, yref=f"{yr} domain", line=line, layer=layer)


def hline(fig, y, row=None, col=None, layer="below", **line):
    xr, yr = _refs(fig, row, col)
    fig.add_shape(type="line", y0=y, y1=y, x0=0, x1=1, yref=yr, xref=f"{xr} domain", line=line, layer=layer)


def dots(fig, x, y, lo, hi, color, sym="circle", htext=None, row=None, col=None, size=11, open_=False, text=None,
         textpos="middle right", horizontal=True):
    """Dots with a thin 95% interval and a white ring. htext: one hover string
    per point (exact numbers)."""
    def ok(v):
        return v is not None and not (isinstance(v, float) and not math.isfinite(v))
    x, y = list(x), list(y)
    est = x if horizontal else y
    plus = [(h - e) if ok(h) and ok(e) else 0 for e, h in zip(est, hi)]
    minus = [(e - l_) if ok(l_) and ok(e) else 0 for e, l_ in zip(est, lo)]
    lc = LINEC.get(color, color)
    edge = EDGE.get(color)
    err = dict(type="data", array=plus, arrayminus=minus, color=lc, thickness=2, width=0, symmetric=False,
               visible=True)
    if open_:
        mk = dict(symbol=sym + "-open", size=size, color=edge or color, line=dict(color=edge or color, width=2))
    else:
        mk = dict(symbol=sym, size=size, color=color, line=dict(color=edge or "white", width=1.4 if not edge else 1.2))
    kw = dict(x=x, y=y, mode="markers+text" if text else "markers", showlegend=False, cliponaxis=False, marker=mk)
    if htext is not None:
        kw.update(hovertext=htext, hovertemplate="%{hovertext}<extra></extra>")
    else:
        kw.update(hoverinfo="skip")
    if text:
        kw.update(text=text, textposition=textpos, textfont=dict(size=BASE - 3, color=INK))
    kw["error_x" if horizontal else "error_y"] = err
    tr = go.Scatter(**kw)
    if row is not None:
        fig.add_trace(tr, row=row, col=col)
    else:
        fig.add_trace(tr)


# ----------------------------------------------------------------------------- pilot watermark

def stamp_once(fig, x=0.5, y=0.5, size=40, angle=14, opacity=0.2):
    """Diagonal style, one large stamp (paper coordinates) for figures with many
    small panels or for cards, where a stamp per panel would sit on the text."""
    fig.add_annotation(text=f"<b>{WATERMARK}</b>", xref="paper", yref="paper", x=x, y=y, showarrow=False,
                       textangle=-angle, opacity=min(1.0, opacity * 1.6), font=dict(size=size, color=STAMP),
                       xanchor="center", yanchor="middle", name="pilot-stamp")


def stamp(fig, skip=()):
    """Diagonal style: one intact light PILOT stamp centered in every panel
    (sized to the panel so it is never clipped), drawn in a very light gray so
    the data stays readable."""
    W = fig.layout.width or WIDTH
    H = fig.layout.height or 500
    m = fig.layout.margin
    pw = W - (m.l or 0) - (m.r or 0)
    ph = H - (m.t or 0) - (m.b or 0)
    keys = [k for k in fig.layout.to_plotly_json() if k.startswith("xaxis") and k not in skip]
    done = 0
    for k in keys:
        ax = fig.layout[k]
        if ax.visible is False:
            continue
        yk = "yaxis" + k[5:]
        yax = fig.layout[yk] if yk in fig.layout.to_plotly_json() else None
        xd = ax.domain or (0, 1)
        yd = (yax.domain if yax is not None and yax.domain else (0, 1))
        wpx, hpx = (xd[1] - xd[0]) * pw, (yd[1] - yd[0]) * ph
        ang = 18 if wpx > 1.6 * hpx else 24
        fs = max(9, min(40, 0.9 * wpx / (len(WATERMARK) * 0.62 * math.cos(math.radians(ang))),
                        0.9 * hpx / (len(WATERMARK) * 0.62 * math.sin(math.radians(ang)) + 1.2)))
        fig.add_annotation(text=f"<b>{WATERMARK}</b>", xref="paper", yref="paper", x=(xd[0] + xd[1]) / 2,
                           y=(yd[0] + yd[1]) / 2, showarrow=False, textangle=-ang, opacity=STAMP_OPACITY,
                           font=dict(size=fs, color=STAMP), xanchor="center", yanchor="middle", name="pilot-stamp")
        done += 1
    if not done:   # a card or diagram with hidden axes: one stamp across the page
        fig.add_annotation(text=f"<b>{WATERMARK}</b>", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                           textangle=-14, opacity=0.32, font=dict(size=max(16, min(46, pw / (len(WATERMARK) * 0.66))),
                                                                  color=STAMP), name="pilot-stamp")


def corner_mark(fig):
    """Corner style: a small 'PILOT DATA, NOT RESULTS' mark at the top right,
    above the title row, so it never touches a mark or a tick label."""
    W = fig.layout.width or WIDTH
    H = fig.layout.height or 500
    m = fig.layout.margin
    l_, r, t, b = m.l or 0, m.r or 0, m.t or 0, m.b or 0
    pw, ph = W - l_ - r, H - t - b
    fig.add_annotation(text=WATERMARK, xref="paper", yref="paper", x=(W - MARGIN_X - l_) / pw, y=(H - 12 - b) / ph,
                       xanchor="right", yanchor="top", showarrow=False, opacity=0.95, name="pilot-mark",
                       font=dict(family=FONT, size=BASE - 3, color=FAINT, weight=600))


def add_watermark(fig, style=None, skip_stamp=(), single_stamp=None):
    style = style or WM_STYLE
    if style not in WM_STYLES:
        raise ValueError(f"unknown watermark style {style!r}")
    if style == "diagonal":
        if single_stamp is not None:
            stamp_once(fig, **single_stamp)
        else:
            stamp(fig, skip_stamp)
    else:
        corner_mark(fig)


# ----------------------------------------------------------------------------- export

def _escape_dollars(fig):
    for a in fig.layout.annotations:          # a text with two "$" would be typeset as LaTeX
        if a.text and "$" in a.text:
            a.text = a.text.replace("$", "&#36;")
    for tr in fig.data:
        if getattr(tr, "text", None) is not None and not isinstance(tr.text, str):
            tr.text = [t.replace("$", "&#36;") if isinstance(t, str) else t for t in tr.text]
    if fig.layout.title.text and "$" in fig.layout.title.text:   # figures that set their own layout title
        fig.layout.title.text = fig.layout.title.text.replace("$", "&#36;")


def save(fig, outdir: Path, stem: str, pilot: bool, made: list, watermark: bool = True, skip_stamp=(),
         single_stamp: dict | None = None, engine: str | None = None, wm_style: str | None = None,
         variant: str = "") -> dict:
    """Plotly: PNG (scale 3), SVG and self-contained interactive HTML (plotly.js
    from the CDN). Matplotlib: <stem>_mpl.png at 300 dpi and <stem>_mpl.svg.
    Pilot: watermark (corner or diagonal) and suffix _PILOT. The figure passed
    in is not changed, so it can be saved again in another style."""
    engine = engine or ENGINE
    if engine not in ENGINES:
        raise ValueError(f"unknown engine {engine!r}")
    fig = go.Figure(copy.deepcopy(fig.to_dict()))
    outdir.mkdir(parents=True, exist_ok=True)
    _escape_dollars(fig)
    if pilot and watermark:
        add_watermark(fig, wm_style, skip_stamp, single_stamp)
        stem = stem + "_PILOT"
    stem += variant
    if engine == "matplotlib":
        import mpl_render
        png, svg = outdir / f"{stem}_mpl.png", outdir / f"{stem}_mpl.svg"
        mpl_render.render(fig, png, svg, dpi=100 * SCALE)
        rec = {"png": str(png), "svg": str(svg), "html": None, "engine": engine}
    else:
        png, svg, html = outdir / f"{stem}.png", outdir / f"{stem}.svg", outdir / f"{stem}.html"
        fig.write_image(png, scale=SCALE)
        fig.write_image(svg)
        fig.write_html(html, include_plotlyjs="cdn", full_html=True,
                       config={"displaylogo": False, "responsive": True,
                               "toImageButtonOptions": {"format": "png", "scale": SCALE, "filename": stem}})
        rec = {"png": str(png), "svg": str(svg), "html": str(html), "engine": engine}
    made.append(rec)
    return rec


def fmt_usd(x, signed=True, cents=True):
    if x is None or x != x:
        return "n/a"
    s = "+" if (signed and x > 0) else ("-" if x < 0 else "")
    v = abs(x)
    body = f"${v:,.2f}" if cents else f"${v:,.0f}"
    return s + body


def fmt_pct(x, signed=True, nd=1):
    if x is None or x != x:
        return "n/a"
    return (f"{x:+.{nd}f}%" if signed else f"{x:.{nd}f}%")
