"""Tests for the paper figure and number code (analysis/make_figures.py,
analysis/paper_calc.py). No API calls; synthetic logs only.

Checks:
  - the dollar translation and the t interval are computed as FIGURES_SPEC says
  - number formatting never prints "-0.0" or a bare group label
  - runs still being written are skipped
  - the appendix figures reproduce analyze.py's frozen PLAN 10 numbers exactly
  - the Figure 5D p-values give the same reject share as analyze.shuffled_null
  - pilot output is watermarked everywhere; main output is not, and main mode
    refuses to run without analyze.py's results for the same input files
  - numbers.json carries every result key paper/DRAFT.md uses
"""
import argparse
import json
import math
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import analyze as A  # noqa: E402
import make_figures as MF  # noqa: E402
import paper_calc as P  # noqa: E402

TASKS = 6   # synthetic grids cut to the first 6 tasks to keep the test fast


# ----------------------------------------------------------------------------- unit checks

def test_dollar_translation():
    tr = P.dollar_translation(math.log(1.10), math.log(1.00), math.log(1.21), 20.0)
    assert tr["gap_pct"] == pytest.approx(10.0)
    assert tr["usd_per_purchase"] == pytest.approx(2.0)
    assert tr["usd_per_1000"] == pytest.approx(2000.0)
    assert tr["usd_ci"] == pytest.approx([0.0, 4.2])
    assert tr["usd_per_1000_ci"] == pytest.approx([0.0, 4200.0])
    neg = P.dollar_translation(math.log(0.95), math.log(0.9), math.log(1.0), 16.75)
    assert neg["usd_per_purchase"] == pytest.approx(-0.8375)


def test_t_interval_matches_scipy():
    v = np.array([1.0, 2.5, 3.0, 4.5, 2.0])
    ti = P.t_interval(v)
    lo, hi = stats.t.interval(0.95, len(v) - 1, loc=v.mean(), scale=stats.sem(v))
    assert ti["est"] == pytest.approx(v.mean())
    assert (ti["lo"], ti["hi"]) == pytest.approx((lo, hi))
    assert math.isnan(P.t_interval([1.0])["lo"])


def test_group_labels_name_not_people():
    for g in P.CORE_GROUPS:
        lab = P.group_label(g)
        assert lab.startswith("Names associated with") or lab == "No name on the account"


def test_formatting():
    assert "-0.0" not in MF.f_pct(-1e-16)
    assert "-0.0" not in MF.f_range(-1e-15, 1e-15, "pts")
    assert MF.f_usd(-0.3449) == "-$0.34"
    assert MF.f_usd(335.2, 0) == "+$335"
    assert MF.f_p(0.0004) == "< 0.001"
    assert MF.f_usd(float("nan")) == "n/a"


def test_select_runs_skips_live(tmp_path):
    (tmp_path / "done.outcomes.csv").write_text("x\n")
    (tmp_path / "done.turns.jsonl").write_text("{}\n")
    old = time.time() - 3600
    os.utime(tmp_path / "done.turns.jsonl", (old, old))
    (tmp_path / "live.outcomes.csv").write_text("x\n")
    os.utime(tmp_path / "live.outcomes.csv", (old, old))
    (tmp_path / "live.turns.jsonl").write_text("{}\n")          # written just now, after its scored file
    use, skipped = MF.select_runs(["done", "live", "absent"], tmp_path, 10)
    assert [p.name for p in use] == ["done.outcomes.csv"]
    assert {s["run"] for s in skipped} == {"live", "absent"}


# ----------------------------------------------------------------------------- synthetic world

