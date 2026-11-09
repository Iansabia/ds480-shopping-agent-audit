"""OLMo's separate exploratory block and training-data link (PLAN.md D4, D14), on synthetic data."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import analyze as A  # noqa: E402
import olmo_analysis as OL  # noqa: E402
import paper_calc as P  # noqa: E402

FROZEN = ["results/confirmatory.json", "results/confirmatory.md", "results/exploratory.json",
          "results/exploratory.csv", "results/checks.json", "results/addon_exploratory.json"]


@pytest.fixture(scope="module")
def olmo(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("olmo")
    paths = A.synth(tmp / "logs", effect=0.3, h4_effect=0.8, presets=("reduced",),
                    models=("olmo-3:7b-instruct",))
    src = Path(paths["reduced"][0])
    csv = tmp / "logs" / "reduced_olmo.outcomes.csv"
    src.rename(csv)
    n = len(pd.read_csv(csv))
    (tmp / "logs" / "reduced_olmo.manifest.json").write_text(json.dumps(
        {"run": "reduced_olmo", "preset": "reduced", "model_key": "olmo", "n_episodes": n}))
    return {"tmp": tmp, "csv": csv, "df": A.load_outcomes([str(csv)]), "n": n}


def test_complete_run_is_tested_in_its_own_bh_family(olmo):
    st = OL.run_status(olmo["csv"])
    assert st["complete"] and st["finished"] == olmo["n"] and st["model_key"] == "olmo"
    b = OL.block(olmo["df"], st)
    assert b["tested"] and b["n_tests"] == len(b["rows"]) and b["bh_q"] == 0.10
    keys = {r["key"] for r in b["rows"]} | {r["key"] for r in b["untestable"]}
    assert keys == {k for k, *_ in OL.TESTS}
    # q values are BH over this block only
    ps = [r["p"] for r in b["rows"]]
    assert [r["q_bh"] for r in b["rows"]] == pytest.approx(A.bh(ps))
    # the estimates are the frozen name-level machinery (H1 type = analyze.HYPOTHESES H1 on this model)
    h1 = next(r for r in b["rows"] if r["key"] == "h1_price")
    res, _ = A.run_hypothesis(olmo["df"], "olmo", "H1")
    assert h1["est"] == pytest.approx(res.est) and h1["ci_lo"] == pytest.approx(res.ci_lo)
    assert h1["display"] == pytest.approx(100 * (np.exp(res.est) - 1))
    h4 = next(r for r in b["rows"] if r["key"] == "h4_pick")
    res4, _ = A.run_hypothesis(olmo["df"], "olmo", "H4")
    assert h4["est"] == pytest.approx(res4.est) and h4["unit"] == "pts"
    # the planted Black-name price and assume effects show up
    assert h1["est"] > 0 and h1["q_bh"] < 0.10 and h4["est"] > 0


def test_partial_run_gives_estimates_only(olmo):
    df = olmo["df"]
    keep = df["episode_id"].isin(df["episode_id"].drop_duplicates().sample(frac=0.5, random_state=1))
    part = df[keep].reset_index(drop=True)
    st = {"finished": int(part["finished"].sum()), "episodes_expected": olmo["n"], "complete": False}
    b = OL.block(part, st)
    assert not b["tested"] and b["n_tests"] == 0 and b["rows"]
    assert all("p" not in r and "q_bh" not in r for r in b["rows"])
    assert "partial run" in b["status_text"] and "not tested" in b["status_text"]
    t = OL.table_frame(b)
    assert set(t.loc[t["p"] != "", "p"]) == {"not tested"}


def test_outputs_go_only_where_asked_and_numbers_fill(olmo, tmp_path):
    before = {f: (ROOT / f).read_bytes() for f in FROZEN if (ROOT / f).exists()}
    res = OL.run(olmo["tmp"] / "logs", tmp_path / "res", tmp_path / "tab")
    assert (tmp_path / "res" / "olmo_exploratory.json").exists()
    md = (tmp_path / "tab" / "olmo_exploratory.md").read_text()
    assert "separate exploratory block" in md and "own Benjamini-Hochberg family" in md
    assert {f: (ROOT / f).read_bytes() for f in before} == before          # frozen files untouched
    j = json.loads((tmp_path / "res" / "olmo_exploratory.json").read_text())
    assert j["tested"] and j["training_link"]["rho"] == pytest.approx(res["rho"])
    link = OL.training_link(olmo["df"])
    N = OL.numbers(OL.block(olmo["df"], OL.run_status(olmo["csv"])), link)
    for k, *_ in OL.TESTS:
        assert N[f"olmo.{k}.est"] and N[f"olmo.{k}.q"] != "n/a" or N[f"olmo.{k}.est"] == A.NO_VARIATION
    assert N["olmo.rho"] == f"{link['rho']:.2f}" and "traced, correlation only" in N["olmo.training_link_sentence"]
    assert "Ai2's OLMo 3 32B Instruct index" in N["olmo.training_link_sentence"]
    for v in N.values():
        assert "\u2014" not in v and "\u2013" not in v


def test_numbers_say_pending_without_olmo():
    N = OL.numbers(None, None)
    assert N["olmo.status"].startswith("pending") and N["olmo.training_link_sentence"] == "not run"
    assert N["olmo.rho"].startswith("n/a") and N["olmo.h1_price.est"].startswith("pending")


def test_training_link_rho_and_sensitivities(olmo, tmp_path):
    df = olmo["df"]
    nm = OL.name_gaps(df).merge(A.load_names()[["profile_id", "first"]], on="profile_id")
    assert len(nm) == 40 and set(nm["race"]) == {"Black", "White"}
    # counts that track the gap on the OLMo 3 index, and the reverse on the OLMo 2 index; two names flagged
    order = nm.sort_values("gap_pct")["first"].tolist()
    flagged = set(order[:2])
    rows = []
    for i, f in enumerate(order):
        rows.append({"first": f, "index": OL.INDEX_PRIMARY, "count": 1000 * (i + 1) ** 2,
                     "word_ambiguity_flag": "common word" if f in flagged else ""})
        rows.append({"first": f, "index": OL.INDEX_OLMO2, "count": 1000 * (40 - i) ** 2,
                     "word_ambiguity_flag": "common word" if f in flagged else ""})
    rows.append({"first": "Nobody", "index": "v4_piletrain_llama", "count": 5, "word_ambiguity_flag": ""})
    cp = tmp_path / "counts.csv"
    pd.DataFrame(rows).to_csv(cp, index=False)
    link = OL.training_link(df, cp)
    assert link["n"] == 40 and link["rho"] == pytest.approx(1.0)
    assert link["olmo2"]["rho"] == pytest.approx(-1.0)
    assert link["unflagged"]["n"] == 38 and sorted(link["unflagged"]["dropped"]) == sorted(flagged)
    x = link["names"]
    ref = stats.spearmanr(np.log1p(x["raw_count"]), x["gap_pct"])
    assert link["p"] == pytest.approx(ref.pvalue)
    assert OL.training_link(df[df["model"] != "olmo"], cp) is None
    assert OL.training_link(df, tmp_path / "missing.csv") is None


def test_real_counts_file_has_both_indexes_for_every_core_name():
    c = OL.load_counts()
    names = A.load_names()
    core = set(names[names["profile_id"].str.match(r"^[BW][WM]\d")]["first"])
    for idx in (OL.INDEX_PRIMARY, OL.INDEX_OLMO2):
        got = set(c[c["index"] == idx]["first"])
        assert core <= got, (idx, core - got)
    assert not (A.DATA / "name_freq.csv").exists()      # the frozen SSA covariate stays in force


def test_late_runs_are_left_out_of_the_frozen_hash_match(tmp_path):
    a, o = tmp_path / "main_x.outcomes.csv", tmp_path / "reduced_olmo.outcomes.csv"
    a.write_text("episode_id,outcome\n1,bought\n")
    o.write_text("episode_id,outcome\n1,bought\n")
    (tmp_path / "main_x.manifest.json").write_text(json.dumps({"model_key": "haiku", "preset": "main"}))
    (tmp_path / "reduced_olmo.manifest.json").write_text(json.dumps({"model_key": "olmo", "preset": "reduced"}))
    assert P.is_late_run(o) and not P.is_late_run(a)
    res = tmp_path / "results"
    res.mkdir()
    h = A.file_hashes([str(a)])
    for name in ("checks", "confirmatory", "exploratory"):
        (res / f"{name}.json").write_text(json.dumps({"inputs": h}))
    b = P.analysis_bundle([a, o], None, {}, False, ["haiku"], res, 0, 0)
    assert b["late_runs"] == ["reduced_olmo.outcomes.csv"]
    # a non-late extra run still fails the match
    x = tmp_path / "main_y.outcomes.csv"
    x.write_text("episode_id,outcome\n2,bought\n")
    (tmp_path / "main_y.manifest.json").write_text(json.dumps({"model_key": "luna", "preset": "main"}))
    with pytest.raises(SystemExit):
        P.analysis_bundle([a, x], None, {}, False, ["haiku"], res, 0, 0)


def test_figure_a3_draws_from_the_olmo_counts_and_skips_without_olmo(olmo, tmp_path):
    import make_figures as MF
    out = MF.Out(tmp_path / "fig", tmp_path / "tab", pilot=False)
    st = [{"path": str(olmo["csv"]), "model_key": "olmo"}]
    b = MF.olmo_block(out, olmo["df"], st)
    assert b["tested"] and (tmp_path / "tab" / "olmo_exploratory.md").exists()
    link = MF.figA3_training(out, olmo["df"])
    assert "figA3" in out.figs and link["rho"] is not None
    cap = out.figs["figA3"]["caption"]
    assert "OLMo 3 pretraining data (shared base, via Ai2's 32B Instruct index)" in cap
    assert "traced, correlation only" in cap and "OLMo 2" in cap
    d = pd.read_csv(out.figs["figA3"]["csv"])
    assert len(d) == 40 and d["spearman_rho"].iloc[0] == pytest.approx(link["rho"])
    out2 = MF.Out(tmp_path / "fig2", tmp_path / "tab2", pilot=False)
    none = olmo["df"].assign(model="haiku")
    assert MF.olmo_block(out2, none, []) is None and MF.figA3_training(out2, none) is None
    assert "figA3" in out2.skipped and "pending" in out2.skipped["figA3"]
    # pilot data never gets a test, even for a finished run
    out3 = MF.Out(tmp_path / "fig3", tmp_path / "tab3", pilot=True)
    assert not MF.olmo_block(out3, olmo["df"], st)["tested"]


def test_figure_a4_reads_olmo_asked_first_from_its_block(olmo, tmp_path, monkeypatch):
    """Verifier fix: OLMo is not in the frozen exploratory family, so A4's Asked first cell comes from the OLMo
    block (never 'no name variation' when names differ), and Over budget says 'no runs' (no S1 arm), not flat."""
    import make_figures as MF
    import figstyle as S
    seen = {}
    monkeypatch.setattr(S, "save", lambda fig, *a, **k: seen.setdefault("fig", fig) and {})
    df = olmo["df"].copy()
    df = df[df["arm"] != "S1"]                      # the reduced preset has no S1 for OLMo
    rng = np.random.default_rng(3)
    v = df["arm"] == "V"
    df.loc[v, "asked"] = rng.integers(0, 2, v.sum())  # asked varies by name
    out = MF.Out(tmp_path / "fig", tmp_path / "tab", pilot=False)
    b = OL.block(df, {"complete": False, "finished": 10, "episodes_expected": 100}, test=False)
    ask = next(r for r in b["rows"] if r["key"] == "v_ask_race")
    bundle = {"confirmatory": {"rows": []}, "exploratory": {"tests": []}}
    MF.figA4_scorecard(out, df, ["olmo"], [], bundle, {}, b)
    t = pd.read_csv(out.figs["figA4"]["csv"])
    r = t[(t["model"] == "olmo") & (t["outcome"] == "race: V ask rate")]
    assert len(r) == 1 and r["est"].iloc[0] == pytest.approx(ask["display"])
    assert r["family"].iloc[0] == "OLMo block, not tested"
    txt = " ".join(a.text for a in seen["fig"].layout.annotations if a.text)
    assert "OLMo Asked first" not in txt                         # no false 'every name had the same result'
    assert "own exploratory block (D14)" in txt
    assert "Over budget" in txt.split("Not shown")[1]       # no S1 anywhere: column left out, never 'flat'
    assert "every name had the same result" not in txt
