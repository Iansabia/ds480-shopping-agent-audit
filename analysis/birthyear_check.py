"""Birth-year check behind APPENDIX.md B2 (the "Birth year" row). Exploratory, added after the main results.

The frozen H1 test (clear-request price, names associated with Black vs White buyers) is rerun with one
more name-level covariate: each core first name's births-weighted average birth year in Social Security
data, 1950 to 2005. The question is whether the race price gap is really an age signal, since the core
first names associated with Black buyers were given about 14 years later on average.

Everything except the extra covariate comes from the frozen analysis code (analysis/analyze.py):
the H1 episode selection, the cell adjustment, the name averages and the HC2 fit.

Inputs:  logs/main_luna.outcomes.csv, logs/main_haiku.outcomes.csv
         data/derived/core_name_mean_birth_year.csv (40 rows, built from the SSA yearly files
         yob1950.txt to yob2005.txt; the source is described in data/NAMES_README.md)
Output:  prints one line per model; writes nothing.

Run from the repo root:  .venv/bin/python -B analysis/birthyear_check.py
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import analyze as A  # noqa: E402  (frozen analysis code, used read-only)


def main():
    by = pd.read_csv(ROOT / "data" / "derived" / "core_name_mean_birth_year.csv")
    for run in ("main_luna", "main_haiku"):
        df = A.load_outcomes([str(ROOT / "logs" / f"{run}.outcomes.csv")])
        model = df["model"].iloc[0]
        d = A.hyp_data(df, model, "H1")                 # frozen H1 episode selection
        nm = A.name_means(d, "logp")                    # frozen cell adjustment and name averages
        nm = nm.merge(by[["profile_id", "mean_birth_year"]], on="profile_id", how="left")
        assert len(nm) == 40 and nm["mean_birth_year"].notna().all()
        z = (nm["mean_birth_year"] - nm["mean_birth_year"].mean()) / nm["mean_birth_year"].std()
        X = np.column_stack([np.ones(len(nm)), nm["is_black"], nm["is_woman"], z])
        b, se, dof = A._hc2_ols(X, nm["mean"].to_numpy(float))   # frozen HC2 fit
        p = 2 * stats.t.sf(abs(b[1] / se[1]), dof)
        q = stats.t.ppf(0.975, dof)
        lo, hi = b[1] - q * se[1], b[1] + q * se[1]
        g = nm.groupby("race")["mean_birth_year"].mean()
        print(f"{model}: race price gap with the first name's average birth year added: "
              f"{100 * (math.exp(b[1]) - 1):+.2f}% [{100 * (math.exp(lo) - 1):+.2f}, {100 * (math.exp(hi) - 1):+.2f}], "
              f"p = {p:.4f}, df = {dof}; average birth year {g['Black']:.1f} (Black-associated) vs "
              f"{g['White']:.1f} (White-associated)")


if __name__ == "__main__":
    main()