@pytest.fixture(scope="module")
def world(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("mf")
    paths = A.synth(tmp / "logs", effect=0.06, h3_effect=0.8, h4_effect=0.8, seed=480, task_limit=TASKS,
                    presets=("pilot", "main", "planted", "validity", "m1"))
    for preset, ps in paths.items():
        if preset == "truth":
            continue
        for p in ps:
            run = Path(p).name.replace(".outcomes.csv", "")
            n = len(pd.read_csv(p))
            mk = A.MODEL_KEYS.get(run.split("_", 2)[2], run)
            Path(p.replace(".outcomes.csv", ".manifest.json")).write_text(json.dumps(
                {"run": run, "preset": preset, "model_key": mk, "n_episodes": n}))
            old = time.time() - 3600
            tp = Path(p.replace(".outcomes.csv", ".turns.jsonl"))
            os.utime(tp, (old, old))
    ns = argparse.Namespace(results=str(tmp / "results"), data=str(A.DATA), mde=None,
                            confirm_models=["synth_a", "synth_b"], perms=200, shuffles=100,
                            pilot=paths["pilot"], family_size=None)
    A.cmd_mde(ns)
    return {"tmp": tmp, "paths": paths, "ns": ns}


def _main_paths(w):
    return [p for k, v in w["paths"].items() if k not in ("pilot", "truth") for p in v]


def test_pilot_build_is_watermarked(world, monkeypatch):
    tmp = world["tmp"]
    res = MF.build(world["paths"]["pilot"], tmp / "results" / "mde.json", tmp / "pilot_fig", tmp / "pilot_tab",
                   tmp / "nowhere", ["synth_a", "synth_b"], n_perm=200, shuffles=100, idle_minutes=10,
                   logs=tmp / "logs")
    assert res["pilot"]
    assert not (tmp / "nowhere").exists()                       # pilot never writes analyze.py results
    pngs = sorted((tmp / "pilot_fig").glob("*.png"))
    assert pngs
    for p in pngs:
        assert p.name == "fig2_design.png" or p.stem.endswith("_PILOT"), p.name
    for c in (tmp / "pilot_fig").glob("*.csv"):
        assert pd.read_csv(c)["watermark"].eq(P.WATERMARK).all()
    for t in (tmp / "pilot_tab").glob("*.md"):
        assert P.WATERMARK in t.read_text()
    n = json.loads((tmp / "pilot_tab" / "numbers_PILOT.json").read_text())
    assert n["_meta"]["watermark"] == P.WATERMARK
    assert P.WATERMARK in (tmp / "pilot_fig" / "CAPTIONS_PILOT.md").read_text()
    # every figure file stem in numbers.json exists, with svg and png
    for k, rec in n["_meta"]["figures"].items():
        assert Path(rec["png"]).exists() and Path(rec["svg"]).exists() and Path(rec["html"]).exists()
    # pilot figures never print a verdict or a dollar translation of a group gap
    fig4 = (tmp / "pilot_fig" / "fig4_price_gap_PILOT.html").read_text()
    assert "PILOT DATA, NOT RESULTS" in fig4
    # figure text is plain English: no plan section numbers, file names or deviation codes, and no
    # p-value on a pilot figure, not even for a method check
    for h in (tmp / "pilot_fig").glob("*.html"):
        body = h.read_text()
        assert not re.search(r"PLAN \d|analyze\.py|Deviation D\d|sn_p80|mde\.json", body), h.name
        assert not re.search(r"\bp 0\.\d|Holm p:", body), h.name


def test_main_build_matches_frozen_outputs(world, monkeypatch):
    tmp = world["tmp"]
    ns = world["ns"]
    monkeypatch.setattr(A, "MAIN_GRID_EPISODES", 10)            # cut grid; let both synthetic models enter the family
    ns.outcomes = _main_paths(world)
    figdir, tabdir = tmp / "main_fig", tmp / "main_tab"
    with pytest.raises(SystemExit):                             # analyze.py has not run yet
        MF.build(ns.outcomes, tmp / "results" / "mde.json", figdir, tabdir, tmp / "results_main",
                 ["synth_a", "synth_b"], 200, 100, 10, tmp / "logs")
    ns.results = str(tmp / "results_main")
    import shutil
    (tmp / "results_main").mkdir(exist_ok=True)
    shutil.copy(tmp / "results" / "mde.json", tmp / "results_main" / "mde.json")
    A.cmd_all(ns)
    res = MF.build(ns.outcomes, tmp / "results_main" / "mde.json", figdir, tabdir, tmp / "results_main",
                   ["synth_a", "synth_b"], 200, 100, 10, tmp / "logs")
    assert not res["pilot"]
    assert not list(figdir.glob("*_PILOT*")) and not list(tabdir.glob("*_PILOT*"))
    n = json.loads((tabdir / "numbers.json").read_text())
    assert n["_meta"]["watermark"] is None
    for key in ("fig1", "fig2", "fig3", "fig4", "fig5", "fig6", "fig7", "fig8", "figA1", "figA2", "figA4"):
        assert key in n["_meta"]["figures"], key

    # numbers come from analyze.py's confirmatory.json
    conf = json.loads((tmp / "results_main" / "confirmatory.json").read_text())
    r = next(r for r in conf["rows"] if r["model"] == "synth_a" and r["hypothesis"] == "H1")
    f3 = pd.read_csv(figdir / "fig4_price_gap.csv")
    row = f3[(f3.model == "synth_a") & (f3.hypothesis == "H1")].iloc[0]
    assert row["est_log"] == pytest.approx(r["r_est"])
    assert row["gap_pct"] == pytest.approx(100 * (math.exp(r["r_est"]) - 1))
    assert row["usd_per_purchase"] == pytest.approx((math.exp(r["r_est"]) - 1) * row["ref_usd"])
    assert row["usd_per_1m"] == pytest.approx(1e6 * (math.exp(r["r_est"]) - 1))

    # appendix figures reproduce analyze.py's frozen PLAN 10 tables
    df = A.load_outcomes(ns.outcomes)
    frozen = A.figures(df, json.loads((tmp / "results_main" / "mde.json").read_text()), ["synth_a", "synth_b"],
                       tmp / "frozen_figs")
    assert frozen
    a2 = pd.read_csv(figdir / "figA2_price_vs_no_name.csv").sort_values(["model", "arm", "group"]).reset_index(drop=True)
    f1 = pd.read_csv(tmp / "frozen_figs" / "fig1_price_gap_by_group.csv").sort_values(["model", "arm", "group"]).reset_index(drop=True)
    np.testing.assert_allclose(a2["est_pct"], f1["est_pct"])
    np.testing.assert_allclose(a2["lo_pct"], f1["lo_pct"])
    a1 = pd.read_csv(figdir / "figA1_position_bias.csv").sort_values(["model", "order", "position"]).reset_index(drop=True)
    fa1 = pd.read_csv(tmp / "frozen_figs" / "figA1_pick_share_by_position.csv").sort_values(
        ["model", "order", "position"]).reset_index(drop=True)
    np.testing.assert_allclose(a1["share"], fa1["share"])
    f4 = pd.read_csv(figdir / "fig6_hair_skin_fit.csv")
    fb = pd.read_csv(tmp / "frozen_figs" / "fig2b_wrong_need_when_assumed.csv")
    mine = f4[f4.panel == "B"].set_index(["model", "group"])["est"].sort_index()
    theirs = fb[fb.split == "identity-linked need"].set_index(["model", "group"])["est"].sort_index()
    np.testing.assert_allclose(mine.to_numpy(), theirs.loc[mine.index].to_numpy())

    # Figure 5D p-values give the same reject share as the frozen shuffled-null check
    ch = json.loads((tmp / "results_main" / "checks.json").read_text())
    ps = P.shuffled_pvalues(df, "synth_a", "H1", n=ns.shuffles)
    assert np.mean(np.array(ps) < 0.05) == pytest.approx(ch["shuffled_null"]["synth_a"]["H1"]["reject_rate"])

    # numbers.json carries every result key the draft uses (genai keys are Ian's, template keys are examples)
    draft = (ROOT / "paper" / "DRAFT.md").read_text()
    keys = set(re.findall(r"\{\{([^}]*)\}\}", draft))
    ignore = {"placeholder", "model", "group", "gap_usd", "gap_per1000_usd"}
    missing = [k for k in keys if k not in n and not k.startswith("genai.") and k not in ignore]
    assert not missing, missing


# ----------------------------------------------------------------------------- engines and watermark styles

def _small_fig():
    import plotly.graph_objects as go
    import figstyle as S
    fig = go.Figure()
    S.dots(fig, [20.1, 19.8], [0, 1], [18.7, 18.6], [21.5, 21.1], S.gcolor("Black woman"))
    fig.add_trace(go.Bar(x=[1, 2], y=[3.0, 0.0], error_y=dict(type="data", array=[1.0, 2.0], arrayminus=[0.5, 0.0])))
    S.layout(fig, "A takeaway title", "Method and n. Costs < 0.05 of the total.", True, 420, bottom=60, left=80)
    S.footer(fig, "Footer note.")
    return fig


def test_plotly_and_matplotlib_engines(tmp_path):
    import figstyle as S
    from PIL import Image
    fig = _small_fig()
    before = fig.to_json()
    p = S.save(fig, tmp_path, "demo", True, [], engine="plotly")
    m = S.save(fig, tmp_path, "demo", True, [], engine="matplotlib")
    assert fig.to_json() == before                                   # save never changes the figure passed in
    assert Path(p["png"]).name == "demo_PILOT.png" and Path(p["html"]).exists()
    assert Path(m["png"]).name == "demo_PILOT_mpl.png" and Path(m["svg"]).name == "demo_PILOT_mpl.svg"
    assert m["html"] is None
    a, b = Image.open(p["png"]), Image.open(m["png"])
    assert a.size == b.size                                          # same canvas: 300 dpi = Plotly scale 3
    assert round(b.info["dpi"][0]) == 300
    svg = Path(m["svg"]).read_text()
    assert P.WATERMARK in svg and "A takeaway title" in svg
    assert "Costs &lt; 0.05" in svg                                  # "<" in text is text, not an HTML tag
    assert "Click to enter" not in svg                               # no Plotly editor placeholders


def test_watermark_styles(tmp_path):
    import figstyle as S
    fig = _small_fig()
    for style in S.WM_STYLES:
        r = S.save(fig, tmp_path, "demo", True, [], engine="matplotlib", wm_style=style, variant=f"_wm-{style}")
        assert Path(r["png"]).name == f"demo_PILOT_wm-{style}_mpl.png"
        assert P.WATERMARK in Path(r["svg"]).read_text()
    corner = S.save(fig, tmp_path, "c", True, [], engine="plotly", wm_style="corner")
    diag = S.save(fig, tmp_path, "d", True, [], engine="plotly", wm_style="diagonal")
    ch, dh = Path(corner["html"]).read_text(), Path(diag["html"]).read_text()
    assert '"pilot-mark"' in ch and '"pilot-stamp"' not in ch
    assert '"pilot-stamp"' in dh and '"pilot-mark"' not in dh
    with pytest.raises(ValueError):
        S.save(fig, tmp_path, "x", True, [], wm_style="sideways")
    main = S.save(fig, tmp_path, "m", False, [], engine="plotly")    # main data: no watermark at all
    assert P.WATERMARK not in Path(main["html"]).read_text()
