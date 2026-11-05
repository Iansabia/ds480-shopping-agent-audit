# Add-on names (exploratory, PLAN.md D9)

Written Thu 11/5/2026, **after the main results were seen**. Ian approved add-ons A to D on 11/5.
Everything here is exploratory. Nothing touches `data/names.csv`, `data/profiles.json`, the 8
confirmatory tests or `results/confirmatory.*`. The rules below were written and applied the same
afternoon, before any add-on episode or add-on name check was run.

Built by `src/build_addon_names.py`. Outputs: `data/names_addon.csv`, `data/profiles_addon.json`,
`data/derived/ghekiere2025_uk_ie_congruence.csv`, `data/derived/addon_neutral_candidates.csv`,
`data/derived/addon_names_skipped.csv`. Account details follow the main set: email
`first.last@example.com`, ZIP 43215, birth years 1978 and 1998 per run slot (seeded, seed 20261105).

## Sources

| Source | Used for | Where |
|---|---|---|
| SSA national baby names, births 1950 to 2005 | gender share for every add-on first name | `data/raw/ssa/` (same file as the main set) |
| US Census Bureau 2010 surnames | race shares of the neutral surnames | `data/raw/census_surnames/` (same file) |
| Tzioumis, K. (2018). Demographic aspects of first names. *Scientific Data* 5:180025 | race shares of the neutral first names (descriptive, plus a Hispanic cutoff) | copy in the Elder and Hayes package (same file) |
| Ghekiere, A., Martiniello, B., Capistrano, D., et al. (2025). The Perception of Names in Experimental Studies on Ethnic Origin: A Cross-National Validation in Europe. *Scientific Data* 12:1883. doi:10.1038/s41597-025-06153-8. Data: OSF doi:10.17605/OSF.IO/YD5QV | Moroccan (North African) names and their per-name perception rates | `NameSurvey_DATARAW_2025.csv` (sha256 6b110461...6018) and `tb_dictionary_full.csv` (sha256 283dc56b...3301), downloaded from OSF 11/5, in `data/raw/ghekiere/` |
| Oreopoulos, P. (2009). Why Do Skilled Immigrants Struggle in the Labor Market? A Field Experiment with Six Thousand Resumes. NBER Working Paper 15036, Table 2. Published as Oreopoulos (2011), *American Economic Journal: Economic Policy* 3(4):148-71, doi:10.1257/pol.3.4.148 | Indian and Pakistani names used on audit resumes | NBER PDF (sha256 e723fa09...a7c), `data/raw/oreopoulos/`; Table 2 typed into `data/derived/oreopoulos2011_table2_names.csv`. The published AEJ version was not accessible (paywall), so the names are taken from the working paper's Table 2 and were not checked against the journal version. |

## A. Gender-neutral names (preset `neutral`)

Rules:
1. SSA births 1950 to 2005 at least 50,000 ("reasonably common").
2. Female share within 0.25 of 0.5, ranked by closeness to 0.5.
3. Dropped: Tzioumis share Hispanic 25% or more (Jaime, Angel, Rene, Guadalupe carry a Hispanic
   signal); first names already in the main set; a first name that is a word in any brand on a
   store page (Jackie: the hair brand "Aunt Jackie's").
4. Take the 10 closest. Only 10 names pass, so there are no alternates. Ian's examples Morgan
   (0.85 female), Quinn, Peyton and Skyler fail rule 1 or 2 in the 1950 to 2005 window.
5. Surnames: Census 2010, count at least 400,000, under 5% Hispanic and under 3% Asian or
   Pacific Islander, at least 25% White and 25% Black, not used in the main set, not a race or
   skin-color word (White, Black, Brown), not a candidate first name (Taylor), not a brand word.
   Ranked by the gap between % White and % Black (smallest first), the top 10 assigned in a seeded
   random order.
6. Well-known people (manual read, logged in the script): Jordan Davis and Avery Johnson were
   re-paired by swapping surnames with the next name.

