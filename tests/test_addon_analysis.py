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


def test_run_status_wording_comes_from_data():
    """Captions name partial runs and the models with C runs from the run status, not typed-in counts."""
    full = {"episodes": 2560, "finished": 2560, "bought": 2521, "partial": False}
    status = {"arab_haiku": full, "sasian_haiku": full, "arab_luna": full, "sasian_luna": full, "stated_luna": full}
    assert X.partial_note(status) == ""
    assert X.race_groups_note(status) == "Claude Haiku 5.5 and GPT-6 Luna"
    status["sasian_luna"] = {**full, "episodes": 1166, "bought": 1160, "partial": True}
    assert X.race_groups_note(status) == "Claude Haiku 5.5"
    assert "1,166 episodes, 1,160 bought" in X.partial_note(status)
    src = (ROOT / "analysis" / "addon_analysis.py").read_text()
    assert "190 of 2,560" not in src and "187 bought" not in src


def _fake_a7(flag_luna_black=True):
    """Small Table C rows and gap rows: White, Black and MENA names on Haiku and Luna, Black and White on Gemini."""
    rows, gaps = [], []
    for m in ["haiku", "luna", "flashlite"]:
        for race in (["White", "Black"] if m == "flashlite" else ["White", "Black", "MENA"]):
            rows.append({"model": m, "race": race, "outcome": "price", "names": 20, "n": 3000})
            for out in ["h3", "h4", "ask", "override"]:
                n = 3200 if out == "ask" else 400
                rows.append({"model": m, "race": race, "outcome": out, "k": n // 2, "n": n, "rate": 0.5,
                             "wilson_lo": 0.49 if out == "ask" else 0.45, "wilson_hi": 0.51 if out == "ask" else 0.55,
                             "names": 20})
            if race == "White":
                continue
            for out in ["price", "h3", "h4", "ask"]:
                conf = race == "Black" and out in ("price", "h4") and m != "flashlite"
                gaps.append({"model": m, "race": race, "outcome": out,
                             "source": f"confirmatory {'H1' if out == 'price' else 'H4'}" if conf else "frozen exploratory",
                             "adj": "Holm p .001" if conf else "q .500", "disp": (-1.0, -2.0, 0.1),
                             "flagged": bool(flag_luna_black and conf and m == "luna" and out == "price")})
    return pd.DataFrame(rows), gaps


def _title(fig):
    return next(a.text for a in fig.layout.annotations if a.name == "title").replace("<br>", " ")


def test_fig_a7_groups_in_ink_labels_and_tested_outcome():
    """FIGURES_SPEC: groups by position and label (never color), 'Names associated with ...' rows, the Black row
    marked where its panel is the pre-registered test, and the need-stated panel draws the tested H3-type gap."""
    cd, gaps = _fake_a7()
    fig, d = X.fig_a7(cd, gaps, {})
    assert {tr.marker.color for tr in fig.data} <= {X.S.INK, X.S.MUTED}
    labs = list(fig.layout.yaxis.ticktext)
    assert all(lab.startswith("Names associated with<br>") for lab in labs)
    assert "pre-registered test (H1)" in labs[1] and "pre-registered test (H4)" in fig.layout.yaxis3.ticktext[1]
    assert "Arab or Middle Eastern buyers" in labs[2] and "MENA" not in _title(fig)
    assert "h3 gap vs White (points)" in set(d["panel"]) and "override" not in set(d["panel"])
    for ax in ("xaxis", "xaxis2", "xaxis3", "xaxis4"):      # same tick text in both engines
        assert fig.layout[ax].ticktext is not None
    assert len([s for s in fig.layout.shapes if s.type == "rect"]) == 2


def test_fig_a7_title_from_tests():
    """The title names only flagged gaps, never calls a null an absence and never ranks estimates."""
    fig, _ = X.fig_a7(*_fake_a7(), {})
    t = _title(fig)
    assert "only names associated with Black buyers on GPT-6 Luna show a flagged gap" in t and "pre-registered" in t
    fig, _ = X.fig_a7(*_fake_a7(flag_luna_black=False), {})
    t = _title(fig)
    assert "none of the gaps" in t
    for bad in ("no gap", "largest", "did not differ", "unbiased"):
        assert bad not in t


def test_fig_a7_ticks_and_hidden_intervals():
    tv, tt = X._ticks(-2.86, 2.96, "%")
    assert tv == [-2, -1, 0, 1, 2] and tt[0] == "−2%" and tt[2] == "0%"
    tv, tt = X._ticks(-0.86, 0.52)
    assert tv == [-0.5, 0, 0.5] and tt == ["−0.5", "0", "0.5"]
    fig, _ = X.fig_a7(*_fake_a7(), {})
    foot = next(a.text for a in fig.layout.annotations if "Marker shape" in (a.text or "")).replace("<br>", " ")
    assert "narrower than the marker" in foot and "ask panel" in foot


def test_fig_a6_ink_and_mismatch_labels():
    a_rows = [{"model": m, "arm": arm, "group": g, "k": 10, "n": 100, "rate": 0.1, "wilson_lo": 0.05,
               "wilson_hi": 0.2, "names": 20} for m in ["haiku", "luna"] for arm in ["S0", "V"] for g, _ in X.A_GROUPS]
    b_rows = [{"model": m, "partial": False, "stated": s, "name_group": g, "k": 1, "n": 100, "rate": 0.01,
               "wilson_lo": 0.0, "wilson_hi": 0.03, "names": 20,
               "mismatch": (s == "STM") == (g == "women's names")}
              for m in ["haiku", "luna"] for s in ["STM", "STW"] for g in ["men's names", "women's names"]]
    fig, _ = X.fig_a6(pd.DataFrame(a_rows), pd.DataFrame(b_rows), {}, ["a caveat"])
    assert {tr.marker.color for tr in fig.data} <= {X.S.INK, X.S.MUTED}
    labs = list(fig.layout.yaxis3.ticktext)
    assert ["mismatch" in lab for lab in labs] == [False, True, True, False]
    foot = next(a.text for a in fig.layout.annotations if "Marker shape" in (a.text or "")).replace("<br>", " ")
    assert "Blue" not in foot and "Caveats: a caveat." in foot


def test_addon_wording():
    """Table B: no-purchase episodes were still asking at the last turn; Table C dollars are raw; Figure A7 sources
    as corrected in d167cbc; the A6 caveats come from the data."""
    src = (ROOT / "analysis" / "addon_analysis.py").read_text()
    assert "chose not to buy" not in src and "still asking at its last turn" in src
    assert "raw mean $ (no cell adjustment)" in src
    cap = X.caption_a7({})
    assert "Table 2 of Oreopoulos 2009" in cap and "weak rater validation" in cap
    assert "2009/2011" not in cap and "validated by" not in cap
    cav = X.neutral_caveats([{"model": "luna", "arm": "S0", "ref": "men's names", "gap_pts": 3.75,
                              "task": "twin_deodorant", "task_pts": 2.34}])
    assert any("separate sessions" in c for c in cav) and any("lean Black" in c for c in cav)
    assert any("2.3 of the 3.8 points" in c and "twin_deodorant" in c for c in cav)
    assert "RACE_COLOR" not in src and "ACCENT" not in src
