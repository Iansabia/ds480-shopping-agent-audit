"""Digitize Gaddis (2017) Figures 1 and 2 (raster bar charts) into per-name rates.

Bars are found by color (red = racially matched last name, blue = no last name,
green = mismatched last name). The 0% and 100% positions come from the chart's
vertical gridlines. Name order was transcribed by eye from the figures (top to bottom).
Accuracy is about +/- 1 percentage point. Run:
  .venv/bin/python -I src/digitize_gaddis.py <fig-000.png> <fig-002.png> <out.csv>
"""
import sys
import numpy as np
import pandas as pd
from PIL import Image

BLACK_ORDER = """Bria Sade Kaylah Lyric Jasmine Nia Kiara Reginald Aniya Hakim Malia Octavia Jalen
Chanel Amari Maurice Quincy Tevin Andre Cedric Shania Malcolm Kimani Savion Wendell Marques Dwayne
Delroy Jabari Leroy Jerome Monique Kevon OVERALL Erykah Jada Jermaine Kenya Aaliyah Divine Marquise
Darius Precious Terell Lamar Darnell Tamia Aisha Keisha Jaleel Ashanti Unique Heaven Taniya Denisha
Kareem Ebony Tyra D'Andre Rasheed Shanice DeShawn Terrell Latonya Tionna Keyana Latoya Jayvon Latrell
Denzel Keyshawn Tyrone DeAndre Tamika Janae Lakisha DaQuan Jamal Tremayne Tanisha DaShawn""".split()
WHITE_ORDER = """Cheyanne Maxwell Mayer Irvin Chloe Edgar Caleb Edwin Deborah Melany Jordy August Ronny
Daniel Brenda Robert Charlie Geoffrey Joan Carrie Charlotte Katie Marlene Lisa Jay OVERALL Brian Lesly
Aubrey Greg Spencer Wyatt Madeline Erica Brad Cassie Angie Cody Mary Brendan Harper Paul Erin Finn
Barbara Graham Luke Anne Steven Allison Susan Heidi Neil Connor Amy Ethan Margaret Meredith Brett
Dustin Hilary Jill Molly Scott Sarah Ryan Emily Kristen Megan Logan Abigail Stephanie Matthew Laurie
Todd Zachary Seth Jake Claire Hunter Katelyn""".split()


REF = {"red": (192, 80, 77), "blue": (79, 129, 189), "green": (155, 187, 89)}


def mask(a, kind):
    d = np.abs(a.astype(int) - np.array(REF[kind])).max(axis=2)
    return d <= 20


def runs(rows_bool):
    idx = np.where(rows_bool)[0]
    if len(idx) == 0:
        return []
    groups, start = [], idx[0]
    for a, b in zip(idx[:-1], idx[1:]):
        if b != a + 1:
            groups.append((start, a)); start = b
    groups.append((start, idx[-1]))
    return groups


def digitize(path, order, signal):
    a = np.array(Image.open(path).convert("RGB"))
    h, w, _ = a.shape
    # gridlines: columns that are mostly mid gray across the plot height
    gray = np.abs(a.astype(int) - 134).max(axis=2) <= 15
    colfrac = gray.mean(axis=0)
    plot_bottom = int(h * 0.95)  # legend sits below the plot
    a = a[:plot_bottom]
    cand = [x for x in range(w) if colfrac[x] > 0.05]
    grid = [g[0] for g in runs(np.isin(np.arange(w), cand))]
    out = {}
    for kind in ("red", "blue", "green"):
        m = mask(a, kind)
        m[:, :60] = False  # ignore name labels left of the axis
        rws = [r for r in runs(m.sum(axis=1) > 3) if r[1] - r[0] >= 2]
        lens = []
        for r0, r1 in rws:
            cols = np.where(m[r0:r1 + 1].any(axis=0))[0]
            lens.append((cols.min(), cols.max()))
        out[kind] = lens
    x0 = np.median([l[0] for l in out["red"]])  # bar origin = 0%
    # 10 gridlines from 10% to 100% (0% axis is the dark axis line)
    right = [g for g in grid if g > x0 + 20]
    step = np.median(np.diff(right))
    x100 = x0 + 10 * step
    print(signal, "rows found", {k: len(v) for k, v in out.items()}, "names", len(order),
          "x0", x0, "step", round(step, 2), "gridlines", len(right))
    recs = []
    for i, name in enumerate(order):
        rec = {"signal": signal, "first": name}
        for kind, col in (("red", "matched_last"), ("blue", "no_last"), ("green", "mismatched_last")):
            if len(out[kind]) == len(order):
                rec[col] = round((out[kind][i][1] + 1 - x0) / (x100 - x0), 3)
        recs.append(rec)
    return recs


if __name__ == "__main__":
    recs = digitize(sys.argv[1], BLACK_ORDER, "Black") + digitize(sys.argv[2], WHITE_ORDER, "White")
    df = pd.DataFrame(recs)
    df.to_csv(sys.argv[3], index=False)
    print(df.to_string())
