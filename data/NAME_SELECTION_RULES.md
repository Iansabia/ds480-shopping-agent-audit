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
