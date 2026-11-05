"""Shared drawing rules for the paper figures (Plotly).

Color means name group, the same hex in every figure. Model is shown by
panel or by marker shape, never by color. Text is always in ink colors.
The group palette is the validated categorical order from the dataviz
skill (adjacent CVD dE >= 9.1, normal-vision dE >= 19.6 on white); three
hues sit below 3:1 contrast on white, so every colored mark also carries a
visible text label (row label or direct label).

Every figure built from pilot data gets the PILOT stamp: once in the title
block and once, intact, inside every panel. Files: PNG (scale 3) and SVG for
the paper, plus an interactive HTML page with exact numbers on hover.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio

from paper_calc import MODEL_LABEL, WATERMARK, group_label

INK = "#1f1f1c"
MUTED = "#5f5e57"
FAINT = "#8a8981"
AXIS = "#b5b4ad"
GRID = "#ebeae5"
SURFACE = "#ffffff"
PANEL = "#f7f6f2"
STAMP = "#8a8981"
ALERT = "#a3261f"        # pilot banner text only (never a data color)
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
WIDTH = 900              # px; PNG export at scale 3 gives 2,700 px across
SCALE = 3
BASE = 15                # base font px (about 7.8 pt at 6.5 in print width)

GROUP_COLORS = {
    "Black woman": "#2a78d6", "Black man": "#eb6834", "White woman": "#1baf7a", "White man": "#eda100",
    "Hispanic woman": "#e87ba4", "Hispanic man": "#008300", "Asian woman": "#6250d6", "Asian man": "#e34948",
    "No name": "#8a8981",
}
MODEL_SYMBOL = {"haiku": "circle", "luna": "square", "flashlite": "diamond", "olmo": "triangle-up",
                "synth_a": "circle", "synth_b": "square"}

try:                       # dollar signs are text, never LaTeX
    pio.defaults.mathjax = None
except AttributeError:     # older plotly
    pio.kaleido.scope.mathjax = None

pio.templates["paper"] = go.layout.Template(
    layout=dict(
        font=dict(family=FONT, size=BASE, color=INK),
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
        colorway=list(GROUP_COLORS.values()),
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, linecolor=AXIS, ticks="outside", tickcolor=AXIS,
                   ticklen=4, tickfont=dict(size=BASE - 2, color=MUTED), title=dict(font=dict(size=BASE - 1, color=MUTED)),
                   automargin=False),
        yaxis=dict(showgrid=False, zeroline=False, linecolor=AXIS, ticks="", tickfont=dict(size=BASE - 2, color=INK),
                   title=dict(font=dict(size=BASE - 1, color=MUTED)), automargin=False),
        hoverlabel=dict(bgcolor="white", bordercolor=AXIS, font=dict(family=FONT, size=13, color=INK), align="left"),
        legend=dict(font=dict(size=BASE - 2), bgcolor="rgba(0,0,0,0)"),
    ))
pio.templates.default = "plotly_white+paper"


def gcolor(g):
    return GROUP_COLORS.get(g, INK)


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


def title_block(title, subtitle, pilot, width=WIDTH):
    """Takeaway title, a muted subtitle (what is compared, on which data) and,
    on pilot data, the stamp line. Returns (title dict, number of lines)."""
    t_ = wrap(title, int((width - 40) / (0.56 * (BASE + 5))))
    s_ = wrap(subtitle, int((width - 40) / (0.54 * BASE)))
    t = f"<b>{t_}</b><br><span style='font-size:{BASE}px;color:{MUTED}'>{s_}</span>"
    lines = t_.count("<br>") + 1 + s_.count("<br>") + 1
    if pilot:
        t += (f"<br><span style='font-size:{BASE - 1}px;color:{ALERT}'><b>{WATERMARK}</b>: built only to test the "
              "figure code; not a finding</span>")
        lines += 1
    return dict(text=t, x=MARGIN_X / width, xanchor="left", xref="container", y=1, yanchor="top", yref="container",
                font=dict(size=BASE + 5, color=INK), pad=dict(t=16)), lines


MARGIN_X = 18


def layout(fig, title, subtitle, pilot, height, top=None, bottom=70, left=None, right=30, width=WIDTH, gap=22):
    tb, lines = title_block(title, subtitle, pilot, width)
    top = top or (16 + 25 * lines + gap)
    fig.update_layout(title=tb, width=width, height=height,
                      margin=dict(t=top, b=bottom, l=left if left is not None else 20, r=right),
                      showlegend=fig.layout.showlegend if fig.layout.showlegend is not None else False)
    return fig


FOOT_LINE = 16


def foot_chars(width=WIDTH):
    return int((width - 2 * MARGIN_X) / (0.5 * (BASE - 3)))


def footer_margin(text, axis_px=64, width=WIDTH):
    """Bottom margin that fits the x axis plus the wrapped footer lines."""
    return axis_px + FOOT_LINE * (wrap(text, foot_chars(width)).count("<br>") + 1) + 12


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


GLYPH = {"circle": "\u25cf", "square": "\u25a0", "diamond": "\u25c6", "triangle-up": "\u25b2"}


def marker_key(models):
    """'Marker: ● Claude Haiku 5.5  ◆ Gemini 3.5 Flash-Lite' for the footer."""
    if len(models) < 2:
        return ""
    return "Marker shape = model: " + "   ".join(f"{GLYPH.get(symbol(m), '?')} {label(m)}" for m in models) + "."


def _refs(fig, row, col):
    if row is None:
        return "x", "y"
    sp = fig.get_subplot(row, col)
    return sp.xaxis.plotly_name.replace("axis", ""), sp.yaxis.plotly_name.replace("axis", "")


def vline(fig, x, row=None, col=None, **line):
    """Full-height vertical line in one panel (works before any trace exists)."""
    xr, yr = _refs(fig, row, col)
    fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=1, xref=xr, yref=f"{yr} domain", line=line, layer="below")


def hline(fig, y, row=None, col=None, **line):
    xr, yr = _refs(fig, row, col)
    fig.add_shape(type="line", y0=y, y1=y, x0=0, x1=1, yref=yr, xref=f"{xr} domain", line=line, layer="below")


def dots(fig, x, y, lo, hi, color, sym="circle", htext=None, row=None, col=None, size=11, open_=False, text=None,
         textpos="middle right", horizontal=True):
    """Dots with a 2 px 95% interval and a white ring. htext: one hover string
    per point (exact numbers)."""
    def ok(v):
        return v is not None and not (isinstance(v, float) and not math.isfinite(v))
    x, y = list(x), list(y)
    est = x if horizontal else y
    plus = [(h - e) if ok(h) and ok(e) else 0 for e, h in zip(est, hi)]
    minus = [(e - l_) if ok(l_) and ok(e) else 0 for e, l_ in zip(est, lo)]
    err = dict(type="data", array=plus, arrayminus=minus, color=color, thickness=2.2, width=0, symmetric=False,
               visible=True)
    kw = dict(x=x, y=y, mode="markers+text" if text else "markers", showlegend=False, cliponaxis=False,
              marker=dict(symbol=sym + ("-open" if open_ else ""), size=size, color=color,
                          line=dict(color=color if open_ else "white", width=2 if open_ else 1.4)))
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


def stamp(fig, skip=()):
    """One intact diagonal PILOT stamp centered in every panel (sized to the
    panel so it is never clipped), behind the data."""
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
        fs = max(9, min(34, 0.9 * wpx / (len(WATERMARK) * 0.62 * math.cos(math.radians(ang))),
                        0.9 * hpx / (len(WATERMARK) * 0.62 * math.sin(math.radians(ang)) + 1.2)))
        fig.add_annotation(text=f"<b>{WATERMARK}</b>", xref="paper", yref="paper", x=(xd[0] + xd[1]) / 2,
                           y=(yd[0] + yd[1]) / 2, showarrow=False, textangle=-ang, opacity=0.22,
                           font=dict(size=fs, color=STAMP), xanchor="center", yanchor="middle")
        done += 1
    if not done:   # a card or diagram with hidden axes: one stamp across the page
        fig.add_annotation(text=f"<b>{WATERMARK}</b>", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                           textangle=-14, opacity=0.2, font=dict(size=max(16, min(46, pw / (len(WATERMARK) * 0.66))),
                                                                 color=STAMP))


def save(fig, outdir: Path, stem: str, pilot: bool, made: list, watermark: bool = True, skip_stamp=()) -> dict:
    """PNG (scale 3) and SVG via kaleido, plus self-contained interactive HTML
    (plotly.js from the CDN). Pilot: stamp every panel and suffix _PILOT."""
    outdir.mkdir(parents=True, exist_ok=True)
    for a in fig.layout.annotations:          # a text with two "$" would be typeset as LaTeX
        if a.text and "$" in a.text:
            a.text = a.text.replace("$", "&#36;")
    for tr in fig.data:
        if getattr(tr, "text", None) is not None and not isinstance(tr.text, str):
            tr.text = [t.replace("$", "&#36;") if isinstance(t, str) else t for t in tr.text]
    if fig.layout.title.text and "$" in fig.layout.title.text:
        fig.layout.title.text = fig.layout.title.text.replace("$", "&#36;")
    if pilot and watermark:
        stamp(fig, skip_stamp)
        stem = stem + "_PILOT"
    png, svg, html = outdir / f"{stem}.png", outdir / f"{stem}.svg", outdir / f"{stem}.html"
    fig.write_image(png, scale=SCALE)
    fig.write_image(svg)
    fig.write_html(html, include_plotlyjs="cdn", full_html=True,
                   config={"displaylogo": False, "responsive": True,
                           "toImageButtonOptions": {"format": "png", "scale": SCALE, "filename": stem}})
    rec = {"png": str(png), "svg": str(svg), "html": str(html)}
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
