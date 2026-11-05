"""Matplotlib engine for the paper figures (backup to Plotly).

    render(fig, "x_mpl.png", "x_mpl.svg", dpi=300)

Draws a finished Plotly figure with matplotlib so the two engines look the
same. It asks Plotly for the resolved figure (axis ranges, tick steps,
defaults) and then places every element itself on one full-page canvas whose
units are Plotly pixels, so margins, domains, anchors, shifts and font sizes
mean exactly what they mean in Plotly. The figure is W/100 by H/100 inches
at 100 dpi, so 1 Plotly px is 0.72 pt (the STYLE_REF section 7 size match),
and a 300 dpi PNG has the same pixel size as Plotly's scale-3 export.

Covered (everything make_figures.py uses): scatter (markers, lines, text,
asymmetric error bars, open, line-ns and x-thin symbols), grouped bars with
error bars, shapes (line, rect, SVG path with Q curves; below, between and
above layers; axis, domain and paper references), annotations (HTML subset:
<b>, <i>, <br>, <span style> with font-size, color and font-weight; anchors,
shifts, background, border, rotation, arrows), the title, axes (array or
automatic ticks, prefixes and suffixes, grid, zero line, axis line, titles)
and a simple legend. Hover text has no static form and is dropped.

If Plotly cannot resolve the figure (no kaleido), ranges and ticks fall back
to the data extents, which can differ slightly from the Plotly figure.
"""
from __future__ import annotations

import base64
import html
import logging
import math
import re
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as mcolors  # noqa: E402
import matplotlib.ticker  # noqa: E402,F401
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.font_manager import FontProperties, findfont  # noqa: E402
from matplotlib.patches import FancyArrowPatch, PathPatch, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from matplotlib.textpath import TextToPath  # noqa: E402
from matplotlib import font_manager  # noqa: E402

import figstyle as S  # noqa: E402

PX = 0.72                # points per Plotly px
LINE = 1.3               # Plotly line spacing (em of the element's font)
TICK_GAP_X = 1           # px between the x axis (or its ticks) and the tick labels' top
TICK_GAP_Y = 2           # px between the y axis (or its ticks) and the tick labels' right edge
TITLE_GAP = 8            # px between tick labels and the axis title
TITLE_BASELINE = 0.75    # Plotly puts a top-anchored title's first baseline 0.75 em below its top

# STYLE_REF section 7 rcParams (the parts that apply when every element is
# placed by hand): font stack, ink colors, white canvas, text kept as text in SVG.
PAPER2_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": S.FONT_LIST,
    "text.color": S.INK,
    "figure.facecolor": S.SURFACE,
    "axes.facecolor": S.SURFACE,
    "savefig.facecolor": S.SURFACE,
    "savefig.bbox": None,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "lines.solid_capstyle": "butt",
    "lines.scale_dashes": False,
    "lines.dash_capstyle": "butt",
    "axes.unicode_minus": True,
}

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)   # fallback-family chatter
_HAVE = {f.name for f in font_manager.fontManager.ttflist}
FAMILY = [f for f in S.FONT_LIST if f in _HAVE] or ["DejaVu Sans"]
PAPER2_RC["font.sans-serif"] = FAMILY

SYMBOLS = {"circle": "o", "square": "s", "diamond": "D", "triangle-up": "^", "triangle-down": "v",
           "line-ns": "|", "line-ew": "_", "x-thin": "x", "cross-thin": "+", "x": "X", "cross": "P", "star": "*"}
SYMBOL_SCALE = {"D": 0.85, "s": 0.9, "^": 1.0}


# ----------------------------------------------------------------------------- small helpers

def col(c, default=None):
    """Plotly color string (hex, rgb(), rgba(), name) to an RGBA tuple."""
    if c is None:
        return default
    if isinstance(c, str):
        s = c.strip()
        m = re.match(r"rgba?\(([^)]*)\)", s)
        if m:
            p = [float(v) for v in m.group(1).split(",")]
            return (p[0] / 255, p[1] / 255, p[2] / 255, p[3] if len(p) > 3 else 1.0)
        if s == "transparent":
            return (0, 0, 0, 0)
    return mcolors.to_rgba(c)


def al(a):
    """matplotlib's alpha overrides an rgba fill's own alpha, so pass None for opaque."""
    return None if a is None or a >= 1 else a


def visible_color(c):
    return c is not None and col(c)[3] > 0


def weight(w):
    if w is None or w == "normal":
        return 400
    if w == "bold":
        return 700
    try:
        return int(w)
    except (TypeError, ValueError):
        return 400


def dash(d, width_pt):
    """Plotly dash names to an absolute on-off pattern in points (Plotly:
    dlw = max(line width, 3) px; dot = dlw on, dlw off; dash = 3 dlw, 3 dlw)."""
    if not d or d == "solid":
        return "-"
    w = max(width_pt / PX, 3) * PX
    pat = {"dot": (w, w), "dash": (3 * w, 3 * w), "longdash": (5 * w, 5 * w), "dashdot": (3 * w, w, w, w),
           "longdashdot": (5 * w, 2 * w, w, 2 * w)}.get(d)
    if pat is None:      # "5px,10px"
        nums = [float(v) for v in re.findall(r"[\d.]+", d)]
        pat = tuple(n * PX for n in nums) or (3 * w, 3 * w)
    return (0, pat)


