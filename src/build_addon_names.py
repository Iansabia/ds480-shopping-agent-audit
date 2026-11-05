"""Build the exploratory add-on name sets (PLAN.md Deviations D9; Ian approved 11/5).

Added after the main results were seen. Nothing here touches data/names.csv,
data/profiles.json or any confirmatory test. Rules: data/ADDON_NAMES_README.md.

Sets:
  GN   gender-neutral first names (SSA female share near 50%) with racially mixed
       common Census surnames, for preset `neutral` (A)
  ME   Middle Eastern / North African (Moroccan) names from Ghekiere et al. 2025, for
       preset `arab` (C)
  SA   South Asian (Indian, then Pakistani) names from Oreopoulos 2009/2011 Table 2,
       for preset `sasian` (C)

Inputs (data/raw, git-ignored): ssa/ext/, census_surnames/ext/, elder_hayes/firstnames.csv
(Tzioumis 2018), ghekiere/NameSurvey_DATARAW_2025.csv.
Committed inputs: data/derived/oreopoulos2011_table2_names.csv (typed from the PDF table).
Outputs: data/names_addon.csv, data/profiles_addon.json,
data/derived/ghekiere2025_uk_ie_congruence.csv.
Run: .venv/bin/python -I src/build_addon_names.py
"""
import csv
import json
import random
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_names import RAW, ssa_gender  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data"
SEED = 20261105
ZIP = "43215"
BIRTH_YEARS = [1978, 1998]

# A: gender-neutral first names
NEUTRAL_MIN_BIRTHS = 50_000       # "reasonably common": births 1950-2005
NEUTRAL_MAX_DIST = 0.25           # |female share - 0.5| at most this
NEUTRAL_MAX_HISPANIC = 25.0       # Tzioumis % Hispanic below this (Jaime, Angel, Rene carry a Hispanic signal)
NEUTRAL_N, NEUTRAL_ALT = 10, 3
# Neutral surnames: Census 2010, common, racially mixed
SURNAME_MIN_COUNT = 400_000
SURNAME_MAX_HISP, SURNAME_MAX_API = 5.0, 3.0
SURNAME_MIN_WHITE, SURNAME_MIN_BLACK = 25.0, 25.0
SURNAME_EXCLUDE_WORDS = {"WHITE", "BLACK", "BROWN"}   # surnames that are race or skin-color words
# C: gender rule = the main SSA share rule, birth floor lowered from 1,000 to 100
FEM_MIN, MALE_MAX, C_MIN_BIRTHS = 0.95, 0.05, 100
C_N, C_ALT = 5, 3
# Ghekiere raters: English-speaking samples only (closest to a US reader)
GHEK_COUNTRIES = ("UK", "Ireland")

BRAND_WORDS: set = set()
# Rule: a full name that is a widely known public figure is skipped (manual read, logged).
FAMOUS = {"Jody Williams": "Nobel Peace Prize laureate (1997)",
          "Casey Jones": "folk-hero railroad engineer and song title",
          "Avery Johnson": "former NBA player and head coach",
          "Jordan Davis": "teenager killed in the 2012 Jacksonville shooting (widely covered); also a country singer"}


def brand_words():
    """Words in every brand on every page (PLAN D2 rule: no test name may share a
    word with a brand, e.g. "Aunt Jackie's" vs a first name Jackie)."""
    import re
    pages = json.loads((OUT / "pages.json").read_text())["pages"]
    products = json.loads((OUT / "products.json").read_text())["products"]
    pids = {it["product_id"] for p in pages for it in p["items"]}
    return {w.lower() for pid in pids for w in re.findall(r"[A-Za-z]+", products[pid].get("brand") or "")}


def existing_names():
    rows = list(csv.DictReader(open(OUT / "names.csv")))
    return {r["first"] for r in rows}, {r["last"] for r in rows}


def tzioumis():
    t = pd.read_csv(RAW / "elder_hayes" / "firstnames.csv", encoding="utf-8-sig")
    t["first"] = t["firstname"].str.title()
    return t.set_index("first")


def ssa_gender_c(ssa, first):
    if first not in ssa.index:
        return None, None, None
    r = ssa.loc[first]
    b, f = int(r["births"]), float(r["female_share"])
    if b < C_MIN_BIRTHS:
        return None, b, f
    return ("woman" if f >= FEM_MIN else "man" if f <= MALE_MAX else None), b, f


