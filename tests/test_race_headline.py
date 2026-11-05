"""Six-group headline figure and omnibus test (PLAN.md D12), and the one dollar definition."""
import html
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

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


def test_omnibus_adds_a_without_black_sensitivity_and_keeps_the_main_draws(monkeypatch):
    import addon_analysis as X
    y, race, woman = _names({"Black": -0.03})
    nm = pd.DataFrame({"race": race, "mean": y, "is_woman": woman})
    monkeypatch.setattr(X, "named", lambda dm, model, arms: pd.DataFrame({"logp": [0.0]}))
    monkeypatch.setattr(RH.A, "name_means", lambda d, col: nm.copy())
    df = pd.DataFrame({"model": ["luna"], "preset": ["main"]})
    o = RH.omnibus(df, "luna", n_perm=200, seed=480)
    # main test: the same numbers as one call on the same seed (the sensitivity draws come after, on their own rng)
    f, q, dfr, hits = RH._perm_f(y, race, woman, RH.RACES, 200, np.random.default_rng(480))
    assert (o["F"], o["df1"], o["df2"], o["perm_hits"]) == (f, q, dfr, hits) and o["p_perm"] == (hits + 1) / 201
    w = o["without_black"]
    assert set(w) >= {"F", "df1", "df2", "p_F", "p_perm", "perm_hits", "n_names", "groups"}
    assert "Black" not in w["groups"] and w["df1"] == 4 and w["n_names"] == len(y) - 20 and w["df2"] == w["n_names"] - 6
    # the planted gap is Black only, so the main test finds it and the test without Black names does not
    assert o["p_perm"] < 0.05 and w["p_perm"] > 0.05
    om = {"luna": o}
    assert "F(4, " in RH.omnibus_text(om, part="without_black") and "F(5, " in RH.omnibus_text(om)


def test_title_and_sentence_never_state_a_null_as_an_absence():
    t = pd.DataFrame({"model": ["luna"] * 3, "race": ["White", "Black", "Asian"], "gap_pct": [0.0, -1.8, -0.2]})
    none = {"haiku": {"p_perm": 0.76}, "luna": {"p_perm": 0.20}}
    title = RH.headline_title(t, none)
    assert title.startswith("Exploratory six-group test: no evidence of a price difference")
    assert "Haiku (p = .760)" in title and "Luna (p = .200)" in title
    some = {"haiku": {"p_perm": 0.76}, "luna": {"p_perm": 0.01}}
    title = RH.headline_title(t, some)
    assert "Exploratory" in title and "differs" in title and "Luna (p = .010" in title
    assert "every group's estimate is below White names" in title
    assert "no evidence of a difference on Haiku (p = .760)" in title
    s = RH.six_group_sentence(t, some)
    assert "GPT-6 Luna's prices differed (p = .010), with every group's estimate below White names" in s
    assert "for Claude Haiku 5.5 there was no evidence of a difference (p = .760)" in s
    for text in (title, s, RH.headline_title(t, none), RH.six_group_sentence(t, none)):
        for bad in ("did not", "not on", "No price difference", "paying less", "\u2014", "\u2013"):
            assert bad not in text


def test_side_clause_only_when_every_estimate_is_on_one_side():
    t = pd.DataFrame({"model": ["luna"] * 3, "race": ["White", "Black", "Asian"], "gap_pct": [0.0, -1.8, 0.4]})
    some = {"haiku": {"p_perm": 0.76}, "luna": {"p_perm": 0.01}}
    assert "every group" not in RH.headline_title(t, some) and "every group" not in RH.six_group_sentence(t, some)


def test_adjusted_p_text_to_number():
    assert RH._adj_num("q .173") == pytest.approx(0.173) and RH._adj_num("Holm p 1.000") == 1.0
    assert RH._adj_num("Holm p <.001") < 0.001 and np.isnan(RH._adj_num("not tested")) and np.isnan(RH._adj_num(None))


@pytest.fixture(scope="module")
def built():
    if not (RH.TAB / "addon_C_race_gaps.csv").exists():
        pytest.skip("add-on race tables missing")
    t = RH.headline_rows({"haiku": 26.47, "luna": 31.22, "flashlite": 26.48})
    def res(p, df1, n):
        return {"p_perm": p, "F": 1.0, "df1": df1, "df2": n - df1 - 2, "p_F": p, "perm_hits": 9, "n_perm": 999,
                "n_names": n}
    om = {m: {**res(p, 5, 82), "without_black": res(0.3, 4, 62)} for m, p in (("haiku", 0.76), ("luna", 0.01))}
    fig, cap = RH.figure(t, om)
    return t, om, fig, cap


