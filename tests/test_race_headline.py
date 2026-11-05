"""Six-group headline figure and omnibus test (PLAN.md D12), and the one dollar definition."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import paper_calc as P  # noqa: E402
import race_headline as RH  # noqa: E402


def _names(shift, seed=0):
    rng = np.random.default_rng(seed)
    n = {"White": 20, "Black": 20, "Hispanic": 12, "Asian": 12, "MENA": 10, "South Asian": 8}
    race = np.concatenate([[r] * k for r, k in n.items()])
    woman = np.tile([0.0, 1.0], len(race) // 2)
    y = rng.normal(0, 0.01, len(race)) + np.array([shift.get(r, 0.0) for r in race])
    return y, race, woman


def test_race_f_finds_a_planted_group_and_not_noise():
    y, race, woman = _names({"Black": -0.03})
    f, q, dfr = RH._race_f(y, race, woman, RH.RACES)
    assert q == 5 and dfr == len(y) - 7 and f > 10
    y0, *_ = _names({}, seed=3)
    assert RH._race_f(y0, race, woman, RH.RACES)[0] < 5


def test_title_never_claims_a_difference_the_omnibus_does_not_support():
    t = pd.DataFrame({"model": ["luna"] * 2, "race": ["White", "Black"], "gap_pct": [0.0, -1.8]})
    none = {"haiku": {"p_perm": 0.76}, "luna": {"p_perm": 0.20}}
    assert RH.headline_title(t, none).startswith("No price difference")
    some = {"haiku": {"p_perm": 0.76}, "luna": {"p_perm": 0.01}}
    title = RH.headline_title(t, some)
    assert "differs" in title and "Luna (p = .010" in title and "not on Haiku (p = .760)" in title
    assert "differed" in RH.six_group_sentence(t, some) and "did not differ" in RH.six_group_sentence(t, some)


def test_one_dollar_definition():
    ref = {"ref_usd": 31.22, "focal_usd": 30.78}
    tr = P.dollar_translation(np.log(1 - 0.018), np.log(1 - 0.026), np.log(1 - 0.009), 31.22)
    u = P.unify_focal(ref, tr)
    assert abs((u["ref_usd"] - u["focal_usd"]) - (-tr["usd_per_purchase"])) < 1e-12
    assert u["focal_usd_cellmean"] == 30.78 and abs(u["focal_usd"] - 30.658) < 0.01