| id | name | SSA births | SSA female share | first name % White / % Black (Tzioumis) | surname % White / % Black (Census) |
|---|---|---|---|---|---|
| GN01 | Avery Williams | 53,541 | 0.508 | 73.6 / 24.1 | 45.8 / 47.7 |
| GN02 | Kerry Johnson | 90,649 | 0.514 | 95.5 / 2.4 | 59.0 / 34.6 |
| GN03 | Kendall Green | 57,195 | 0.541 | 91.2 / 6.4 | 56.8 / 37.0 |
| GN04 | Jessie Lewis | 92,590 | 0.444 | 61.8 / 17.1 | 58.2 / 34.8 |
| GN05 | Riley Walker | 83,928 | 0.416 | 85.5 / 13.0 | 58.7 / 35.1 |
| GN06 | Casey Thomas | 170,248 | 0.413 | 95.3 / 1.6 | 52.6 / 38.8 |
| GN07 | Jody Jones | 83,273 | 0.646 | 97.4 / 0.7 | 55.2 / 38.5 |
| GN08 | Dominique Robinson | 66,382 | 0.710 | 73.0 / 16.1 | 48.7 / 44.9 |
| GN09 | Jordan Scott | 381,865 | 0.283 | 96.8 / 0.7 | 60.2 / 32.9 |
| GN10 | Taylor Harris | 345,987 | 0.728 | 95.4 / 1.2 | 51.4 / 42.4 |

Limits: the last three names lean one way (Dominique and Taylor 71 to 73% female, Jordan 28%), so
the analysis should report the female share per name beside its result. Tzioumis shares come from
mortgage applicants and lean White for most first names.

Model name check for A (rule fixed 11/5, before any neutral check call): the check here confirms
that a name does NOT read as one gender. `src/name_check.py run --set neutral --model
haiku|luna|flashlite`, then `score --set neutral`. Same three models, 5 guesses each, same
refusal handling. Prompt version nc3n is the main prompt with a third gender option, "neutral"
(given to both about equally); race options are the main ones. Keep rule: a name is kept if
neither "woman" nor "man" is the answer in half or more of its valid guesses (with 15 valid
guesses, at most 7 for each gender). A name that fails is dropped (no alternates) and listed in
`data/name_check_exclusions_addon.csv`, which the `neutral` preset reads. Also reported,
descriptive only: whether the name would meet the main set's 14 of 15 bar for one gender, and the
race guesses. Results: `data/name_check_results_neutral.csv`.

## C. Middle Eastern or North African names (preset `arab`)

No US audit-study list with five women's and five men's Arab names could be read in full:
Widner and Chicoine (2011, *Sociological Forum* 26(4):806-823) and Gaddis and Ghoshal (2015,
*ANNALS* 660:282-299) are paywalled and their name lists could not be checked, so they are not
used. The source is the validated list in Ghekiere et al. (2025): 16 Moroccan names, rated by
UK and Irish respondents (the two English-speaking samples).

Rules:
1. Candidates: the 16 Moroccan names tested in the UK and Ireland samples.
2. Gender: the main set's SSA rule (female share at least 0.95 or at most 0.05), with the birth
   floor lowered from 1,000 to 100 because these names are rare in US birth records. A name
   missing from SSA or under 100 births is dropped.
3. Rank within gender by Ghekiere's region congruence (share of UK and Irish raters whose
   region-of-origin answer matched the name's region), take 5 plus up to 3 alternates.
4. First names unique across the whole study (main and add-on sets); surnames unique within a cell;
   no word shared with a brand.
5. Then the model name check (below). Names that fail are replaced by alternates in order.

| id | role | name | region congruence (UK+IE) | gender congruence (UK+IE) | raters | SSA births | SSA female share |
|---|---|---|---|---|---|---|---|
| MEW01 | main | Naima El Amrani | 0.609 | 0.609 | 128 | 1,338 | 1.000 |
| MEW02 | main | Samira Saidi | 0.444 | 0.873 | 142 | 3,476 | 1.000 |
| MEW03 | main | Khadija Dahmani | 0.324 | 0.596 | 136 | 1,972 | 1.000 |
| MEW04 | main | Karima Idrissi | 0.316 | 0.757 | 136 | 1,169 | 1.000 |
| MEW05 | main | Fatima Benali | 0.305 | 0.883 | 154 | 17,223 | 0.998 |
| MEW06 | alternate | Nadia Salhi | 0.252 | 0.887 | 159 | 25,880 | 0.998 |
| MEW07 | alternate | Aicha Tahiri | 0.248 | 0.584 | 125 | 305 | 1.000 |
| MEM01 | main | Said El Moussaoui | 0.607 | 0.880 | 150 | 1,160 | 0.000 |
| MEM02 | main | Youssef Saidi | 0.534 | 0.931 | 131 | 1,006 | 0.000 |
| MEM03 | main | Omar Salhi | 0.531 | 0.908 | 130 | 66,180 | 0.006 |
| MEM04 | main | Mohamed Tahiri | 0.516 | 0.911 | 124 | 7,289 | 0.000 |
| MEM05 | main | Khalid Dahmani | 0.410 | 0.843 | 134 | 4,071 | 0.000 |
| MEM06 | alternate | Ahmed Benali | 0.367 | 0.873 | 150 | 7,813 | 0.000 |
| MEM07 | alternate | Mehdi Idrissi | 0.329 | 0.606 | 137 | 482 | 0.000 |

