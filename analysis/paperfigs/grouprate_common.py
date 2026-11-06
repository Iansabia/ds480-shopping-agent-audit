"""Helpers for the rate-by-name-group figures (fig6, fig7): one band per model on the y axis,
five name groups stacked inside each band, dot = estimate, thin whisker = 95% interval."""
import pandas as pd
from matplotlib.lines import Line2D

from paperfigs.style import GROUP, GRAY, MARKER, MODEL

# CSV group names (singular) -> style.GROUP keys (plural); no-name accounts in gray
GROUPS = ["Black woman", "Black man", "White woman", "White man", "No name"]
GLABEL = {"Black woman": "Black women", "Black man": "Black men", "White woman": "White women",
          "White man": "White men", "No name": "No name"}
GCOLOR = {g: GROUP.get(GLABEL[g], GRAY["mid"]) for g in GROUPS}
GCOLOR["No name"] = GRAY["mid"]
MODELS = ["haiku", "luna", "flashlite", "olmo"]
EXPLORATORY = {"flashlite", "olmo"}           # open markers: estimate only
OFFS = [0.32, 0.16, 0.0, -0.16, -0.32]       # vertical offsets of the 5 groups inside a band
# full model names, broken over two lines so the left label column stays narrow
MODEL_2L = {"haiku": "Claude\nHaiku 5.5", "luna": "GPT-6\nLuna", "flashlite": "Gemini 3.5\nFlash-Lite",
            "olmo": "OLMo 3\n7B"}


def band_y(models=MODELS):
    """Model -> band centre; first model on top."""
    n = len(models)
    return {m: n - 1 - i for i, m in enumerate(models)}


def draw_rows(ax, sub, models=MODELS, scale=100.0, ms=2.6, base=lambda m: m):
    """sub: rows with model, group, est, lo, hi. Draws every (model, group) cell present."""
    yc = band_y(models)
    for m in models:
        for g, off in zip(GROUPS, OFFS):
            r = sub[(sub["model"] == m) & (sub["group"] == g)]
            if r.empty:
                continue
            r = r.iloc[0]
            y = yc[m] + off
            c = GCOLOR[g]
            est, lo, hi = r["est"] * scale, r["lo"] * scale, r["hi"] * scale
            if pd.notna(lo) and pd.notna(hi) and hi > lo:
                ax.plot([lo, hi], [y, y], color=c, lw=0.7, solid_capstyle="butt", zorder=2)
            openm = base(m) in EXPLORATORY
            ax.plot(est, y, marker=MARKER[base(m)], ms=ms, mec=c, mew=0.7,
                    mfc="white" if openm else c, ls="none", zorder=3)


def model_axis(ax, models=MODELS, labels=True):
    yc = band_y(models)
    ax.set_ylim(-0.55, len(models) - 0.45)
    ax.set_yticks([yc[m] for m in models])
    ax.set_yticklabels([MODEL_2L[m] for m in models] if labels else [], linespacing=1.0)
    ax.tick_params(axis="y", length=0)
    for m in models[1:]:
        ax.axhline(yc[m] + 0.5, color=GRAY["faint"], lw=0.5, zorder=0)


def group_legend(fig, y=1.0, ncol=5, x=0.5):
    h = [Line2D([], [], marker="o", ms=3.2, ls="-", lw=0.7, color=GCOLOR[g], mfc=GCOLOR[g], mec=GCOLOR[g])
         for g in GROUPS]
    lab = [GLABEL[g] if g != "No name" else "No name on the account" for g in GROUPS]
    return fig.legend(h, lab, loc="lower center", bbox_to_anchor=(x, y), ncol=ncol, handletextpad=0.4,
                      handlelength=1.5,
                      columnspacing=1.0, borderaxespad=0.0)
