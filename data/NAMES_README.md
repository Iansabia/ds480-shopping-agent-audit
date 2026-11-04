# Names and account profiles

Built 2026-11-04 by `src/build_names.py` for design sections 5.3 and 5.10.
Rules were committed before picking: `data/NAME_SELECTION_RULES.md` (original rules,
then Amendments 1 and 2, each committed before the run that used it; see git log).

## Read this first: the design's name plan did not work as written

The design said: Crabtree et al. 2023 names, gender from SSA, Gaddis as fallback.
Crabtree's file turned out to use only 10 first names each for Black, White and Hispanic
names (crossed with 10 surnames), and those first names are nearly all one gender
(Black: 7 women's, 3 men's; White: 9 men's, 1 woman's; Hispanic: 9 men's plus Guadalupe).
So Crabtree cannot give 10 different Black men's or White women's first names.
**The four core cells therefore use the design's fallback, Gaddis (2017).** Crabtree is
still used for three extended cells. Hispanic women needed a third source. Ian should OK
this change (it alters the "Crabtree names" sentence in the paper's method section).

## Sources

| Source | What we used | Where | License |
|---|---|---|---|
| Gaddis, S. M. (2017). How Black Are Lakisha and Jamal? Racial Perceptions from Names Used in Correspondence Audit Studies. *Sociological Science* 4:469-489. doi:10.15195/v4.a19 | Per-name share of respondents reading the first name as the intended race, shown with a racially matched last name (Figures 1 and 2); mother's-education quartile within race (Table 1 bold/italic) | sociologicalscience.com PDF, downloaded 2026-11-04, sha256 ed91904f...8839 | Open access; exact license not checked (unverified) |
| Crabtree, C., Kim, J. Y., Gaddis, S. M., Holbein, J. B., Guage, C., and Marx, W. W. (2023). Validated names for experimental studies on race and ethnicity. *Scientific Data* 10:130. Data: Harvard Dataverse doi:10.7910/DVN/LP4EAR, version 1 | `names.csv` (race agreement per full name) and `study-1/2/3-names.csv` (44,170 ratings; perceived income and education) | Dataverse API, 2026-11-04, sha256 of names.csv ac8671a7...6676 | CC0 1.0 (from Dataverse metadata) |
| SSA national baby names, yob1880 to yob2025 | Female share of births per first name, birth years 1950 to 2005 | ssa.gov/oact/babynames/names.zip, 2026-11-04 (plain download blocked; fetched with a headless browser), sha256 cd78e975...3724 | US government data |
| US Census Bureau, 2010 surnames file | Surnames and their percent Black, White, Hispanic, Asian | www2.census.gov/topics/genealogy/2010surnames/names.zip, sha256 117c41cb...e135 | US government data |
| Tzioumis, K. (2018). Demographic aspects of first names. *Scientific Data* 5:180025 | P(Hispanic given first name), from mortgage records | Copy inside the Elder and Hayes replication package (`firstnames.csv`) | Package is CC0 1.0 |
| Elder, E. M., and Hayes, M. (2023). Signaling Race, Ethnicity, and Gender with Names: Challenges and Recommendations. *Journal of Politics* 85(2). Data: Harvard Dataverse doi:10.7910/DVN/0LCYN5 | Perceived-Hispanic rating (1 to 5) for Hispanic women's names; perceived class ratings for a balance check | Dataverse API, 2026-11-04 | CC0 1.0 |

Raw downloads are in `data/raw/` (git-ignored). Two small derived files are committed:
`data/derived/gaddis_rates_digitized.csv` and `data/derived/gaddis_table1_fonts.csv`.

**Gaddis rates are digitized, not copied.** Gaddis gives per-name rates only as bar-chart
images. `src/digitize_gaddis.py` measures each bar by its color against the chart's
gridlines. Checked against the numbers he prints in the text: Cheyanne 55.4 vs 55.6,
Maxwell 74.1 vs 74.3, all Black names 83.0 vs 82.5, all White names 92.2 vs 92.4 (matched
surname), mismatched-surname overall 66.6 vs 66.5 and 67.6 vs 67.9. Error is about half a
point. Name order was read by eye from the figure. Table 1 styles come from the PDF's font
names (`src/gaddis_table1_fonts.py`); Jalen and Nia read as italic and DaQuan and Lakisha
as bold, which matches what the text says about them.

## Cutoffs (fixed before picking)

- Gaddis core names: read as the intended race by **at least 85%** of respondents (with a
  matched surname). The 85% figure was already in the 11/3 research note.
- Crabtree names: **at least 70%** race agreement (chance is 25%). Set in the first rules
  commit, before any name was ranked.
- Hispanic women: Tzioumis P(Hispanic) **at least 0.90**.
- Gender (all cells): SSA female share **at least 0.95** (woman) or **at most 0.05** (man),
  with at least 1,000 births from 1950 to 2005.

## How names were picked

- **Core (10 per cell plus 3 alternates):** Gaddis first names that pass the cutoff and
  the gender rule, and sit in the **middle two quartiles of mother's education within
  race**, ranked by recognition. Surnames come from the 2010 Census list (Black: at least
  50% Black and 10,000 people; White: at least 90% White and 30,000 people). Surnames that
  mainly signal a national origin or religion (for example Pierre, Mohamed, Cohen) were
  dropped. The most common ones were used, each once, assigned in a seeded random order.
- **Asian women, Asian men, Hispanic men (6 plus 3 alternates):** Crabtree full names that
  pass 70% and the gender rule, ranked by closeness to the median perceived income and
  education of all eligible Crabtree names (a simple stand-in for the Crabtree tool's
  "similar attributes" mode). Surnames unique within each cell.
- **Hispanic women (6 plus 3 alternates):** first names with an Elder and Hayes rating
  first (by rating), then unrated names by Tzioumis record count. Paired with Crabtree's
  Hispanic surnames. Two main names (Guillermina, Rosalba) and all three alternates have
  **no perception rating**; they depend on the model name check.
- First names never repeat across the set.
- Alternates replace any name that fails the model name check (design 5.10: read as
  intended in 14 of 15 guesses), in order.
- Well-known people: none of the 68 full names matched a widely known figure on a manual
  read. This was a judgment call, not a search.

## Result (main names)

| Cell | Source | n | Recognition (mean, min) |
|---|---|---|---|
| Black women | Gaddis | 10 | 0.915, 0.890 |
| Black men | Gaddis | 10 | 0.931, 0.892 |
| White women | Gaddis | 10 | 0.948, 0.929 |
| White men | Gaddis | 10 | 0.945, 0.924 |
| Hispanic women | Tzioumis + Elder and Hayes | 6 | rated 4: 3.58 of 5; unrated 2: P(Hispanic) 0.92 |
| Hispanic men | Crabtree | 6 | 0.792, 0.737 |
| Asian women | Crabtree | 6 | 0.758, 0.706 |
| Asian men | Crabtree | 6 | 0.732, 0.710 |
| No-name baseline | none | 4 | |

68 main profiles plus 18 alternates. Full table: `data/names.csv`; per-cell summary:
`data/cell_balance.csv`. Recognition numbers from different sources are not on the same
scale and should not be compared across sources.

## Class matching: what it does and does not do

- Core cells are matched only in a relative sense: every core name is from the middle half
  of its own race's mother's-education range in Gaddis's New York birth data. Black and
  White mothers' education levels differ overall, so this does **not** make Black and White
  names equal in perceived class. Gaddis's exact per-name shares (online Table A1) were not
  found.
- Partial check with Elder and Hayes perceived-class ratings (1 to 5), which cover only a
  few of our first names (Black women 3, Black men 1, White women 3, White men 4): mean
  "upper class" rating 2.89 and 2.95 for the Black names vs 3.19 and 3.30 for the White
  names. Too few names to test, but it points the same way as Gaddis and Crabtree: names
  that read clearly Black also read lower in class. **This is a known confound.** The paper
  should say "names associated with Black women" and note that names also carry class.
- Extended Crabtree cells are matched on perceived income and education by the rule above.
  Mean perceived income (1 to 3) / education (1 to 4): Asian men 1.99 / 2.28, Asian women
  2.01 / 2.25, Hispanic men 1.85 / 1.91. Hispanic men read lower on both.

## Profiles (`data/profiles.json`)

Each profile has: `profile_id`, `role` (main or alternate), `tier` (core, extended,
baseline), `race`, `gender`, `name`, `email`, `zip`, `birth_year_by_run`.

- **Email:** `first.last@example.com`, lower case. Baseline: `customer01` to
  `customer04@example.com`, no name.
- **ZIP:** 43215 for everyone (downtown Columbus, Ohio). Builder's choice; it was picked
  as an ordinary US city ZIP, and whether it reads as demographically neutral to a model is
  **not verified**. It is one constant in the script if Ian wants another.
- **Birth year:** two values, 1978 and 1998 (about 48 and 28 in 2026). Builder's choice of
  values. Randomized within name: each name has 4 run slots (2 request wordings x 2 product
  orders), and each wording and each order gets both years once. Which year goes first is
  a seeded coin flip per profile (seed 20261105).

## Things to label as unverified in the paper

- Gaddis's per-name rates are our digitization (about +/- 0.5 points).
- Whether models read our names as intended is untested until the name check runs.
- Two Hispanic women's names have no human perception rating.
- Class is not equal between Black and White names (see above).