def neutral_set(ssa, used_first, used_last):
    tz = tzioumis()
    c = ssa[ssa["births"] >= NEUTRAL_MIN_BIRTHS].copy()
    c["dist"] = (c["female_share"] - 0.5).abs()
    c = c[c["dist"] <= NEUTRAL_MAX_DIST].join(tz[["obs", "pctwhite", "pctblack", "pcthispanic", "pctapi"]])
    c["excluded"] = ""
    c.loc[c["pcthispanic"] >= NEUTRAL_MAX_HISPANIC, "excluded"] = "Tzioumis % Hispanic >= 25"
    c.loc[c.index.isin(used_first), "excluded"] = "first name already in the main set"
    bw = brand_words()
    c.loc[c.index.str.lower().isin(bw), "excluded"] = "first name is a word in a brand on a page"
    c = c.sort_values("dist")
    elig = c[c["excluded"] == ""]
    firsts = list(elig.index[: NEUTRAL_N + NEUTRAL_ALT])

    s = pd.read_csv(RAW / "census_surnames" / "ext" / "Names_2010Census.csv")
    for k in ("pctwhite", "pctblack", "pctapi", "pcthispanic"):
        s[k] = pd.to_numeric(s[k], errors="coerce")
    s = s[(s["count"] >= SURNAME_MIN_COUNT) & (s["pcthispanic"] < SURNAME_MAX_HISP) & (s["pctapi"] < SURNAME_MAX_API)
          & (s["pctwhite"] >= SURNAME_MIN_WHITE) & (s["pctblack"] >= SURNAME_MIN_BLACK)].copy()
    s["Name"] = s["name"].str.title()
    s["gap"] = (s["pctwhite"] - s["pctblack"]).abs()
    s = s[~s["Name"].isin(used_last) & ~s["name"].isin(SURNAME_EXCLUDE_WORDS) & ~s["name"].str.lower().isin(bw)
          & ~s["Name"].isin(set(c.index))]          # no surname that is also a candidate first name (Taylor)
    s = s.sort_values("gap")
    lasts = list(s["Name"].iloc[: len(firsts)])
    rng = random.Random(SEED)
    rng.shuffle(lasts)
    pairs = list(zip(firsts, lasts))
    # FAMOUS rule: re-pair by swapping with the next name's surname (deterministic, logged)
    for i, (f, l) in enumerate(pairs):
        if f"{f} {l}" in FAMOUS:
            j = (i + 1) % len(pairs)
            pairs[i], pairs[j] = (f, pairs[j][1]), (pairs[j][0], l)
    sur = s.set_index("Name")
    rows = []
    for i, (f, l) in enumerate(pairs):
        r, sr = c.loc[f], sur.loc[l]
        rows.append({"name_id": f"GN{i + 1:02d}", "role": "main" if i < NEUTRAL_N else "alternate",
                     "set": "neutral", "tier": "addon", "race": "unmarked", "gender": "neutral",
                     "full_name": f"{f} {l}", "first": f, "last": l,
                     "first_name_source": "SSA 1950-2005 (female share near 50%)",
                     "recognition_measure": "ssa_female_share_distance_from_0.5", "recognition_value": round(r["dist"], 4),
                     "ssa_births_1950_2005": int(r["births"]), "ssa_female_share": round(r["female_share"], 4),
                     "tzioumis_pctwhite": r["pctwhite"], "tzioumis_pctblack": r["pctblack"],
                     "tzioumis_pcthispanic": r["pcthispanic"], "tzioumis_pctapi": r["pctapi"],
                     "surname_census_pctwhite": sr["pctwhite"], "surname_census_pctblack": sr["pctblack"],
                     "surname_census_count": int(sr["count"]), "name_check": "none"})
    return rows, c


def ghekiere_congruence():
    d = pd.read_csv(RAW / "ghekiere" / "NameSurvey_DATARAW_2025.csv", low_memory=False, encoding="latin-1")
    d = d[d["country_survey"].isin(GHEK_COUNTRIES) & d["country_name"].isin(["Morocco", "Pakistan"])].copy()
    d["Name"] = d["Name"].str.strip().str.replace(r"\s+", " ", regex=True)
    g = d.groupby(["country_name", "Name"]).agg(
        raters=("cong_sex", "size"), sex_congruence=("cong_sex", "mean"), region_congruence=("cong_region", "mean"),
        country_congruence=("cong_country", "mean"), religion_congruence=("cong_religion", "mean"),
        rater_countries=("country_survey", lambda x: ";".join(sorted(set(x))))).reset_index()
    for k in ("sex_congruence", "region_congruence", "country_congruence", "religion_congruence"):
        g[k] = g[k].round(4)
    g.to_csv(OUT / "derived" / "ghekiere2025_uk_ie_congruence.csv", index=False)
    return g


def c_cell(cands, ssa, used_first, prefix, race, gender, source, measure):
    """cands: list of dicts with first, last, full_name, value (rank key) in rank order."""
    rows, skipped, seen_last = [], [], set()
    for cnd in cands:
        g, b, f = ssa_gender_c(ssa, cnd["first"])
        why = None
        if g is None:
            why = ("not in SSA 1950-2005" if b is None else f"SSA births {b} < {C_MIN_BIRTHS}" if b < C_MIN_BIRTHS
                   else f"SSA female share {f:.3f} fails the 0.95/0.05 rule")
        elif g != gender:
            why = f"SSA gender is {g}"
        elif cnd["first"] in used_first:
            why = "first name already used"
        elif cnd["last"] in seen_last:
            why = "surname already used in this cell"
        elif {w.lower() for w in cnd["full_name"].split()} & BRAND_WORDS:
            why = "shares a word with a brand on a page"
        if why:
            skipped.append({**cnd, "why": why})
            continue
        if len(rows) >= C_N + C_ALT:
            break
        used_first.add(cnd["first"])
        seen_last.add(cnd["last"])
        i = len(rows)
        rows.append({"name_id": f"{prefix}{i + 1:02d}", "role": "main" if i < C_N else "alternate",
                     "set": "arab" if race == "MENA" else "sasian", "tier": "addon", "race": race, "gender": gender,
                     "full_name": cnd["full_name"], "first": cnd["first"], "last": cnd["last"],
                     "first_name_source": source, "recognition_measure": measure,
                     "recognition_value": cnd.get("value", ""), "ssa_births_1950_2005": b,
                     "ssa_female_share": round(f, 4), "name_check": "rg_addon"})
    return rows, skipped


