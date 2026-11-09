"""Appendix Figure A5: Haiku and Luna were sent the same text in every main run.

For each of the 32,640 main runs, the harness logs a SHA-256 fingerprint of the full text of the
first request (system text + buyer message + store page; runner.py, "prompt_sha256"). This script
matches the two main-run logs run by run (same request type, account, task, wording and product
order) and counts how many fingerprints are equal. It also re-renders one example run from the
frozen inputs, checks that its fingerprint equals the logged one for both models, and prints the
start of that text in panel (a).

Reads:  logs/main_haiku.turns.jsonl.gz, logs/main_luna.turns.jsonl.gz, data/*.json
Writes: paper/figures/figA10_same_inputs.csv, paper/figures/paper/figA10_same_inputs.{pdf,png}
Run:    python analysis/paperfigs/figA10_same_inputs.py
"""
import csv
import gzip
import hashlib
import json
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from matplotlib.patches import FancyBboxPatch
from paperfigs.style import FIGDATA, FULL, GRAY, MODEL, ROOT, plt, save

from harness.catalog import Catalog

NAME = "figA10_same_inputs"
ARMS = [("S0", "Clear request"), ("S1", "Clear request\nplus a budget"), ("V", "Vague request")]
EXAMPLE = ("S0", "BW01", "neutral_keyboard", "w1_fwd")
MONO = ["Menlo", "DejaVu Sans Mono", "Courier New"]


def first_requests(model):
    """episode_id -> (arm, fingerprint) for the first request of every run."""
    out = {}
    with gzip.open(ROOT / "logs" / f"main_{model}.turns.jsonl.gz", "rt") as f:
        for line in f:
            j = json.loads(line)
            if j["turn"] == 0:
                out[j["episode_id"]] = (j["episode"]["arm"], j["prompt_sha256"])
    return out


def compare():
    h, l = first_requests("haiku"), first_requests("luna")
    assert set(h) == set(l), "the two logs do not hold the same runs"
    rows = []
    for arm, _ in ARMS:
        ids = [k for k, v in h.items() if v[0] == arm]
        rows.append({"arm": arm, "n_runs": len(ids),
                     "n_identical": sum(h[k][1] == l[k][1] for k in ids)})
    rows.append({"arm": "all", "n_runs": len(h),
                 "n_identical": sum(h[k][1] == l[k][1] for k in h)})
    with open(FIGDATA / f"{NAME}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["arm", "n_runs", "n_identical"])
        w.writeheader()
        w.writerows(rows)
    return rows, h, l


def example(h, l):
    cat = Catalog()
    ep = cat.make_episode(*EXAMPLE)
    r = cat.render(ep)
    digest = hashlib.sha256((r.system + "\x00" + r.user).encode()).hexdigest()
    assert h[ep.episode_id][1] == digest == l[ep.episode_id][1], "example does not match the logs"
    return ep, r, digest


def excerpt(r):
    acct = r.system[r.system.index("Account holder:"):].splitlines()
    user = r.user.splitlines()
    cut = next(i for i, s in enumerate(user) if s.startswith("2. Product ID"))
    lines = ["You are an AI shopping agent working for the account",
             "holder below. [...]", ""] + acct + [""]
    for s in user[:cut]:
        w = textwrap.wrap(s, 56, subsequent_indent="   ") or [""]
        if s.lstrip().startswith("Details:") and len(w) > 2:    # long product blurb: keep two lines
            w = w[:2] + ["   [...]"]
        lines += w
    n_more = sum(s[:1].isdigit() and ". Product ID" in s for s in user) - 1
    return "\n".join(lines).rstrip() + f"\n\n[... {n_more} more products]"


def make():
    rows, h, l = compare()
    ep, r, digest = example(h, l)
    fig = plt.figure(figsize=(FULL, 3.0))
    ax = fig.add_axes([0.0, 0.0, 0.60, 1.0])
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.0, 0.985, "(a)", fontfamily="STIXGeneral", fontweight="bold", va="top")
    ax.text(0.075, 0.985, "First request of one run, sent to both models", va="top")
    ax.add_patch(FancyBboxPatch((0.01, 0.145), 0.96, 0.775, boxstyle="round,pad=0.004,rounding_size=0.012",
                                fc="0.97", ec=GRAY["light"], lw=0.6))
    ax.text(0.03, 0.905, excerpt(r), va="top", fontsize=5.6, linespacing=1.22,
            fontfamily=MONO, color=GRAY["dark"])
    for y, m in ((0.085, "haiku"), (0.025, "luna")):
        ax.text(0.01, y, f"Fingerprint logged for {MODEL[m]}:", fontsize=6.8, va="center")
        ax.text(0.47, y, digest[:16] + "...", fontsize=6.0, va="center", fontfamily=MONO)
        ax.text(0.80, y, "same" if m == "luna" else "", fontsize=6.8, va="center", style="italic")

    bx = fig.add_axes([0.735, 0.34, 0.215, 0.48])
    labels = [lab for _, lab in ARMS]
    vals = [x["n_identical"] for x in rows[:3]]
    tot = [x["n_runs"] for x in rows[:3]]
    ys = [2, 1, 0]
    bx.barh(ys, tot, height=0.55, color="white", edgecolor=GRAY["mid"], lw=0.6)
    bx.barh(ys, vals, height=0.55, color=GRAY["light"], edgecolor=GRAY["mid"], lw=0.6)
    for y, v, t in zip(ys, vals, tot):
        bx.text(t / 2, y, f"{v:,} of {t:,}", ha="center", va="center", fontsize=7)
    bx.set_yticks(ys)
    bx.set_yticklabels(labels)
    bx.set_xlim(0, max(tot))
    bx.set_xticks([0, max(tot)])
    bx.set_xticklabels(["0", f"{max(tot):,}"])
    bx.set_xlabel("Runs where Haiku and Luna\nwere sent identical text")
    bx.tick_params(axis="y", length=0)
    fig.text(0.625, 0.985, "(b)", fontfamily="STIXGeneral", fontweight="bold", va="top")
    fig.text(0.67, 0.985, "All main runs, by request type", va="top")
    allr = rows[3]
    fig.text(0.84, 0.04, f"Total: {allr['n_identical']:,} of {allr['n_runs']:,}", ha="center", fontsize=8)
    out = save(fig, NAME)
    plt.close(fig)
    print(f"{NAME}: {allr['n_identical']:,} of {allr['n_runs']:,} first requests identical; "
          f"example {ep.episode_id} fingerprint {digest[:16]}")
    return out


if __name__ == "__main__":
    make()
