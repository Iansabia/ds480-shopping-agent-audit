"""Tests for the frozen analysis script on synthetic data (PLAN 11).

Two synthetic worlds are built with the real catalog, grids and scorer:
  planted: names associated with Black buyers get a price, override and assume effect
  null:    no name effect at all
The frozen pipeline must find the planted effects, cover the true gap, and
stay quiet on the null world.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import stats
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import analyze as A  # noqa: E402


def _run_world(tmp: Path, effect: float, h3: float, h4: float):
    paths = A.synth(tmp / "logs", effect=effect, h3_effect=h3, h4_effect=h4, seed=480)
    ns = argparse.Namespace(results=str(tmp / "results"), data=str(A.DATA), mde=None,
                            confirm_models=["synth_a", "synth_b"], perms=500, shuffles=200,
                            pilot=paths["pilot"], family_size=None)
    A.cmd_mde(ns)
    ns.outcomes = [p for k, v in paths.items() if k not in ("pilot", "truth") for p in v]
    res = A.cmd_all(ns)
    df = A.load_outcomes(ns.outcomes)
    return res, df, paths


@pytest.fixture(scope="module")
def planted(tmp_path_factory):
    return _run_world(tmp_path_factory.mktemp("planted"), 0.3, 0.5, 0.6)


@pytest.fixture(scope="module")
def null(tmp_path_factory):
    return _run_world(tmp_path_factory.mktemp("null"), 0.0, 0.0, 0.0)


# ---------------------------------------------------------------- unit pieces

def test_holm_and_bh_match_statsmodels():
    p = [0.001, 0.02, 0.03, 0.2, 0.04, 0.5, 0.012, 0.9]
    assert np.allclose(A.holm(p), multipletests(p, method="holm")[1])
    assert np.allclose(A.bh(p), multipletests(p, method="fdr_bh")[1])


def test_mde_matches_power_t_test():
    # R: power.t.test(n = 20, sd = 1, sig.level = 0.05, power = 0.8)$delta = 0.9091587
    assert abs(A.mde(20, 20, 1.0, 0.05, n_cov=0) - 0.9091587) < 1e-3
    # stricter alpha and covariates make the detectable gap larger
    assert A.mde(20, 20, 1.0, 0.05 / 8) > A.mde(20, 20, 1.0, 0.05) > A.mde(20, 20, 1.0, 0.05, n_cov=0)


def test_mde_has_80_percent_power_by_simulation():
    rng = np.random.default_rng(1)
    d = A.mde(20, 20, 1.0, 0.05, n_cov=0)
    hits = 0
    for _ in range(4000):
        a, b = rng.normal(d, 1, 20), rng.normal(0, 1, 20)
        hits += stats.ttest_ind(a, b).pvalue < 0.05
    assert abs(hits / 4000 - 0.80) < 0.025


def test_tost_logic():
    r = A.TestResult(est=0.001, se=0.01, df=36, t=0.1, p=0.9, ci_lo=-0.02, ci_hi=0.02, n_a=20, n_b=20)
    assert A.tost(r, math.log(1.05))["p"] < 0.05          # tight CI around 0: equivalent
    r2 = A.TestResult(est=0.0, se=0.05, df=36, t=0.0, p=1.0, ci_lo=-0.1, ci_hi=0.1, n_a=20, n_b=20)
    assert A.tost(r2, math.log(1.05))["p"] > 0.05         # wide CI: not equivalent


def test_freq_rule_drops_collinear_frequency():
    names = pd.read_csv(A.DATA / "names.csv")
    core = names[(names["role"] == "main") & (names["tier"] == "core")]
    nm = pd.DataFrame({"log_name_freq": np.log1p(core["ssa_births_1950_2005"]).to_numpy(),
                       "is_black": (core["race"] == "Black").astype(float).to_numpy(),
                       "is_woman": (core["gender"] == "woman").astype(float).to_numpy()})
    assert A.freq_rule(nm, "is_black")[0] is False      # race and SSA frequency correlate about -0.84
    assert A.freq_rule(nm, "is_woman")[0] is True


# ---------------------------------------------------------------- planted world

def test_planted_effects_detected_after_holm(planted):
    res, _, _ = planted
    rows = {(r["model"], r["hypothesis"]): r for r in res["confirm"]["rows"]}
    assert res["confirm"]["family_size"] == 8
    for m in ("synth_a", "synth_b"):
        for h in ("H1", "H3", "H4"):
            assert rows[(m, h)]["p_holm"] < 0.05, (m, h)
            assert rows[(m, h)]["r_est"] > 0
        assert rows[(m, "H2")]["p_holm"] > 0.05      # no gender effect was planted


def test_ci_covers_true_price_gap(planted):
    _, df, paths = planted
    for m in ("synth_a", "synth_b"):
        true = A.synth_true_gap(df, paths["truth"][0], m, "H1").est
        est, _ = A.run_hypothesis(df, m, "H1")
        assert est.ci_lo <= true <= est.ci_hi


def test_validity_checks_pass(planted):
    res, _, _ = planted
    ch = res["checks"]
    for m in ("synth_a", "synth_b"):
        assert ch["planted"][m]["pass"] and ch["planted"][m]["own_shift_detected"]
        assert ch["arm_p"][m]["pass"]
        for h in A.HYPOTHESES:
            assert ch["shuffled_null"][m][h]["pass"], (m, h)
        assert ch["main_grid"][m]["enters_confirmatory_family"]


def test_figures_written(planted):
    res, _, _ = planted
    for k in ("fig1", "fig2", "figA1"):
        assert Path(res["figures"][k]).exists()


def test_confirm_refuses_without_checks(planted, tmp_path):
    _, _, paths = planted
    ns = argparse.Namespace(results=str(tmp_path), data=str(A.DATA), mde=None, confirm_models=["synth_a"],
                            perms=10, shuffles=10, outcomes=paths["main"])
    with pytest.raises(SystemExit):
        A.cmd_confirm(ns)


# ---------------------------------------------------------------- null world

def test_null_world_finds_nothing_confirmatory(null):
    res, _, _ = null
    assert all(r["p_holm"] >= 0.05 for r in res["confirm"]["rows"])


def test_null_world_exploratory_false_discoveries_are_rare(null):
    res, _, _ = null
    disc = [t for t in res["explore"]["tests"] if t["discovery_q10"]]
    assert len(disc) <= 0.10 * res["explore"]["n_tests"] + 2


def test_mde_file_reports_detectable_gap(null):
    _, _, _ = null
    # the mde step writes a conservative detectable gap for every hypothesis and model
    res_dir = Path(null[2]["pilot"][0]).parents[1] / "results"
    m = json.loads((res_dir / "mde.json").read_text())
    for model in ("synth_a", "synth_b"):
        for h in A.HYPOTHESES:
            c = m["models"][model][h]["conservative"]
            assert c["mde_holm"] > c["mde_raw"] > 0
        assert m["models"][model]["price_margin"] in ("narrow (3%)", "wide (5%)")
