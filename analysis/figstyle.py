"""Shared drawing rules for the paper figures (paper/FIGURES_SPEC.md section 0).

Color means model and nothing else (same hexes and markers as analyze.py).
Name groups are encoded by position and text. Text is always in ink colors.
Every figure built from pilot data gets the PILOT watermark on every panel,
in the footer and in the file name.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

import analyze as A  # noqa: E402
from paper_calc import MODEL_LABEL, WATERMARK  # noqa: E402

INK = "#1f1f1c"
MUTED = "#6b6a63"
AXIS = "#b5b4ad"
GRID = "#e6e5e0"
BAND = "#efeee9"
STAMP = "#9a998f"
SURFACE = "#ffffff"
DPI = 300

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.edgecolor": AXIS, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": INK, "text.color": INK, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE, "svg.fonttype": "path",
    "axes.unicode_minus": False,
})


def color(m):
    return A.MODEL_COLORS.get(m, INK)


def marker(m):
    return A.MODEL_MARKERS.get(m, "o")


def label(m):
    return MODEL_LABEL.get(m, m)


def style(ax, value_axis="x"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(AXIS)
    ax.spines["bottom"].set_color(AXIS)
    ax.tick_params(length=2.5)
    ax.grid(axis=value_axis, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)


def dot(ax, x, y, lo, hi, model, fill="full", size=6.5, horizontal=True, zorder=3):
    """Dot plus a 2 px interval line, white ring around the marker."""
    c = color(model)
    if lo is not None and hi is not None and lo == lo and hi == hi:
        if horizontal:
            ax.plot([lo, hi], [y, y], color=c, lw=2, solid_capstyle="round", zorder=zorder)
        else:
            ax.plot([x, x], [lo, hi], color=c, lw=2, solid_capstyle="round", zorder=zorder)
    kw = dict(marker=marker(model), ms=size, mec=c, mew=1.4, zorder=zorder + 1, ls="none")
    if fill == "full":
        kw.update(mfc=c, mec="white", mew=1.2)
    elif fill == "none":
        kw.update(mfc="white")
    else:  # half: inconclusive or not tested
        kw.update(mfc=c, fillstyle="left", markerfacecoloralt="white")
    ax.plot([x], [y], **kw)


def model_handles(models, fill="full"):
    hs = []
    for m in models:
        kw = dict(marker=marker(m), color=color(m), lw=2, ms=6)
        if fill == "full":
            kw.update(mfc=color(m), mec="white")
        hs.append(Line2D([0], [0], label=label(m), **kw))
    return hs


def stamp(ax):
    """Large light-gray diagonal stamp, behind the marks."""
    bb = ax.get_window_extent().transformed(ax.figure.dpi_scale_trans.inverted())
    fs = max(6, min(30, 72 * bb.width / (len(WATERMARK) * 0.62)))
    ax.text(0.5, 0.5, WATERMARK, transform=ax.transAxes, ha="center", va="center", rotation=22,
            fontsize=fs, fontweight="bold", color=STAMP, alpha=0.25, zorder=0, clip_on=True)


def stamp_figure(fig):
    for ax in fig.axes:
        if ax.get_label() == "nostamp":
            continue
        stamp(ax)
    fig.text(0.995, 0.995, WATERMARK, ha="right", va="top", fontsize=8, fontweight="bold", color=INK)


def save(fig, outdir: Path, stem: str, pilot: bool, made: list, watermark: bool = True) -> dict:
    """PNG at 300 dpi and SVG. Pilot: stamp every panel and suffix _PILOT."""
    outdir.mkdir(parents=True, exist_ok=True)
    if pilot and watermark:
        fig.canvas.draw()
        stamp_figure(fig)
        stem = stem + "_PILOT"
    png, svg = outdir / f"{stem}.png", outdir / f"{stem}.svg"
    fig.savefig(png, dpi=DPI)
    fig.savefig(svg)
    plt.close(fig)
    rec = {"png": str(png), "svg": str(svg)}
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