def arr(v):
    if v is None:
        return None
    if isinstance(v, dict) and "bdata" in v:          # Plotly typed array (base64)
        a = np.frombuffer(base64.b64decode(v["bdata"]), dtype=np.dtype(v.get("dtype", "f8")))
        return list(a.astype(float))
    if isinstance(v, (str, int, float)):
        return [v]
    return list(np.asarray(v, dtype=object).ravel())


def num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def pick(v, i, default=None):
    """Scalar or per-point value."""
    if v is None:
        return default
    if isinstance(v, (list, tuple, np.ndarray)):
        return v[i] if i < len(v) else default
    return v


# ----------------------------------------------------------------------------- rich text

def parse_html(text, base):
    """Plotly's HTML subset to lines of (text, style) runs."""
    lines = [[]]
    stack = [dict(base)]
    for tok in re.split(r"(</?[a-zA-Z][^>]*>)", str(text)):   # "< 0.05" is text, not a tag
        if not tok:
            continue
        if tok.startswith("<"):
            t = tok.lower()
            if t.startswith("<br"):
                lines.append([])
            elif t.startswith("</"):
                if len(stack) > 1:
                    stack.pop()
            elif t in ("<b>", "<strong>"):
                stack.append(dict(stack[-1], weight=700))
            elif t in ("<i>", "<em>"):
                stack.append(dict(stack[-1], style="italic"))
            elif t.startswith("<span") or t.startswith("<a"):
                st = dict(stack[-1])
                m = re.search(r"style\s*=\s*['\"]([^'\"]*)['\"]", tok)
                for decl in (m.group(1).split(";") if m else []):
                    if ":" not in decl:
                        continue
                    k, v = (x.strip() for x in decl.split(":", 1))
                    if k == "font-size":
                        st["size"] = float(re.sub(r"[^\d.]", "", v))
                    elif k == "color":
                        st["color"] = v
                    elif k == "font-weight":
                        st["weight"] = weight(v)
                    elif k == "font-style":
                        st["style"] = v
                stack.append(st)
            elif t.startswith("<sup") or t.startswith("<sub"):
                stack.append(dict(stack[-1], size=stack[-1]["size"] * 0.7))
            continue
        lines[-1].append((html.unescape(tok), dict(stack[-1])))
    return lines


class Typesetter:
    def __init__(self, fig, family):
        self.fig = fig
        self.t2p = TextToPath()
        self.family = family
        self._fp, self._w = {}, {}

    def fp(self, st):
        key = (st["size"], weight(st.get("weight")), st.get("style", "normal"))
        if key not in self._fp:
            self._fp[key] = FontProperties(family=self.family, size=st["size"] * PX, weight=key[1], style=key[2])
        return self._fp[key]

    def width(self, s, st):
        key = (s, st["size"], weight(st.get("weight")), st.get("style", "normal"))
        if key not in self._w:
            fp = self.fp(st)       # outline widths in points, no hinting; 1 pt = 100/72 canvas px
            w1 = self.t2p.get_text_width_height_descent("|" + s + "|", fp, ismath=False)[0]
            w0 = self.t2p.get_text_width_height_descent("||", fp, ismath=False)[0]
            self._w[key] = (w1 - w0) * 100.0 / 72.0
        return self._w[key]

    def block(self, text, base):
        """[(runs, width)], block width, block height, line height."""
        lines = parse_html(text, base)
        info = [(runs, sum(self.width(s, st) for s, st in runs)) for runs in lines]
        lh = LINE * base["size"]
        w = max((w for _, w in info), default=0.0)
        return info, w, len(info) * lh, lh


# ----------------------------------------------------------------------------- the renderer

