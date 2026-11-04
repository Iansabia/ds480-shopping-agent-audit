"""Build the name set and account profiles (design 5.3, 5.10).

Rules: data/NAME_SELECTION_RULES.md (original rules plus Amendment 1).
Inputs (data/raw, git-ignored): crabtree/, ssa/ext/, gaddis/gaddis_rates_digitized.csv,
gaddis/table1_fonts_raw.csv, census_surnames/ext/, elder_hayes/.
Outputs: data/names.csv, data/profiles.json, data/cell_balance.csv.
Run: .venv/bin/python -I src/build_names.py
"""
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data"

CRABTREE_CUTOFF = 0.70
GADDIS_CUTOFF = 0.85
TZIOUMIS_MIN, TZIOUMIS_OBS = 90.0, 30  # Amendment 2 (was 100)
FEM_MIN, MALE_MAX, MIN_BIRTHS = 0.95, 0.05, 1000
YEARS = range(1950, 2006)
CORE_N, EXT_N, N_ALT = 10, 6, 3
SEED = 20261104
ZIP = "43215"
BIRTH_YEARS = [1978, 1998]

# Surnames that mainly signal a national origin or religion (Amendment 1, rule 5).
SURNAME_DROP = {
    "PIERRE", "JEAN", "LOUIS", "FRANCOIS", "JOSEPH", "CHARLES", "JEAN-BAPTISTE", "ETIENNE",
    "DESIR", "JOSEPH", "MOHAMED", "MUHAMMAD", "MOHAMMED", "AHMED", "ALI", "HASSAN", "IBRAHIM",
    "ABDI", "OSMAN", "COHEN", "SCHWARTZ", "KLEIN", "FRIEDMAN", "LEVY", "KATZ", "SHAPIRO",
    "OBRIEN", "OCONNOR", "OCONNELL", "ONEILL", "ONEAL", "OBRYAN", "ODONNELL",  # apostrophe lost
}
# Rule 6: full names of widely known public figures, filled by hand after review.
FAMOUS = set()
CODE = {"Black": "B", "White": "W", "Hispanic": "H", "Asian": "A", "woman": "W", "man": "M"}


def ssa_gender():
    s = pd.concat(pd.read_csv(RAW / "ssa" / "ext" / f"yob{y}.txt", header=None,
                              names=["first", "sex", "n"]) for y in YEARS)
    s = s.groupby(["first", "sex"])["n"].sum().unstack(fill_value=0)
    s["births"] = s["F"] + s["M"]
    s["female_share"] = s["F"] / s["births"]
    return s[["births", "female_share"]]


def gender_of(births, fshare):
    if pd.isna(births) or births < MIN_BIRTHS:
        return None
    if fshare >= FEM_MIN:
        return "woman"
    if fshare <= MALE_MAX:
        return "man"
    return None


def census_surnames():
    c = pd.read_csv(RAW / "census_surnames" / "ext" / "Names_2010Census.csv", na_values=["(S)"])
    c = c[c["name"] != "ALL OTHER NAMES"]
    c = c[~c["name"].isin(SURNAME_DROP)]
    black = c[(c.pctblack >= 50) & (c["count"] >= 10000)].sort_values("count", ascending=False)
    white = c[(c.pctwhite >= 90) & (c["count"] >= 30000)].sort_values("count", ascending=False)
    return black, white