def main():
    global BRAND_WORDS
    BRAND_WORDS = brand_words()
    ssa = ssa_gender()
    used_first, used_last = existing_names()
    neutral, neutral_cands = neutral_set(ssa, used_first, used_last)
    used_first |= {r["first"] for r in neutral}

    g = ghekiere_congruence()
    mor = g[g["country_name"] == "Morocco"].copy()
    sex_of = {}
    dic = pd.read_csv(RAW / "ghekiere" / "tb_dictionary_full.csv", encoding="utf-8-sig")
    dic["name"] = dic["name"].str.strip().str.replace(r"\s+", " ", regex=True)
    for r in dic.itertuples():
        sex_of[r.name] = "man" if int(r.sex) == 1 else "woman"
    out, skipped = [], []
    for gender, prefix in (("woman", "MEW"), ("man", "MEM")):
        sub = mor[mor["Name"].map(sex_of) == gender].sort_values("region_congruence", ascending=False)
        cands = []
        for r in sub.itertuples():
            first, last = r.Name.split(" ", 1)
            cands.append({"full_name": r.Name, "first": first, "last": last, "value": r.region_congruence,
                          "ghekiere_sex_congruence": r.sex_congruence, "ghekiere_raters": r.raters})
        rows, sk = c_cell(cands, ssa, used_first, prefix, "MENA", gender,
                          "Ghekiere et al. 2025 (Moroccan names, UK and Ireland raters)",
                          "ghekiere_region_congruence_uk_ie")
        meta = {c["full_name"]: c for c in cands}
        for row in rows:
            row["ghekiere_sex_congruence"] = meta[row["full_name"]]["ghekiere_sex_congruence"]
            row["ghekiere_raters"] = meta[row["full_name"]]["ghekiere_raters"]
        out += rows
        skipped += [{**s, "cell": f"MENA {gender}"} for s in sk]

    oreo = pd.read_csv(OUT / "derived" / "oreopoulos2011_table2_names.csv")
    oreo = oreo[oreo["group"].isin(["Indian", "Pakistani"])].sort_values("table_order")
    for gender, prefix in (("woman", "SAW"), ("man", "SAM")):
        sub = oreo[oreo["sex"] == gender]
        cands = [{"full_name": r.full_name, "first": r.first, "last": r.last, "value": r.group,
                  "table_order": int(r.table_order)} for r in sub.itertuples()]
        rows, sk = c_cell(cands, ssa, used_first, prefix, "South Asian", gender,
                          "Oreopoulos 2009 NBER WP 15036 Table 2 (audit-study names; Indian, then Pakistani)",
                          "oreopoulos_group")
        out += rows
        skipped += [{**s, "cell": f"South Asian {gender}"} for s in sk]

    allrows = neutral + out
    df = pd.DataFrame(allrows)
    df.to_csv(OUT / "names_addon.csv", index=False)
    pd.DataFrame(skipped).to_csv(OUT / "derived" / "addon_names_skipped.csv", index=False)
    neutral_cands.round(4).to_csv(OUT / "derived" / "addon_neutral_candidates.csv")

    prng = random.Random(SEED + 1)
    slots = ["w1_fwd", "w1_rev", "w2_fwd", "w2_rev"]

    def schedule():
        a, b = BIRTH_YEARS if prng.random() < 0.5 else BIRTH_YEARS[::-1]
        return dict(zip(slots, [a, b, b, a]))

    profiles = []
    for r in allrows:
        email = (r["first"] + "." + r["last"]).lower().replace(" ", "").replace("'", "") + "@example.com"
        profiles.append({"profile_id": r["name_id"], "role": r["role"], "tier": "addon", "set": r["set"],
                         "race": r["race"], "gender": r["gender"], "name": r["full_name"], "email": email,
                         "zip": ZIP, "birth_year_by_run": schedule()})
    meta = {"seed": SEED, "zip": ZIP, "birth_years": BIRTH_YEARS,
            "note": "Exploratory add-on profiles (PLAN.md D9), added after the main results were seen. "
                    "Not part of any confirmatory test.",
            "profiles": profiles}
    (OUT / "profiles_addon.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(df[["name_id", "role", "set", "gender", "full_name", "recognition_value", "ssa_births_1950_2005",
              "ssa_female_share"]].to_string())
    print("\nskipped:")
    print(pd.DataFrame(skipped)[["cell", "full_name", "why"]].to_string() if skipped else "none")


if __name__ == "__main__":
    main()