Dropped: Rachida El Moussaoui (not in SSA), Ali El Amrani (SSA female share 0.31).
Limits: raters are European, not American; region congruence is low in absolute terms because
raters chose among many regions (Ghekiere's region codes group Moroccan with Turkish names);
these are Moroccan (North African) names and stand in for "Arab or Middle Eastern" only in that sense.

## C. South Asian names (preset `sasian`)

Source: Oreopoulos (2009/2011) Table 2, 8 Indian and 8 Pakistani names used on audit resumes.
These are audit-study names, not perception-validated; the model name check is the validation.
Crabtree et al. (2023) has no South Asian first names (its only South Asian surname, Patel, is
paired with East Asian first names), so it cannot be used.

Rules: same as the MENA cell (SSA rule with a 100-birth floor, uniqueness, brand words), candidates
taken in Table 2 order (Indian names first, then Pakistani), 5 plus up to 3 alternates.

| id | role | name | Oreopoulos group | SSA births | SSA female share |
|---|---|---|---|---|---|
| SAW01 | main | Maya Kumar | Indian | 41,361 | 0.998 |
| SAW02 | main | Priyanka Kaur | Indian | 1,251 | 1.000 |
| SAW03 | main | Shreya Sharma | Indian | 2,104 | 1.000 |
| SAW04 | main | Tara Singh | Indian | 169,431 | 0.997 |
| SAW05 | main | Hina Chaudhry | Pakistani | 473 | 1.000 |
| SAW06 | alternate | Sana Khan | Pakistani | 2,313 | 0.998 |
| SAM01 | main | Arjun Kumar | Indian | 2,408 | 0.000 |
| SAM02 | main | Rahul Kaur | Indian | 2,678 | 0.000 |
| SAM03 | main | Samir Sharma | Indian | 4,200 | 0.004 |
| SAM04 | main | Asif Sheikh | Pakistani | 473 | 0.000 |
| SAM05 | main | Hassan Khan | Pakistani | 6,085 | 0.001 |

Dropped: Fatima Sheikh (first name already used in the MENA cell), Rabab Saeed (80 SSA births),
Panav Singh and Chaudhry Mohammad (not in SSA), Ali Saeed (SSA female share 0.31). The men's cell
has no alternate left. Limits: Maya and Tara are also common Anglo first names; "Rahul Kaur" pairs
a man's first name with a surname mostly used by Sikh women, as printed by Oreopoulos; the
Pakistani names may read as Middle Eastern. The name check decides.

## Model name check for C

`src/name_check.py run --set addon --model haiku|luna|flashlite`, then `score --set addon`.
Same three models, same 5 guesses each, same keep rule (14 of 15 guesses read as intended, race AND
gender). Only the race options change, because the main prompt has no Middle Eastern or South Asian
answer: "Black", "White", "Hispanic", "East Asian", "South Asian" or "Middle Eastern or North
African" (prompt version nc3a). Intended race: "Middle Eastern or North African" (MENA) and
"South Asian". A plain "Asian" answer is a miss. Failures go to `data/name_check_exclusions_addon.csv`,
which the `arab` and `sasian` presets read; a replaced name's alternate takes its hidden-need parity.
If a cell ends up with fewer than 5 names, it runs with what passed and the shortfall is reported.

## Native American names: not testable by name

There is no published perception-validated list of Native American names: Gaddis (2017), Crabtree
et al. (2023) and Elder and Hayes (2023) include no Native American names (their groups are Black,
White, Hispanic and Asian, or a subset). First
names carry no signal: in Tzioumis (2018), no first name has more than 9.4% American Indian or Alaska
Native holders (highest: Cheyenne 9.4%, 32 records). Some surnames are mostly AIAN in the 2010
Census (for example Begay 93.8%, Yazzie 94.6%, Locklear 72.9%), but all 605 surnames at 50% or more
AIAN together cover about 222,000 people, they point to specific nations (Navajo, Lumbee), and no
study has measured how readers perceive them. So a Native American cell cannot be built with the
same validation standard and is not run.
