"""Add-on analysis (PLAN.md D9/D10): its own BH family, Wilson rates, frozen outputs untouched."""
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import addon_analysis as X  # noqa: E402


def _nm(gap, n_a=5, n_b=20, seed=0):
    rng = np.random.default_rng(seed)
    y = np.r_[rng.normal(gap, 0.02, n_a), rng.normal(0, 0.02, n_b)]
    return pd.DataFrame({"profile_id": [f"p{i}" for i in range(n_a + n_b)], "mean": y,
                         "focal": [1.0] * n_a + [0.0] * n_b, "log_name_freq": rng.normal(10, 1, n_a + n_b)})


def test_family_bh_and_untestable():
    fam = X.Family()
    fam.add("A", "haiku", "big", _nm(0.2), "focal", None, "rate")
    fam.add("A", "haiku", "null", _nm(0.0, seed=1), "focal", None, "rate")
    flat = _nm(0.0).assign(mean=0.0)
    fam.add("A", "haiku", "flat", flat, "focal", None, "rate")
    fam.finish()
    assert len(fam.tests) == 2 and len(fam.untestable) == 1
    big = next(t for t in fam.tests if t["test"] == "big")
    assert big["discovery_q10"] and abs(big["gap_points"] - 20) < 3
    assert fam.untestable[0]["q_bh"] is None


def test_pooled_wilson():
    r = X.pooled(pd.DataFrame({"profile_id": ["a"] * 10, "y": [1.0] * 0 + [0.0] * 10}), "y")
    assert r["k"] == 0 and r["n"] == 10 and r["wilson_lo"] == 0 and 0.25 < r["wilson_hi"] < 0.32
    assert X.fmt_rate({"k": 3.0, "n": 10.0, "rate": .3, "wilson_lo": .1, "wilson_hi": .6}).endswith("(3/10)")


def test_frozen_results_untouched_by_addon_run():
    """The add-on script writes only addon_* tables, figA6/figA7 and results/addon_exploratory.json."""
    src = (ROOT / "analysis" / "addon_analysis.py").read_text()
    writes = [ln for ln in src.splitlines() if ".write_text(" in ln or ".to_csv(" in ln]
    assert writes
    for ln in writes:
        assert "confirmatory" not in ln and "checks" not in ln
        assert "exploratory" not in ln or "addon_exploratory" in ln
    assert '"addon_exploratory.json"' in src
