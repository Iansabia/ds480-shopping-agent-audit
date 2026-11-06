"""Figure A4: every model on every outcome, compact forest plot (journal style)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerLine2D
from paperfigs.style import FIGDATA, RESULTS, FULL, MODEL, MARKER, GRAY, mstyle, panel, save, plt, signed, star_handle

NAME = "figA4_model_scorecard"
MODELS = ["haiku", "luna", "flashlite", "olmo"]
CONFIRM = {"haiku", "luna"}
COLS = [("H1", "(a) Test H1:\nprice, Black\nminus White", "pct"),
        ("H2", "(b) Test H2:\nprice, women\nminus men", "pct"),
        ("H3", "(c) Test H3: coily\nor deep-shade pick,\nneed stated,\nBlack minus White", "pts"),
        ("H4", "(d) Test H4: need\nguessed from name,\nBlack minus White", "pts"),
        ("race: V ask rate", "(e) Asked first\n(vague request),\nBlack minus White", "pts"),
        ("race: S1 cap violation", "(f) Over budget\n(budget request),\nBlack minus White", "pts")]


def detected(verdict):
    """Star a cell only when the data's own verdict says a gap was found (never computed here)."""
    v = str(verdict)
    return v.startswith("gap detected") or v.startswith("discovery at q")


def mde(m, h, key):
    try:
        d = json.load(open(RESULTS / "mde.json"))
        return d["models"][m][h]["conservative"][key]
    except (KeyError, TypeError, FileNotFoundError):
        return None


def make():
    df = pd.read_csv(FIGDATA / f"{NAME}.csv")
    untestable = {(u["model"], u["test"]) for u in json.load(open(RESULTS / "exploratory.json")).get("untestable", [])}
    fig, axes = plt.subplots(1, 6, figsize=(FULL, 1.95), sharey=True,
                             gridspec_kw={"wspace": 0.12, "width_ratios": [1, 1, 1.15, 1.15, 1.15, 1.15]})
    ys = {m: len(MODELS) - 1 - i for i, m in enumerate(MODELS)}
    for k, (ax, (out, title, unit)) in enumerate(zip(axes, COLS)):
        ax.axvline(0, color=GRAY["light"], lw=0.6, zorder=0)
        for m in MODELS:
            y = ys[m]
            r = df[(df.model == m) & (df.outcome == out)]
            if r.empty or pd.isna(r.est.iloc[0]):
                # read the reason from the data instead of guessing it from the model
                verdict = "" if r.empty else str(r.verdict.iloc[0])
                novar = "no name variation" in verdict or (m, out) in untestable
                ax.text(0, y, "no name\nvariation" if novar else "no runs", ha="center", va="center",
                        fontsize=7, color=GRAY["mid"], linespacing=0.95,
                        bbox=dict(fc="white", ec="none", pad=0.6))
                continue
            r = r.iloc[0]
            st = mstyle(m)
            ax.plot([r.lo, r.hi], [y, y], color=st["color"], lw=0.8, solid_capstyle="butt")
            ax.plot(r.est, y, ls="none", zorder=3, **{**st, "color": None})
            v = mde(m, out, "mde_holm_pct" if unit == "pct" else "mde_holm_points")
            if v:
                # one bracket per row, raised clear of the mark: |----| from -v to +v
                ax.plot([-v, v], [y + 0.34] * 2, color=GRAY["mid"], lw=0.6, zorder=2,
                        marker="|", ms=4.5, mew=0.9, markevery=[0, 1])
            if detected(r.verdict):
                # same glyph as the key's star entry, just above the mark
                ax.plot(r.est, y + 0.3, ls="none", marker="$*$", ms=5,
                        color=GRAY["dark"], zorder=3)
        if unit == "pct":
            ax.set_xlim(-3.2, 3.2)
            ax.set_xticks([-2, 0, 2])
        else:
            ax.set_xlim(-13, 13)
            ax.set_xticks([-10, 0, 10])
        ax.xaxis.set_major_formatter(signed(0))
        ax.set_title(title, fontsize=7, pad=4, linespacing=1.05)
        ax.set_ylim(-0.6, len(MODELS) - 0.4)
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axes[0].set_yticks([ys[m] for m in MODELS], [MODEL[m] for m in MODELS])
    fig.text(0.5 * (axes[0].get_position().x0 + axes[1].get_position().x1), -0.04,
             "Gap in price paid (%)\nleft of 0 = Black or\nwomen's names paid less",
             ha="center", va="top", fontsize=8.5, linespacing=1.15)
    fig.text(0.5 * (axes[2].get_position().x0 + axes[5].get_position().x1), -0.04,
             "Gap in how often the panel's outcome happened (percentage points)\n"
             "right of 0 = that outcome happened more often for Black names",
             ha="center", va="top", fontsize=8.5, linespacing=1.15)
    def mk(m, label):
        # marker plus a short line in the model's own color, as drawn in the panels
        return Line2D([], [], ls="-", lw=0.8, label=label, **mstyle(m))

    bracket = Line2D([], [], color=GRAY["mid"], lw=0.6, marker="|", ms=4.5, mew=0.9,
                     label="Gray bracket: smallest gap that\n"
                           "Claude Haiku's main test could find")
    text_only = dict(ls="none", marker="none")
    handles = [mk("haiku", "Claude Haiku 5.5 (filled = main model)"),
               mk("luna", "GPT-6 Luna (filled = main model)"),
               mk("flashlite", "Gemini 3.5 Flash-Lite (open = exploratory)"),
               mk("olmo", "OLMo 3 7B (open = exploratory)"),
               Line2D([], [], color=GRAY["dark"], lw=0.9,
                      label="Line through a mark: 95% interval\n(gray for exploratory models)"),
               Line2D([], [], label="Mark with no line: interval\nnarrower than the mark", **text_only),
               star_handle("Star: gap detected (unlikely to be\nchance after correcting for\nmultiple tests)"),
               Line2D([], [], color=GRAY["light"], lw=0.9, label="Light gray line: no gap (0)"),
               bracket,
               Line2D([], [], label="H1 to H4: the paper's main tests;\n(e), (f): extra checks", **text_only),
               Line2D([], [], label="Gray words: no gap\ncan be computed", **text_only)]
    # local copy of style.key() so the bracket entry can show both end ticks
    leg = fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.31),
                     bbox_transform=fig.transFigure, ncol=3, frameon=False, handlelength=1.8,
                     columnspacing=0.8, handletextpad=0.5, fontsize=7.5, borderaxespad=0.2,
                     labelspacing=0.55, handler_map={bracket: HandlerLine2D(numpoints=2)})
    for t, h in zip(leg.get_texts(), handles):
        if h.get_label().startswith("Gray words"):
            t.set_color(GRAY["mid"])
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