def test_right_panel_draws_the_tested_gap_from_table_c(built):
    t, _, fig, _ = built
    g = pd.read_csv(RH.TAB / "addon_C_race_gaps.csv")
    g = g[g.outcome == "h4"].dropna(subset=["gap_display"])
    rows = t.dropna(subset=["h4_gap_pts"]).merge(g, on=["model", "race"])
    assert len(rows) == len(g) and "White" not in set(rows["race"])
    assert np.allclose(rows["h4_gap_pts"], rows["gap_display"]) and np.allclose(rows["h4_gap_lo"], rows["lo_display"])
    conf = {r["model"]: r for r in json.loads((RH.RES / "confirmatory.json").read_text())["rows"]
            if r["hypothesis"] == "H4"}
    for m, r in conf.items():   # the shaded Black row is the confirmatory H4
        b = t[(t.model == m) & (t.race == "Black")].iloc[0]
        assert b["h4_gap_pts"] == pytest.approx(100 * r["r_est"]) and b["h4_source"] == "confirmatory H4"
    # what the right panel draws: exactly the tested gaps (not the pooled shares), with a zero line
    drawn = sorted(float(x) for tr in fig.data if tr.xaxis == "x2" for x in tr.x)
    assert drawn == pytest.approx(sorted(rows["h4_gap_pts"]))
    assert any(s.type == "line" and s.xref == "x2" and s.x0 == 0 for s in fig.layout.shapes)
    # Gemini rows are descriptive: open markers
    gem = [tr for tr in fig.data if tr.xaxis == "x2" and tr.marker.symbol.endswith("-open")]
    assert len(gem) == len(rows[rows.model == "flashlite"])


def test_figure_text_labels_and_footer(built):
    _, _, fig, cap = built
    texts = [a.text for a in fig.layout.annotations]
    foot = next(a.text for a in fig.layout.annotations if "Pre-registered" in a.text)
    sub = next(a.text for a in fig.layout.annotations if a.name == "subtitle")
    flat = html.unescape(foot.replace("<br>", " "))
    assert not foot.startswith("Exploratory") and "H1 left (Haiku Holm p 1.000, Luna Holm p <.001)" in flat
    assert "H4 right (Haiku Holm p .379, Luna Holm p <.001)" in flat
    assert "added after the main results were seen" in flat and "without names associated with Black buyers" in flat
    assert "<" not in foot.replace("<br>", "")   # text "<" goes in as &lt; (a wrapped line may start with it)
    assert "Claude Haiku 5.5" in sub and "GPT-6 Luna" in sub and "◇ Gemini 3.5 Flash-Lite" in sub
    assert all(lab.startswith("<span") and "Names associated with" in lab for lab in fig.layout.yaxis.ticktext)
    assert "names associated with White buyers" in fig.layout.xaxis.title.text
    assert "names associated with White buyers" in fig.layout.xaxis2.title.text
    for txt in texts + [cap]:
        assert "D12" not in txt and "PLAN" not in txt and "\u2014" not in txt and "\u2013" not in txt


def test_table_labels_pooled_shares(built, tmp_path):
    t, om, _, _ = built
    RH.write_table(t, om, tmp_path)
    md = (tmp_path / "race_headline.md").read_text()
    assert "Pooled share (not adjusted)" in md and "not the tested gap" in md
    assert "Sensitivity, same test with names associated with Black buyers left out: F(4, 56)" in md
    assert "D12" not in md


def test_one_dollar_definition():
    ref = {"ref_usd": 31.22, "focal_usd": 30.78}
    tr = P.dollar_translation(np.log(1 - 0.018), np.log(1 - 0.026), np.log(1 - 0.009), 31.22)
    u = P.unify_focal(ref, tr)
    assert abs((u["ref_usd"] - u["focal_usd"]) - (-tr["usd_per_purchase"])) < 1e-12
    assert u["focal_usd_cellmean"] == 30.78 and abs(u["focal_usd"] - 30.658) < 0.01
