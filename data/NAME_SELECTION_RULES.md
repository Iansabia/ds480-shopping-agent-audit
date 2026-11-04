# Name selection rules (fixed before any name was picked)

Written 2026-11-04, committed before running `src/build_names.py`. At this point only
column codings and pooled-agreement totals by race had been looked at, no individual
names were ranked or chosen.

Design source: `DS480/notes/2026-11-03 - Paper 2 design (draft).md`, sections 5.3 and 5.10.

## Data

- Crabtree et al. 2023 validated names, Harvard Dataverse doi:10.7910/DVN/LP4EAR (CC0 1.0).
  `names.csv` gives `mean.correct`, the share of all ratings (studies 1 to 3 pooled) where the
  rater's race guess matched the intended race. Perceived income (1 low, 2 middle, 3 upper)
  and education (1 high school, 2 bachelor's, 3 master's, 4 PhD) are averaged per name from
  `study-1/2/3-names.csv`, all rows pooled, missing values dropped.
- SSA national baby names (yob1880 to yob2025), used only for gender.

## Rules

1. **Race agreement cutoff: `mean.correct >= 0.70`** for every cell (core and extended).
   Chance with four options is 0.25. Crabtree sets no cutoff. 0.70 was chosen because it is
   well above chance while leaving room for the later model name check (design 5.10) to drop
   names. If a cell has too few names at 0.70 after the other rules, the shortfall is reported
   and the design's Gaddis fallback is discussed with Ian. The cutoff is not lowered silently.
2. **Gender from SSA:** sum births for the first name over birth years 1950 to 2005 (people
   who would be adult shoppers now). Woman if female share >= 0.95, man if <= 0.05, and at
   least 1,000 births in that window (so the name is in the data). Anything else is excluded.
3. **One use per first name and per surname** across the whole set, so surnames vary and
   no first name appears twice.
4. **Matching on perceived class:** compute each eligible name's mean perceived income and
   education, z-scored over all eligible names in the four core cells. Target = the median
   of those core names on each z-score. Within each cell, rank eligible names by Euclidean
   distance to the target and take the closest (10 per core cell, 6 per extended cell),
   applying rule 3 greedily in order of distance across all cells (core cells first,
   interleaved by rank so no cell gets first pick of shared surnames). This is a simple
   stand-in for the Crabtree tool's "Control (Similar Attributes)" mode, not the tool itself.
5. **Alternates:** the next 3 names in each cell by the same ranking are kept as alternates,
   for names that fail the model name check.
6. **Well-known people:** after selection, a name that is the full name of a widely known
   public figure is swapped for the first alternate. This is a manual judgment and is logged.
7. Cells: core = Black and White x woman and man, 10 each; extended = Hispanic and Asian
   (Crabtree's "Asian or Pacific Islander") x woman and man, 6 each; baseline = 4 profiles
   with no name.

## Amendment 1 (2026-11-04, committed before the final selection run)

**Why.** The first run of the rules above (not kept) showed the Crabtree file cannot fill
the gender cells. Crabtree's Black, White and Hispanic names each use only 10 first
names, crossed with 10 surnames. Those first names are almost all one gender:
Black = 7 women's names (Lakisha, Tamika, Latonya, Latasha, Tanisha, Latoya, Ebony) and
3 men's (Jermaine, Darnell, Roosevelt); White = 9 men's names and 1 woman's (Mary);
Hispanic = 9 men's names and Guadalupe (mixed gender in SSA). Crabtree has no gender
field, so the design's plan (Crabtree plus SSA gender) gives at most 3 distinct Black men's
first names and 1 White women's first name. Only the per-cell counts were looked at
before this amendment, not a ranked pick.

**Core cells (Black and White x women and men) now use the design's named fallback,
Gaddis (2017), "How Black Are Lakisha and Jamal?", Sociological Science 4:469-489.**
1. Recognition: the share of Gaddis's respondents who read the first name as the intended
   race when shown with a racially matched last name (his Figures 1 and 2). Cutoff
   **>= 0.85**, the value already set for Gaddis names in the 11/3 research note
   (`stats_design.md`, rule 1). Gaddis publishes these rates only as bar charts, so they are
   digitized from the figure images (`src/digitize_gaddis.py`, checked against the numbers
   he states in the text, error about 0.5 points).
2. Class: Gaddis Table 1 marks each name's mother's-education quartile within race (bold =
   lowest, italic = highest). Keep only names in the **middle two quartiles** (regular
   type) so no cell leans on the strongest class signals. This is within race, so it does
   not equalize absolute class between Black and White names; that limit is reported.
   Gaddis's supplement Table A1 (exact share of mothers with some college) was not found.
3. Gender: same SSA rule as above (>= 0.95 female or <= 0.05 female, >= 1,000 births,
   birth years 1950 to 2005).
4. Rank within a cell by recognition (highest first); take 10, then 3 alternates.
5. Surnames from the 2010 Census surname file: Black surnames with pctblack >= 50 and count
   >= 10,000; White surnames with pctwhite >= 90 and count >= 30,000. Drop surnames that
   mainly signal a national origin or religion (a fixed list written in the script), then
   take the most common ones and assign them to names in a seeded random order, each
   surname used once.

**Extended cells.** Asian and Hispanic men stay on Crabtree full names (rules 1 to 4
above), except that surnames only need to be unique within a cell, because Crabtree has
just 10 Asian and 10 Hispanic surnames. Class target for these cells is the median of all
eligible Crabtree names. **Hispanic women** have no Crabtree names, so they use first names
with Tzioumis (2018) P(Hispanic | first name) >= 0.90 (stats_design.md rule 2), at least
100 mortgage records in that file, the SSA women rule, and an Elder and Hayes (2023)
perceived-Hispanic rating; ranked by that rating; paired with Crabtree's Hispanic surnames
not already used in the Hispanic men's cell where possible. Asian women stay on Crabtree.

The model name check (design 5.10) runs afterward on all picks and alternates.
