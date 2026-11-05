"""H3 2x2 descriptive table (paper/tables/h3_2x2.csv and .md): wrong-product
rate by name group and stated need, S0 + S1, hair and skin tasks, core names,
main runs. No new test: the H3 estimate in results/confirmatory.json stays the
only inference.

Each cell gives the mean over names with a 95% percentile bootstrap interval
over names (2,000 draws, seed 20261104), and the pooled count k of n with a 95%
Wilson score interval. The Wilson interval is the one to read for cells with
0 wrong picks, where the name bootstrap has no width (D7 in PLAN.md Deviations).

    .venv/bin/python analysis/h3_2x2.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze as A  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RUNS = {"haiku": "logs/main_haiku.outcomes.csv", "luna": "logs/main_luna.outcomes.csv"}
LABEL = {"haiku": "Claude Haiku 5.5", "luna": "GPT-6 Luna"}
NEED = {"coily_4c": "deep", "deep_shade": "deep", "fine_straight": "light", "light_shade": "light"}
SEED, N_BOOT = 20261104, 2000


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    lo, hi = max(0.0, mid - half), min(1.0, mid + half)
    return (0.0 if k == 0 else lo), (1.0 if k == n else hi)


def build() -> pd.DataFrame:
    df = A.load_outcomes([str(ROOT / p) for p in RUNS.values()])
    rng = np.random.default_rng(SEED)
    rows = []
    for m in RUNS:
        d = A.subset(df, m, ["S0", "S1"], tasks="identity")
        d = d[d["opposite_need_pick"].notna() & d["stated_need"].isin(NEED)].assign(asked=lambda x: x["stated_need"].map(NEED))
        for race in ["White", "Black"]:
            for need in ["light", "deep"]:
                c = d[(d["race"] == race) & (d["asked"] == need)]
                nm = c.groupby("profile_id")["opposite_need_pick"].mean().to_numpy()
                boot = [nm[rng.integers(0, len(nm), len(nm))].mean() for _ in range(N_BOOT)]
                k, n = int(c["opposite_need_pick"].sum()), int(len(c))
                wl, wh = wilson(k, n)
                rows.append({"model": m, "names": race, "asked": need, "mean": 100 * nm.mean(),
                             "lo": 100 * np.percentile(boot, 2.5), "hi": 100 * np.percentile(boot, 97.5),
                             "wrong": k, "episodes": n, "pooled": 100 * k / n, "wilson_lo": 100 * wl,
                             "wilson_hi": 100 * wh, "n_names": len(nm),
                             "mismatch": (race == "White") == (need == "deep")})
    return pd.DataFrame(rows)


def f2(x: float) -> str:
    """Two decimals, halves rounded up (0.125 -> 0.13, as in the first version of this table)."""
    return f"{math.floor(x * 100 + 0.5 + 1e-9) / 100:.2f}"


def cell(r) -> str:
    w = f"{r.wrong:,} of {r.episodes:,}"
    wil = f"Wilson {f2(r.wilson_lo)} to {f2(r.wilson_hi)}"
    if r.wrong == 0:
        s = f"0% ({w}; {wil}; no spread between names, so no bootstrap interval)"
    else:
        s = f"{f2(r['mean'])}% [{f2(r.lo)}, {f2(r.hi)}], {w}; {wil}"
    return f"**{s}**" if r.mismatch else s


def main():
    t = build()
    out = ROOT / "paper" / "tables"
    t.to_csv(out / "h3_2x2.csv", index=False)
    conf = {r["model"]: r for r in json.loads((ROOT / "results" / "confirmatory.json").read_text())["rows"]
            if r["hypothesis"] == "H3"}
    L = ["# H3 2x2: wrong product by name group and stated need (descriptive, no new test)", "",
         "S0 and S1, the 20 hair and skin tasks, core names, finished episodes with a scored pick (bought), main runs "
         "only. Cell: share of picks that were the product for the other need (wrong product), averaged over names, "
         "with a 95% percentile bootstrap interval over names (2,000 draws); then wrong picks out of episodes, with a "
         "95% Wilson interval on the pooled share (in percent). A cell with 0 wrong picks has no spread between names, "
         "so only its Wilson interval is given. 20 names per row. **Bold** cells are the two mismatch cells: a name "
         "associated with White buyers asking for deep shade or coily 4C, and a name associated with Black buyers "
         "asking for light shade or fine straight hair. A name-based override would show up as a higher rate in "
         "those cells.", "",
         "The H3 estimate and verdict (results/confirmatory.json) stay the only inference. This table only shows "
         "where any override happens.", ""]
    for m in RUNS:
        s = t[t.model == m]
        L += [f"## {LABEL[m]}", "", "| Names associated with | Asked for light shade or fine straight | "
              "Asked for deep shade or coily 4C |", "|---|---|---|"]
        for race in ["White", "Black"]:
            a = s[(s.names == race) & (s.asked == "light")].iloc[0]
            b = s[(s.names == race) & (s.asked == "deep")].iloc[0]
            L.append(f"| {race} buyers | {cell(a)} | {cell(b)} |")
        c = conf[m]
        L += ["", f"H3 (Holm across 8): {c['gap_points']:+.2f} points, 95% CI {c['ci_points'][0]:+.2f} to "
              f"{c['ci_points'][1]:+.2f}, {c['verdict']}.", ""]
    L += ["## Reading", "",
          "- Wrong picks are rare in every cell (at most about 1%), for both models.",
          "- The mismatch cells are not higher than the matching cells in the same column. For Haiku, wrong picks "
          "are a bit more common when the stated need is light shade or fine straight, for both name groups alike.",
          "- Gemini is not shown: it is exploratory and has no S1 arm.", "",
          "Source: logs/main_haiku.outcomes.csv and logs/main_luna.outcomes.csv via analyze.load_outcomes (same "
          "columns as H3: stated_need, opposite_need_pick); made by analysis/h3_2x2.py. Numbers also in "
          f"paper/tables/h3_2x2.csv. Bootstrap seed {SEED}."]
    (out / "h3_2x2.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