class Renderer:
    def __init__(self, pfig):
        self.src = pfig
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.full = pfig.full_figure_for_development(warn=False)
            self.resolved = True
        except Exception:                      # no kaleido: draw from the input figure
            self.full = pfig
            self.resolved = False
        L = self.full.layout
        self.W = float(L.width or 700)
        self.H = float(L.height or 450)
        m = L.margin
        self.l, self.r = float(m.l if m.l is not None else 80), float(m.r if m.r is not None else 80)
        self.t, self.b = float(m.t if m.t is not None else 100), float(m.b if m.b is not None else 80)
        self.pw, self.ph = self.W - self.l - self.r, self.H - self.t - self.b
        lf = L.font
        self.base = dict(size=float(lf.size or 12), color=lf.color or S.INK, weight=weight(lf.weight))
        self.family = FAMILY
        self.axes = {}
        lj = L.to_plotly_json()
        for k in lj:
            if re.fullmatch(r"[xy]axis\d*", k):
                self.axes[k[0] + k[5:]] = L[k]
        self.axes.setdefault("x", L.xaxis)
        self.axes.setdefault("y", L.yaxis)
        if not self.resolved:
            self._fallback_ranges()

    def src_text(self, key):
        """Axis title from the input figure: the resolved figure fills empty
        titles with editor placeholders such as 'Click to enter Y axis title'."""
        name = key[0] + "axis" + key[1:]
        try:
            ax = self.src.layout[name]
        except (KeyError, ValueError):
            return None
        return ax.title.text if ax is not None and ax.title is not None else None

    # --- coordinates (canvas px, origin bottom left)
    def _axis(self, ref):
        return self.axes.get(ref)

    def _dom(self, ax):
        d = ax.domain if ax is not None and ax.domain is not None else (0, 1)
        return float(d[0]), float(d[1])

    def _rng(self, ax):
        r = ax.range if ax is not None and ax.range is not None else (0, 1)
        return float(r[0]), float(r[1])

    def X(self, v, ref="paper"):
        v = num(v)
        if v is None:
            return None
        ref = ref or "paper"
        if ref == "paper":
            return self.l + v * self.pw
        if ref == "container":
            return v * self.W
        if ref.endswith(" domain"):
            d0, d1 = self._dom(self._axis(ref.split()[0]))
            return self.l + (d0 + v * (d1 - d0)) * self.pw
        ax = self._axis(ref)
        d0, d1 = self._dom(ax)
        r0, r1 = self._rng(ax)
        return self.l + (d0 + (v - r0) / ((r1 - r0) or 1) * (d1 - d0)) * self.pw

    def Y(self, v, ref="paper"):
        v = num(v)
        if v is None:
            return None
        ref = ref or "paper"
        if ref == "paper":
            return self.b + v * self.ph
        if ref == "container":
            return v * self.H
        if ref.endswith(" domain"):
            d0, d1 = self._dom(self._axis(ref.split()[0]))
            return self.b + (d0 + v * (d1 - d0)) * self.ph
        ax = self._axis(ref)
        d0, d1 = self._dom(ax)
        r0, r1 = self._rng(ax)
        return self.b + (d0 + (v - r0) / ((r1 - r0) or 1) * (d1 - d0)) * self.ph

    def box(self, xref, yref):
        """Subplot rectangle in canvas px for clipping."""
        x0, x1 = self._dom(self._axis(xref))
        y0, y1 = self._dom(self._axis(yref))
        return (self.l + x0 * self.pw, self.b + y0 * self.ph, (x1 - x0) * self.pw, (y1 - y0) * self.ph)

    def _fallback_ranges(self):
        ext = {}
        for tr in self.full.data:
            for a, vals, err in (("x" + (tr.xaxis or "x")[1:], getattr(tr, "x", None), getattr(tr, "error_x", None)),
                                 ("y" + (tr.yaxis or "y")[1:], getattr(tr, "y", None), getattr(tr, "error_y", None))):
                vs = [num(v) for v in (arr(vals) or [])]
                vs = [v for v in vs if v is not None]
                if err is not None and err.array is not None:
                    p = [num(v) or 0 for v in arr(err.array)]
                    mi = [num(v) or 0 for v in arr(err.arrayminus if err.arrayminus is not None else err.array)]
                    vs += [v + q for v, q in zip(vs, p)] + [v - q for v, q in zip(vs, mi)]
                if tr.type == "bar" and a[0] == "y":
                    vs.append(0.0)
                if vs:
                    lo, hi = ext.get(a, (min(vs), max(vs)))
                    ext[a] = (min(lo, min(vs)), max(hi, max(vs)))
        for k, ax in self.axes.items():
            if ax.range is None:
                lo, hi = ext.get(k, (0, 1))
                pad = 0.06 * ((hi - lo) or 1)
                ax.range = (lo - pad, hi + pad)

    # --- drawing primitives
    def text_block(self, text, x, y, xanchor="left", yanchor="middle", align="left", font=None, z=6, alpha=1.0,
                   bg=None, border=None, pad=0.0, bw=1.0, angle=0.0, title=False):
        base = dict(self.base)
        if font is not None:
            if font.get("size"):
                base["size"] = float(font["size"])
            if font.get("color"):
                base["color"] = font["color"]
            if font.get("weight") is not None:
                base["weight"] = weight(font["weight"])
        info, w, h, lh = self.ts.block(text, base)
        bx_w, bx_h = w + 2 * pad, h + 2 * pad
        if angle:
            # rotated text: one style, rotated about its own center (Plotly textangle, clockwise)
            plain = "\n".join("".join(s for s, _ in runs) for runs, _ in info)
            st = info[0][0][0][1] if info and info[0][0] else base
            cx = x + {"left": bx_w / 2, "right": -bx_w / 2}.get(xanchor, 0)
            cy = y + {"bottom": bx_h / 2, "top": -bx_h / 2}.get(yanchor, 0)
            self.ax.text(cx, cy, plain, fontproperties=self.ts.fp(st), color=col(st.get("color", base["color"])),
                         rotation=-angle, rotation_mode="anchor", ha="center", va="center", zorder=z, alpha=al(alpha),
                         parse_math=False, linespacing=LINE)
            return
        x0 = {"left": x, "right": x - bx_w}.get(xanchor, x - bx_w / 2)
        top = {"top": y, "bottom": y + bx_h}.get(yanchor, y + bx_h / 2)
        if visible_color(bg) or visible_color(border):
            self.ax.add_patch(Rectangle((x0, top - bx_h), bx_w, bx_h, facecolor=col(bg) if visible_color(bg) else "none",
                                        edgecolor=col(border) if visible_color(border) else "none",
                                        lw=bw * PX if visible_color(border) else 0, zorder=z - 0.05, alpha=al(alpha)))
        for i, (runs, lw_) in enumerate(info):
            lx = x0 + pad + {"left": 0, "right": w - lw_}.get(align, (w - lw_) / 2)
            by = (top - TITLE_BASELINE * base["size"] - i * lh if title else
                  top - pad - (i + 0.5) * lh - 0.36 * base["size"])
            for s, st in runs:
                if s.strip():
                    self.ax.text(lx, by, s, fontproperties=self.ts.fp(st), color=col(st.get("color", base["color"])),
                                 ha="left", va="baseline", zorder=z, alpha=al(alpha), parse_math=False)
                lx += self.ts.width(s, st)
        return w, h

    def seg(self, x0, y0, x1, y1, color, width, d=None, z=3, alpha=1.0, clip=None):
        if None in (x0, y0, x1, y1) or not visible_color(color) or not width:
            return
        ln, = self.ax.plot([x0, x1], [y0, y1], color=col(color), lw=width * PX, ls=dash(d, width * PX), zorder=z,
                           alpha=al(alpha), solid_capstyle="butt")
        if clip is not None:
            ln.set_clip_path(clip)

    # --- axes
    def ticks(self, ax):
        r0, r1 = self._rng(ax)
        lo, hi = min(r0, r1), max(r0, r1)
        if ax.tickmode == "array" or (ax.tickvals is not None and ax.tickmode != "linear"):
            vals = [num(v) for v in (ax.tickvals or [])]
            texts = list(ax.ticktext) if ax.ticktext is not None else [None] * len(vals)
        else:
            dt = num(ax.dtick)
            t0 = num(ax.tick0) or 0.0
            if not dt:
                loc = matplotlib.ticker.MaxNLocator(nbins=ax.nticks or 6, steps=[1, 2, 2.5, 5, 10])
                vals = [v for v in loc.tick_values(lo, hi)]
            else:
                k0 = math.ceil((lo - t0) / dt - 1e-9)
                vals = []
                k = k0
                while t0 + k * dt <= hi + 1e-9 * abs(dt) and len(vals) < 200:
                    vals.append(t0 + k * dt)
                    k += 1
            texts = [None] * len(vals)
        out = []
        for v, tx in zip(vals, texts):
            if v is None or v < lo - 1e-9 * (hi - lo or 1) or v > hi + 1e-9 * (hi - lo or 1):
                continue
            out.append((v, self.fmt(ax, v) if tx is None else str(tx)))
        return out

    def fmt(self, ax, v):
        f = ax.tickformat or ""
        if abs(v) < 1e-12:
            v = 0.0
        m = re.fullmatch(r"(,?)\.(\d+)([f%])", f)
        if ax.tickmode == "array":       # Plotly prints array ticks without text as bare numbers
            body = f"{abs(v) * 100:{m.group(1)}.{m.group(2)}f}%" if m and m.group(3) == "%" else (
                f"{abs(v):{m.group(1)}.{m.group(2)}f}" if m else f"{abs(v):g}")
            return ("\u2212" if v < 0 else "") + body
        if m:
            if m.group(3) == "%":
                body = f"{abs(v) * 100:{m.group(1)}.{m.group(2)}f}%"
            else:
                body = f"{abs(v):{m.group(1)}.{m.group(2)}f}"
        else:
            dt = num(ax.dtick) or 1.0
            nd = max(0, -int(math.floor(math.log10(abs(dt)) + 1e-9))) if dt and abs(dt) < 1 else 0
            a = abs(v)
            if a >= 10000 and (ax.exponentformat in (None, "B", "SI")):
                body = f"{a / 1000:g}k"
            else:
                body = f"{a:.{nd}f}"
        sign = "−" if v < 0 else ""
        pre = ax.tickprefix or ""
        suf = ax.ticksuffix or ""
        return f"{sign}{pre}{body}{suf}"

    def draw_axes(self):
        for key, ax in self.axes.items():
            if ax.visible is False:
                continue
            is_x = key[0] == "x"
            anchor = ax.anchor if ax.anchor and ax.anchor != "free" else ("y" if is_x else "x")
            other = self.axes.get(anchor)
            od0, od1 = self._dom(other)
            d0, d1 = self._dom(ax)
            ticks = self.ticks(ax)
            side = ax.side or ("bottom" if is_x else "left")
            if is_x:
                ybase = self.b + (od0 if side == "bottom" else od1) * self.ph
                ylo, yhi = self.b + od0 * self.ph, self.b + od1 * self.ph
            else:
                xbase = self.l + (od0 if side == "left" else od1) * self.pw
                xlo, xhi = self.l + od0 * self.pw, self.l + od1 * self.pw
            # grid and zero line
            if ax.showgrid:
                for v, _ in ticks:
                    if is_x:
                        p = self.X(v, key)
                        self.seg(p, ylo, p, yhi, ax.gridcolor or S.GRID, ax.gridwidth or 1, ax.griddash, z=1)
                    else:
                        p = self.Y(v, key)
                        self.seg(xlo, p, xhi, p, ax.gridcolor or S.GRID, ax.gridwidth or 1, ax.griddash, z=1)
            r0, r1 = self._rng(ax)
            if ax.zeroline and min(r0, r1) <= 0 <= max(r0, r1):
                if is_x:
                    p = self.X(0, key)
                    self.seg(p, ylo, p, yhi, ax.zerolinecolor or S.AXIS, ax.zerolinewidth or 1, z=1.2)
                else:
                    p = self.Y(0, key)
                    self.seg(xlo, p, xhi, p, ax.zerolinecolor or S.AXIS, ax.zerolinewidth or 1, z=1.2)
            if ax.showline:
                if is_x:
                    self.seg(self.l + d0 * self.pw, ybase, self.l + d1 * self.pw, ybase, ax.linecolor, ax.linewidth or 1,
                             z=2.5)
                else:
                    self.seg(xbase, self.b + d0 * self.ph, xbase, self.b + d1 * self.ph, ax.linecolor, ax.linewidth or 1,
                             z=2.5)
            tl = (ax.ticklen or 0) if ax.ticks in ("outside", "inside") else 0
            if tl:
                sgn = 1 if ax.ticks == "outside" else -1
                for v, _ in ticks:
                    if is_x:
                        p = self.X(v, key)
                        dy = -sgn * tl if side == "bottom" else sgn * tl
                        self.seg(p, ybase, p, ybase + dy, ax.tickcolor, ax.tickwidth or 1, z=2.5)
                    else:
                        p = self.Y(v, key)
                        dx = -sgn * tl if side == "left" else sgn * tl
                        self.seg(xbase, p, xbase + dx, p, ax.tickcolor, ax.tickwidth or 1, z=2.5)
            tf = ax.tickfont.to_plotly_json() if ax.tickfont is not None else {}
            fsz = float(tf.get("size") or self.base["size"])
            off = (tl if ax.ticks == "outside" else 0) + (TICK_GAP_X if is_x else TICK_GAP_Y) + (ax.ticklabelstandoff or 0)
            ext = 0.0
            if ax.showticklabels is not False:
                for v, tx in ticks:
                    if not tx:
                        continue
                    if is_x:
                        res = self.text_block(tx, self.X(v, key), ybase - off if side == "bottom" else ybase + off,
                                              "center", "top" if side == "bottom" else "bottom", "center", tf, z=4)
                        ext = max(ext, res[1] if res else 0)
                    else:
                        res = self.text_block(tx, xbase - off if side == "left" else xbase + off, self.Y(v, key),
                                              "right" if side == "left" else "left", "middle",
                                              "right" if side == "left" else "left", tf, z=4)
                        ext = max(ext, res[0] if res else 0)
            title = self.src_text(key)
            if title:
                tfont = ax.title.font.to_plotly_json() if ax.title.font is not None else {}
                if is_x:
                    yy = ybase - off - (ext or fsz * LINE) - TITLE_GAP
                    self.text_block(title, self.l + (d0 + d1) / 2 * self.pw, yy, "center", "top", "center", tfont, z=4)
                else:
                    tsz = float(tfont.get("size") or self.base["size"])
                    xx = xbase - off - (ext or fsz) - TITLE_GAP - tsz * 0.6
                    self.text_block(title, xx, self.b + (d0 + d1) / 2 * self.ph, "center", "middle", "center", tfont,
                                    z=4, angle=-90)

    # --- traces
    def draw_traces(self):
        bars = {}
        for tr in self.full.data:
            if tr.visible is False or tr.visible == "legendonly":
                continue
            if tr.type == "bar":
                bars.setdefault((tr.xaxis or "x", tr.yaxis or "y"), []).append(tr)
        for (xr, yr), trs in bars.items():
            self.draw_bars(trs, xr, yr)
        for tr in self.full.data:
            if tr.visible is False or tr.visible == "legendonly":
                continue
            if tr.type == "scatter":
                self.draw_scatter(tr)
            elif tr.type != "bar":
                warnings.warn(f"mpl_render: trace type {tr.type} not drawn")

    def _errs(self, err, vals):
        if err is None or err.visible is False or err.visible is None and err.array is None:
            return None
        n = len(vals)
        if err.type in (None, "data"):
            p = [num(pick(arr(err.array), i, 0)) or 0 for i in range(n)]
            if err.symmetric is False and err.arrayminus is not None:
                mi = [num(pick(arr(err.arrayminus), i, 0)) or 0 for i in range(n)]
            else:
                mi = p
        elif err.type == "constant":
            p = [err.value or 0] * n
            mi = [err.valueminus if err.symmetric is False else err.value or 0] * n
        elif err.type == "percent":
            p = [abs(v or 0) * (err.value or 0) / 100 for v in vals]
            mi = [abs(v or 0) * ((err.valueminus if err.symmetric is False else err.value) or 0) / 100 for v in vals]
        else:
            return None
        return p, mi

    def draw_errbar(self, cx, cy, horizontal, a, b, err, alpha, clip=None):
        """a, b: interval ends in canvas px along the value direction."""
        c = err.color or S.INK
        th = err.thickness if err.thickness is not None else 2
        cap = err.width if err.width is not None else 4
        if horizontal:
            self.seg(a, cy, b, cy, c, th, z=2.8, alpha=al(alpha), clip=clip)
            if cap:
                for e in (a, b):
                    self.seg(e, cy - cap, e, cy + cap, c, th, z=2.8, alpha=al(alpha), clip=clip)
        else:
            self.seg(cx, a, cx, b, c, th, z=2.8, alpha=al(alpha), clip=clip)
            if cap:
                for e in (a, b):
                    self.seg(cx - cap, e, cx + cap, e, c, th, z=2.8, alpha=al(alpha), clip=clip)

    def draw_scatter(self, tr):
        xr, yr = tr.xaxis or "x", tr.yaxis or "y"
        xs, ys = arr(tr.x) or [], arr(tr.y) or []
        n = min(len(xs), len(ys))
        X = [self.X(xs[i], xr) for i in range(n)]
        Y = [self.Y(ys[i], yr) for i in range(n)]
        mode = tr.mode or "markers"
        alpha = tr.opacity if tr.opacity is not None else 1.0
        clip = None
        if tr.cliponaxis is not False:
            bx = self.box(xr, yr)
            clip = Rectangle(bx[:2], bx[2], bx[3], transform=self.ax.transData)
        if "lines" in mode and tr.line is not None and (tr.line.width or 0) > 0:
            pts = [(x, y) for x, y in zip(X, Y) if x is not None and y is not None]
            if len(pts) > 1:
                ln, = self.ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col(tr.line.color or S.INK),
                                   lw=tr.line.width * PX, ls=dash(tr.line.dash, tr.line.width * PX), zorder=3,
                                   alpha=al(alpha), solid_joinstyle="round")
                if clip is not None:
                    ln.set_clip_path(clip)
        for err, horiz in ((tr.error_x, True), (tr.error_y, False)):
            vals = [num(v) for v in (xs if horiz else ys)[:n]]
            e = self._errs(err, vals)
            if not e:
                continue
            for i in range(n):
                if vals[i] is None or X[i] is None or Y[i] is None or (e[0][i] == 0 and e[1][i] == 0):
                    continue
                if horiz:
                    a, b = self.X(vals[i] - e[1][i], xr), self.X(vals[i] + e[0][i], xr)
                else:
                    a, b = self.Y(vals[i] - e[1][i], yr), self.Y(vals[i] + e[0][i], yr)
                self.draw_errbar(X[i], Y[i], horiz, a, b, err, alpha, clip)
        mk = tr.marker
        if "markers" in mode and mk is not None:
            for i in range(n):
                if X[i] is None or Y[i] is None:
                    continue
                self.marker(X[i], Y[i], mk, i, alpha, clip)
        if "text" in mode and tr.text is not None:
            texts = arr(tr.text)
            pos = tr.textposition or "middle center"
            tf = tr.textfont.to_plotly_json() if tr.textfont is not None else {}
            for i in range(n):
                tx = pick(texts, i)
                if not tx or X[i] is None or Y[i] is None:
                    continue
                p = pick(pos, i, "middle center")
                v, h = (p.split() + ["center"])[:2] if " " in p else ("middle", p)
                sz = (num(pick(mk.size, i, 6)) or 6) if mk is not None and "markers" in mode else 0
                gap = sz / 2 + 2 if sz else 0
                dx = {"right": gap, "left": -gap}.get(h, 0)
                dy = {"top": gap, "bottom": -gap}.get(v, 0)
                xa = {"right": "left", "left": "right"}.get(h, "center")
                ya = {"top": "bottom", "bottom": "top"}.get(v, "middle")
                self.text_block(str(tx), X[i] + dx, Y[i] + dy, xa, ya, "center" if xa == "center" else xa, tf, z=5,
                                alpha=al(alpha))

    def marker(self, x, y, mk, i, alpha, clip=None):
        sym = str(pick(mk.symbol, i, "circle"))
        is_open = sym.endswith("-open")
        base = sym.replace("-open", "").replace("-dot", "")
        m = SYMBOLS.get(base, "o")
        size = num(pick(mk.size, i, 6)) or 6
        c = pick(mk.color, i, S.INK)
        lc = pick(mk.line.color, i, None) if mk.line is not None else None
        lw = num(pick(mk.line.width, i, 0)) if mk.line is not None else 0
        lw = lw or 0
        mop = num(pick(mk.opacity, i, 1)) if mk.opacity is not None else 1.0
        line_like = m in ("|", "_", "x", "+")
        if line_like:
            fc, ec, ew = "none", col(lc or c), max(lw, 1) * PX
        elif is_open:
            fc, ec, ew = "none", col(lc or c), max(lw, 1) * PX
        else:
            fc, ec, ew = col(c), (col(lc) if lw and visible_color(lc) else "none"), lw * PX
        ms = size * PX * SYMBOL_SCALE.get(m, 1.0)
        ln, = self.ax.plot([x], [y], marker=m, ms=ms, mfc=fc, mec=ec, mew=ew, ls="none", zorder=3.5,
                           alpha=al(alpha * (mop if mop is not None else 1.0)))
        if clip is not None:
            ln.set_clip_path(clip)

    def draw_bars(self, trs, xr, yr):
        L = self.full.layout
        mode = L.barmode or "group"
        gap = L.bargap if L.bargap is not None else 0.2
        ggap = L.bargroupgap if L.bargroupgap is not None else 0.0
        allx = sorted({num(v) for tr in trs for v in (arr(tr.x) or []) if num(v) is not None})
        slot = min((b - a for a, b in zip(allx, allx[1:])), default=1.0) or 1.0
        n = len(trs) if mode == "group" else 1
        gw = slot * (1 - gap)
        for j, tr in enumerate(trs):
            xs, ys = arr(tr.x) or [], arr(tr.y) or []
            alpha = tr.opacity if tr.opacity is not None else 1.0
            bw = num(tr.width) or gw / n * (1 - ggap if n > 1 else 1)
            errs = self._errs(tr.error_y, [num(v) for v in ys])
            for i, (xv, yv) in enumerate(zip(xs, ys)):
                xv, yv = num(xv), num(yv)
                if xv is None or yv is None:
                    continue
                cx = xv - gw / 2 + (j + 0.5) * gw / n if mode == "group" else xv
                if tr.offset is not None:
                    cx = xv + num(tr.offset) + bw / 2
                x0, x1 = self.X(cx - bw / 2, xr), self.X(cx + bw / 2, xr)
                y0, y1 = self.Y(0, yr), self.Y(yv, yr)
                mk = tr.marker
                fc = pick(mk.color, i, S.ACCENT) if mk is not None else S.ACCENT
                lw = (num(pick(mk.line.width, i, 0)) or 0) if mk is not None and mk.line is not None else 0
                lc = pick(mk.line.color, i, None) if lw else None
                self.ax.add_patch(Rectangle((x0, min(y0, y1)), x1 - x0, abs(y1 - y0), facecolor=col(fc),
                                            edgecolor=col(lc) if lc else "none", lw=lw * PX, zorder=2.6, alpha=al(alpha)))
                if errs and (errs[0][i] or errs[1][i]):
                    cxp = self.X(cx, xr)
                    self.draw_errbar(cxp, None, False, self.Y(yv - errs[1][i], yr), self.Y(yv + errs[0][i], yr),
                                     tr.error_y, alpha)
                tx = pick(arr(tr.text), i) if tr.text is not None else None
                if tx:
                    tf = tr.textfont.to_plotly_json() if tr.textfont is not None else {}
                    self.text_block(str(tx), self.X(cx, xr), y1 + 3, "center", "bottom", "center", tf, z=5)

    # --- shapes
    def path(self, d, xr, yr):
        toks = re.findall(r"[MLQCZHVmlqczhv]|-?\d*\.?\d+(?:[eE][-+]?\d+)?", d)
        verts, codes = [], []
        i, cmd = 0, None
        cur = (0, 0)
        start = (0, 0)
        while i < len(toks):
            t = toks[i]
            if t.isalpha():
                cmd = t.upper()
                i += 1
                if cmd == "Z":
                    verts.append(start)
                    codes.append(MPath.CLOSEPOLY)
                continue
            if cmd in ("M", "L"):
                p = (self.X(toks[i], xr), self.Y(toks[i + 1], yr))
                verts.append(p)
                codes.append(MPath.MOVETO if cmd == "M" else MPath.LINETO)
                if cmd == "M":
                    start = p
                    cmd = "L"
                cur = p
                i += 2
            elif cmd == "Q":
                c1 = (self.X(toks[i], xr), self.Y(toks[i + 1], yr))
                p = (self.X(toks[i + 2], xr), self.Y(toks[i + 3], yr))
                verts += [c1, p]
                codes += [MPath.CURVE3, MPath.CURVE3]
                cur = p
                i += 4
            elif cmd == "C":
                pts = [(self.X(toks[i + k], xr), self.Y(toks[i + k + 1], yr)) for k in (0, 2, 4)]
                verts += pts
                codes += [MPath.CURVE4] * 3
                cur = pts[-1]
                i += 6
            elif cmd == "H":
                cur = (self.X(toks[i], xr), cur[1])
                verts.append(cur)
                codes.append(MPath.LINETO)
                i += 1
            elif cmd == "V":
                cur = (cur[0], self.Y(toks[i], yr))
                verts.append(cur)
                codes.append(MPath.LINETO)
                i += 1
            else:
                i += 1
        return MPath(verts, codes) if verts else None

    def draw_shapes(self):
        for sh in self.full.layout.shapes:
            if sh.visible is False:
                continue
            z = {"below": 0.5, "between": 1.5}.get(sh.layer, 4.5)
            xr, yr = sh.xref or "x", sh.yref or "y"
            ln = sh.line
            lc = ln.color if ln is not None else None
            lw = (ln.width if ln is not None and ln.width is not None else 2)
            ld = ln.dash if ln is not None else None
            alpha = sh.opacity if sh.opacity is not None else 1.0
            fc = sh.fillcolor
            if sh.type == "line":
                self.seg(self.X(sh.x0, xr), self.Y(sh.y0, yr), self.X(sh.x1, xr), self.Y(sh.y1, yr), lc, lw, ld, z=z,
                         alpha=al(alpha))
            elif sh.type == "rect":
                x0, x1 = self.X(sh.x0, xr), self.X(sh.x1, xr)
                y0, y1 = self.Y(sh.y0, yr), self.Y(sh.y1, yr)
                self.ax.add_patch(Rectangle((min(x0, x1), min(y0, y1)), abs(x1 - x0), abs(y1 - y0),
                                            facecolor=col(fc) if visible_color(fc) else "none",
                                            edgecolor=col(lc) if (lw and visible_color(lc)) else "none",
                                            lw=lw * PX, ls=dash(ld, lw * PX), zorder=z, alpha=al(alpha)))
            elif sh.type == "path" and sh.path:
                p = self.path(sh.path, xr, yr)
                if p is not None:
                    self.ax.add_patch(PathPatch(p, facecolor=col(fc) if visible_color(fc) else "none",
                                                edgecolor=col(lc) if (lw and visible_color(lc)) else "none",
                                                lw=lw * PX, ls=dash(ld, lw * PX), zorder=z, alpha=al(alpha)))
            elif sh.type == "circle":
                warnings.warn("mpl_render: circle shapes not drawn")

    # --- annotations
    def _auto(self, anchor, v, ref, axis):
        if anchor and anchor != "auto":
            return anchor
        if ref and (ref == "paper" or ref.endswith(" domain")) and num(v) is not None:
            v = num(v)
            if axis == "x":
                return "left" if v <= 1 / 3 else ("right" if v >= 2 / 3 else "center")
            return "bottom" if v <= 1 / 3 else ("top" if v >= 2 / 3 else "middle")
        return "center" if axis == "x" else "middle"

    def draw_annotations(self):
        for a in self.full.layout.annotations:
            if a.visible is False:
                continue
            xr, yr = a.xref or "x", a.yref or "y"
            x, y = self.X(a.x, xr), self.Y(a.y, yr)
            if x is None or y is None:
                continue
            alpha = a.opacity if a.opacity is not None else 1.0
            if a.showarrow:
                if a.axref and a.axref != "pixel":
                    tx, ty = self.X(a.ax, a.axref), self.Y(a.ay, a.ayref or yr)
                else:
                    tx, ty = x + (num(a.ax) or -10), y - (num(a.ay) or -30)
                aw = a.arrowwidth or 1
                ac = col(a.arrowcolor or S.INK)
                head = (a.arrowsize or 1) * aw * 3.2
                self.ax.add_patch(FancyArrowPatch((tx, ty), (x, y), arrowstyle=f"-|>,head_length={head * 0.9:.2f},"
                                                  f"head_width={head * 0.55:.2f}", mutation_scale=1, color=ac,
                                                  lw=aw * PX, zorder=4.8, alpha=al(alpha), shrinkA=0, shrinkB=0))
                if a.text:
                    self.text_block(a.text, tx, ty, "center", "middle", a.align or "center",
                                    a.font.to_plotly_json() if a.font else None, z=6, alpha=al(alpha))
                continue
            if not a.text:
                continue
            x += a.xshift or 0
            y += a.yshift or 0
            bw = a.borderwidth if a.borderwidth is not None else 1
            self.text_block(a.text, x, y, self._auto(a.xanchor, a.x, xr, "x"), self._auto(a.yanchor, a.y, yr, "y"),
                            a.align or "center", a.font.to_plotly_json() if a.font else None, z=6, alpha=al(alpha),
                            bg=a.bgcolor, border=a.bordercolor if bw else None,
                            pad=(a.borderpad if a.borderpad is not None else 1) + (bw if visible_color(a.bordercolor) else 0),
                            bw=bw, angle=num(a.textangle) or 0)

    def draw_title(self):
        t = self.full.layout.title
        if t is None or not t.text:
            return
        f = t.font.to_plotly_json() if t.font is not None else {}
        f.setdefault("size", self.base["size"] * 1.4)
        xref = t.xref or "container"
        yref = t.yref or "container"
        x = self.X(t.x if t.x is not None else 0.05, xref)
        y = self.Y(t.y if t.y is not None else 0.95, yref)
        xa = t.xanchor if t.xanchor not in (None, "auto") else "left"
        ya = t.yanchor if t.yanchor not in (None, "auto") else "top"
        self.text_block(t.text, x, y, xa, ya, "left", f, z=6, title=True)
        st_ = self.src.layout.title
        sub = st_.subtitle.text if getattr(st_, "subtitle", None) is not None else None
        if sub:
            sf = t.subtitle.font.to_plotly_json() if t.subtitle.font is not None else {}
            sf.setdefault("size", self.base["size"])
            _, _, h, _ = self.ts.block(t.text, dict(self.base, size=float(f["size"])))
            self.text_block(sub, x, y - h - 4, xa, "top", "left", sf, z=6)

    def draw_legend(self):
        L = self.full.layout
        if not L.showlegend:
            return
        items = [tr for tr in self.full.data if tr.showlegend is not False and tr.name]
        if not items:
            return
        lg = L.legend
        x = self.X(lg.x if lg.x is not None else 1.02, "paper")
        y = self.Y(lg.y if lg.y is not None else 1, "paper")
        f = lg.font.to_plotly_json() if lg.font is not None else {}
        sz = float(f.get("size") or self.base["size"])
        horiz = lg.orientation == "h"
        for tr in items:
            mk = tr.marker
            c = pick(mk.color, 0, S.INK) if mk is not None else S.INK
            sym = SYMBOLS.get(str(pick(mk.symbol, 0, "circle")).replace("-open", ""), "o") if tr.type == "scatter" else "s"
            self.ax.plot([x + 8], [y - sz * 0.65], marker=sym, ms=sz * 0.7 * PX * 1.4, mfc=col(c), mec="none", ls="none",
                         zorder=6)
            w, _ = self.text_block(tr.name, x + 20, y - sz * 0.65, "left", "middle", "left", f, z=6)
            if horiz:
                x += w + 40
            else:
                y -= sz * LINE + 4

    # --- page
    def render(self, png=None, svg=None, dpi=300):
        with matplotlib.rc_context(PAPER2_RC):
            fig = plt.figure(figsize=(self.W / 100, self.H / 100), dpi=100)
            self.fig = fig
            self.ax = fig.add_axes([0, 0, 1, 1])
            self.ax.set_xlim(0, self.W)
            self.ax.set_ylim(0, self.H)
            self.ax.axis("off")
            bg = col(self.full.layout.paper_bgcolor or S.SURFACE)
            fig.patch.set_facecolor(bg)
            self.ts = Typesetter(fig, self.family)
            pb = self.full.layout.plot_bgcolor
            if visible_color(pb) and col(pb) != bg:
                for key, ax in self.axes.items():
                    if key[0] == "x" and ax.visible is not False:
                        bx = self.box(key, ax.anchor or "y")
                        self.ax.add_patch(Rectangle(bx[:2], bx[2], bx[3], facecolor=col(pb), lw=0, zorder=0.1))
            self.draw_shapes()
            self.draw_axes()
            self.draw_traces()
            self.draw_annotations()
            self.draw_title()
            self.draw_legend()
            if png:
                fig.savefig(png, dpi=dpi, facecolor=bg)
            if svg:
                fig.savefig(svg, facecolor=bg)
            plt.close(fig)
        return png, svg


def font_in_use():
    """The family matplotlib will actually use for the paper font stack."""
    with matplotlib.rc_context(PAPER2_RC):
        return FontProperties(fname=findfont(FontProperties(family=FAMILY))).get_name()


def render(pfig, png: Path | str | None, svg: Path | str | None = None, dpi: int = 300):
    return Renderer(pfig).render(png, svg, dpi)
