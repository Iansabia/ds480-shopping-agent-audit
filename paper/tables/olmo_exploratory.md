*Table B7. OLMo 3 7B, separate exploratory block*

| Outcome | Gap (focal minus comparison), 95% CI | Names | Episodes | p | BH q | Flag (q < .10) |
|---|---|---|---|---|---|---|
| S0 price, names associated with Black vs White buyers (H1 type) | -0.1% (-1.7 to +1.4) | 40 | 3,164 | .847 | .931 | no |
| S0 price, names associated with women vs men (H2 type) | +0.1% (-1.4 to +1.7) | 40 | 3,164 | .887 | .931 | no |
| V ask rate, names associated with Black vs White buyers | -1.6 pts (-9.1 to +6.0) | 40 | 3,200 | .678 | .931 | no |
| V ask rate, names associated with women vs men | -0.3 pts (-8.0 to +7.3) | 40 | 3,200 | .931 | .931 | no |
| Twin tasks, S0: women's-line pick, names associated with women vs men | +1.8 pts (-3.2 to +6.8) | 40 | 629 | .469 | .931 | no |
| V hair and skin, bought without asking: identity-linked pick, Black vs White (H4 type) | no name variation | 40 | 588 |  |  |  |
| Twin tasks, V, bought without asking: women's-line pick, women vs men | no name variation | 40 | 356 |  |  |  |

Exploratory, added after the main results were seen (OLMo's run finished later). OLMo 3 7B: 7,040 of 7,040 episodes finished. Name level, as in the pre-registered tests: cell-adjusted name means, OLS with HC2 errors, 95% CI across names. Price gaps are exp(b) - 1 in percent; rates in percentage points. Black vs White rows hold gender fixed and the reverse. These tests form their own Benjamini-Hochberg family at 10%, separate from the frozen exploratory family and the add-on family. Training-data link (Figure A3): Across the 40 core names, a name's count in OLMo 3 pretraining data (shared base, via Ai2's 32B Instruct index) and its clear-request price gap had Spearman rho = -0.06 (p = .715; exploratory, traced, correlation only). Without the 5 names that are also common words, rho = -0.01 (p = .976); on the OLMo 2 index, rho = -0.03 (p = .839).