def main():
    ssa = ssa_gender()
    picked = {}  # cell -> list of dict rows
    used_first = set()

    # ---------- Core cells: Gaddis 2017 ----------
    g = pd.read_csv(OUT / "derived" / "gaddis_rates_digitized.csv")
    g = g[g["first"] != "OVERALL"]
    f = pd.read_csv(OUT / "derived" / "gaddis_table1_fonts.csv").rename(columns={"text_a": "first"})
    f["first"] = f["first"].str.replace("’", "'")
    g = g.merge(f[["first", "style"]].drop_duplicates("first"), on="first", how="left")
    g["ssa_key"] = g["first"].str.replace("'", "")
    g = g.merge(ssa, left_on="ssa_key", right_index=True, how="left")
    g["gender"] = [gender_of(b, s) for b, s in zip(g.births, g.female_share)]
    elig = g[(g.matched_last >= GADDIS_CUTOFF) & (g["style"] == "regular") & g.gender.notna()]

    black_s, white_s = census_surnames()
    rng = random.Random(SEED)
    surname_pool = {"Black": black_s["name"].tolist(), "White": white_s["name"].tolist()}
    surname_meta = pd.concat([black_s, white_s]).set_index("name")

    for race in ["Black", "White"]:
        for gender in ["woman", "man"]:
            cand = elig[(elig.signal == race) & (elig.gender == gender)].sort_values(
                ["matched_last", "first"], ascending=[False, True])
            rows = []
            for rec in cand.to_dict("records"):
                if rec["first"] in used_first:
                    continue
                rows.append(rec); used_first.add(rec["first"])
                if len(rows) == CORE_N + N_ALT:
                    break
            picked[(race, gender)] = rows
    for race in ["Black", "White"]:
        cells = [picked[(race, "woman")], picked[(race, "man")]]
        n_need = sum(len(c) for c in cells)
        pool = surname_pool[race][:n_need]
        rng.shuffle(pool)
        it = iter(pool)
        for c in cells:
            for rec in c:
                ln = next(it)
                t = ln.title()
                rec["last"] = "Mc" + t[2:].capitalize() if t.startswith("Mc") else t
                rec["surname_census_pct_group"] = float(
                    surname_meta.loc[ln, "pctblack" if race == "Black" else "pctwhite"])

    # ---------- Extended cells ----------
    names = pd.read_csv(RAW / "crabtree" / "names.csv")
    ratings = pd.concat(pd.read_csv(RAW / "crabtree" / f"study-{i}-names.csv") for i in (1, 2, 3))
    attr = ratings.groupby("name").agg(perceived_income=("income.ord", "mean"),
                                       perceived_education=("education.ord", "mean"),
                                       n_ratings=("correct", "size"))
    cr = names.merge(attr, left_on="name", right_index=True).merge(
        ssa, left_on="first", right_index=True, how="left")
    cr["race"] = cr["identity"].map({"Hispanic": "Hispanic", "Asian or Pacific Islander": "Asian",
                                     "Black or African American": "Black", "White": "White"})
    cr["gender"] = [gender_of(b, s) for b, s in zip(cr.births, cr.female_share)]
    cr = cr.rename(columns={"mean.correct": "race_agreement"})
    ce = cr[(cr.race_agreement >= CRABTREE_CUTOFF) & cr.gender.notna()].copy()
    for c in ["perceived_income", "perceived_education"]:
        ce[c + "_z"] = (ce[c] - ce[c].mean()) / ce[c].std()
    tgt = ce[["perceived_income_z", "perceived_education_z"]].median()
    ce["match_distance"] = np.hypot(ce.perceived_income_z - tgt.perceived_income_z,
                                    ce.perceived_education_z - tgt.perceived_education_z)

    for race, gender in [("Hispanic", "man"), ("Asian", "woman"), ("Asian", "man")]:
        cand = ce[(ce.race == race) & (ce.gender == gender)].sort_values(["match_distance", "name"])
        rows, used_last = [], set()
        for rec in cand.to_dict("records"):
            if rec["first"] in used_first or rec["last"] in used_last:
                continue
            rows.append(rec); used_first.add(rec["first"]); used_last.add(rec["last"])
            if len(rows) == EXT_N + N_ALT:
                break
        picked[(race, gender)] = rows

    # Hispanic women: Tzioumis + SSA + Elder and Hayes perceived-Hispanic rating
    tz = pd.read_csv(RAW / "elder_hayes" / "firstnames.csv")
    tz["first"] = tz["firstname"].str.title()
    eh = pd.read_csv(RAW / "elder_hayes" / "comb_traitratings.tab", sep="\t")
    hw = tz[(tz.pcthispanic >= TZIOUMIS_MIN) & (tz.obs >= TZIOUMIS_OBS)].merge(
        ssa, left_on="first", right_index=True, how="left").merge(
        eh[["name", "Hispanic"]], left_on="first", right_on="name", how="left")
    hw["gender"] = [gender_of(b, s) for b, s in zip(hw.births, hw.female_share)]
    hw = hw[(hw.gender == "woman") & ~hw["first"].isin(used_first)]
    hw["rated"] = hw["Hispanic"].notna()
    hw = hw.sort_values(["rated", "Hispanic", "obs", "first"],
                        ascending=[False, False, False, True])
    hisp_last = names[names.identity == "Hispanic"]["last"].drop_duplicates().tolist()
    men_last = {r["last"] for r in picked[("Hispanic", "man")]}
    last_order = [l for l in hisp_last if l not in men_last] + [l for l in hisp_last if l in men_last]
    rows = []
    for rec, ln in zip(hw.head(EXT_N + N_ALT).to_dict("records"), last_order):
        rec["last"] = ln
        rows.append(rec); used_first.add(rec["first"])
    picked[("Hispanic", "woman")] = rows

    # ---------- Assemble ----------
    out_rows = []
    for (race, gender), recs in picked.items():
        tier = "core" if race in ("Black", "White") else "extended"
        need = CORE_N if tier == "core" else EXT_N
        if len(recs) < need:
            print(f"SHORTFALL {race} {gender}: {len(recs)} < {need}")
        for i, r in enumerate(recs):
            if (race, gender) in [("Hispanic", "woman")]:
                if r["rated"]:
                    source, rec_measure, rec_value = ("Tzioumis 2018 + Elder & Hayes 2023",
                                                      "eh_perceived_hispanic_1to5", r["Hispanic"])
                else:
                    source, rec_measure, rec_value = ("Tzioumis 2018 (no perception rating)",
                                                      "tzioumis_pct_hispanic", r["pcthispanic"] / 100)
            elif tier == "core":
                source, rec_measure, rec_value = ("Gaddis 2017",
                                                  "gaddis_congruent_matched_surname",
                                                  r["matched_last"])
            else:
                source, rec_measure, rec_value = ("Crabtree et al. 2023",
                                                  "crabtree_race_agreement", r["race_agreement"])
            out_rows.append({
                "name_id": f"{CODE[race]}{CODE[gender]}{i + 1:02d}",
                "role": "main" if i < need else "alternate",
                "tier": tier, "race": race, "gender": gender,
                "full_name": f"{r['first']} {r['last']}", "first": r["first"], "last": r["last"],
                "first_name_source": source,
                "recognition_measure": rec_measure,
                "recognition_value": round(float(rec_value), 4),
                "gaddis_mother_edu_quartile": "middle two" if tier == "core" else "",
                "crabtree_perceived_income": round(r["perceived_income"], 3) if "perceived_income" in r else "",
                "crabtree_perceived_education": round(r["perceived_education"], 3) if "perceived_education" in r else "",
                "crabtree_match_distance": round(r["match_distance"], 3) if "match_distance" in r else "",
                "tzioumis_pct_hispanic": r.get("pcthispanic", ""),
                "surname_census_pct_group": r.get("surname_census_pct_group", ""),
                "ssa_births_1950_2005": int(r["births"]),
                "ssa_female_share": round(float(r["female_share"]), 4),
            })
    out = pd.DataFrame(out_rows)
    out = out[~out.full_name.isin(FAMOUS)]
    out.to_csv(OUT / "names.csv", index=False)

    main_ = out[out.role == "main"]
    bal = main_.groupby(["tier", "race", "gender", "recognition_measure"]).agg(
        n=("full_name", "size"), recognition_mean=("recognition_value", "mean"),
        recognition_min=("recognition_value", "min"),
        ssa_female_share_mean=("ssa_female_share", "mean")).round(3)
    bal.to_csv(OUT / "cell_balance.csv")
    print(bal.to_string())

    # ---------- Profiles ----------
    prng = random.Random(SEED + 1)
    slots = ["w1_fwd", "w1_rev", "w2_fwd", "w2_rev"]

    def schedule():
        a, b = BIRTH_YEARS if prng.random() < 0.5 else BIRTH_YEARS[::-1]
        # each wording and each product order gets both birth years once
        return dict(zip(slots, [a, b, b, a]))

    profiles = []
    for r in out.itertuples():
        profiles.append({
            "profile_id": r.name_id, "role": r.role, "tier": r.tier,
            "race": r.race, "gender": r.gender, "name": r.full_name,
            "email": f"{r.first.lower()}.{r.last.lower()}@example.com".replace("'", ""),
            "zip": ZIP, "birth_year_by_run": schedule(),
        })
    for i in range(1, 5):
        profiles.append({
            "profile_id": f"BASE{i}", "role": "main", "tier": "baseline",
            "race": None, "gender": None, "name": None,
            "email": f"customer{i:02d}@example.com", "zip": ZIP,
            "birth_year_by_run": schedule(),
        })
    meta = {"seed": SEED, "zip": ZIP, "birth_years": BIRTH_YEARS,
            "run_slots": "w1/w2 = request wording, fwd/rev = product order",
            "n_main_profiles": sum(p["role"] == "main" for p in profiles),
            "n_alternate_profiles": sum(p["role"] == "alternate" for p in profiles),
            "profiles": profiles}
    (OUT / "profiles.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("main profiles:", meta["n_main_profiles"], "alternates:", meta["n_alternate_profiles"])


if __name__ == "__main__":
    main()
