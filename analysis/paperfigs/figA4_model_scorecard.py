"""Figure A4: every model on every outcome, compact forest plot (journal style)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
from paperfigs.style import FIGDATA, RESULTS, FULL, MODEL, MARKER, GRAY, mstyle, panel, save, plt, signed

NAME = "figA4_model_scorecard"
MODELS = ["haiku", "luna", "flashlite", "olmo"]
CONFIRM = {"haiku", "luna"}
COLS = [("H1", "H1 price,\nBlack minus\nWhite", "pct"),
        ("H2", "H2 price,\nwomen minus\nmen", "pct"),
        ("H3", "H3 stated need\noverridden", "pts"),
        ("H4", "H4 need guessed\nfrom name", "pts"),
        ("race: V ask rate", "Asked first\n(vague request)", "pts"),
        ("race: S1 cap violation", "Over budget\n(budget request)", "pts")]


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
                for s in (-1, 1):
                    ax.plot([s * v] * 2, [y + 0.18, y + 0.4], color=GRAY["mid"], lw=1.0,
                            solid_capstyle="butt", zorder=2)
        if unit == "pct":
            ax.set_xlim(-3.2, 3.2)
            ax.set_xticks([-2, 0, 2])
        else:
            ax.set_xlim(-13, 13)
            ax.set_xticks([-10, 0, 10])
        ax.xaxis.set_major_formatter(signed(0))
        ax.set_title(title, fontsize=7.5, pad=4, linespacing=1.05)
        ax.set_ylim(-0.6, len(MODELS) - 0.4)
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
    axes[0].set_yticks([ys[m] for m in MODELS], [MODEL[m] for m in MODELS])
    fig.text(0.5 * (axes[0].get_position().x0 + axes[1].get_position().x1), -0.04, "Gap (%)",
             ha="center", va="top", fontsize=8.5)
    fig.text(0.5 * (axes[2].get_position().x0 + axes[5].get_position().x1), -0.04,
             "Gap (percentage points)", ha="center", va="top", fontsize=8.5)
    return save(fig, NAME)


if __name__ == "__main__":
    print(make())
