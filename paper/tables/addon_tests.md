# Add-on test family (Benjamini-Hochberg, 10%)

Exploratory, added after the main results were seen. 26 tests in the family, separate from the frozen exploratory family. Name-level OLS on cell-adjusted name means, HC2 errors, t reference; z(log SSA name frequency) enters only when it correlates under 0.5 with the focal group (PLAN 5.3). Rows with no variation across names have no p and are left out (D5 rule).

| Part | Model | Test | Gap [95% CI] | p | q | Names (focal/other) |
|---|---|---|---|---|---|---|
| A | Claude Haiku 5.5 | S0 twin women's-line pick, gender-neutral vs men's names | +1.1 pts [-2.0, +4.3] | .466 | .638 | 5/20 |
| A | Claude Haiku 5.5 | S0 twin women's-line pick, gender-neutral vs women's names | -2.7 pts [-5.8, +0.4] | .084 | .299 | 5/20 |
| A | Claude Haiku 5.5 | V twin women's-line pick, gender-neutral vs men's names | +3.1 pts [-0.8, +7.0] | .111 | .321 | 5/20 |
| A | Claude Haiku 5.5 | V twin women's-line pick, gender-neutral vs women's names | -1.7 pts [-5.0, +1.5] | .273 | .473 | 5/20 |
| A | GPT-6 Luna | S0 twin women's-line pick, gender-neutral vs men's names | +3.9 pts [+2.2, +5.7] | <.001 | <.001 (discovery) | 5/20 |
| A | GPT-6 Luna | S0 twin women's-line pick, gender-neutral vs women's names | -7.6 pts [-10.3, -4.9] | <.001 | <.001 (discovery) | 5/20 |
| A | GPT-6 Luna | V twin women's-line pick, gender-neutral vs men's names | +22.3 pts [+17.1, +27.6] | <.001 | <.001 (discovery) | 5/20 |
| A | GPT-6 Luna | V twin women's-line pick, gender-neutral vs women's names | -16.7 pts [-19.7, -13.7] | <.001 | <.001 (discovery) | 5/20 |
| B | Claude Haiku 5.5 | STM wrong-line pick, women's vs men's names | -0.3 pts [-1.7, +1.0] | .634 | .749 | 20/20 |
| B | Claude Haiku 5.5 | STW wrong-line pick, women's vs men's names | -0.6 pts [-1.6, +0.3] | .195 | .390 | 20/20 |
| C | Claude Haiku 5.5 | MENA vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.3 pts [-0.6, +0.1] | .170 | .368 | 10/20 |
| C | Claude Haiku 5.5 | MENA vs White, S0 price (H1 type) | -0.21% [-1.83, +1.43] | .791 | .857 | 10/20 |
| C | Claude Haiku 5.5 | MENA vs White, V ask rate | +2.0 pts [-0.0, +4.0] | .054 | .236 | 10/20 |
| C | Claude Haiku 5.5 | MENA vs White, V identity-linked pick, bought without asking (H4 type) | +0.0 pts [-3.2, +3.2] | .993 | .993 | 10/20 |
| C | Claude Haiku 5.5 | South Asian vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.3 pts [-0.7, +0.1] | .159 | .368 | 8/20 |
| C | Claude Haiku 5.5 | South Asian vs White, S0 price (H1 type) | +0.60% [-1.50, +2.74] | .566 | .736 | 8/20 |
| C | Claude Haiku 5.5 | South Asian vs White, V ask rate | -1.1 pts [-3.4, +1.1] | .313 | .509 | 8/20 |
| C | Claude Haiku 5.5 | South Asian vs White, V identity-linked pick, bought without asking (H4 type) | -0.6 pts [-4.0, +2.8] | .708 | .800 | 8/20 |
| D | Claude Haiku 5.5 | Asian vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.0 pts [-0.5, +0.5] | .973 | .993 | 12/20 |
| D | Claude Haiku 5.5 | Asian vs White, V identity-linked pick, bought without asking (H4 type) | -0.8 pts [-3.6, +2.1] | .597 | .739 | 12/20 |
| D | Claude Haiku 5.5 | Hispanic vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.3 pts [-0.7, +0.1] | .092 | .299 | 12/20 |
| D | Claude Haiku 5.5 | Hispanic vs White, V identity-linked pick, bought without asking (H4 type) | +1.6 pts [-2.2, +5.4] | .403 | .617 | 12/20 |
| D | GPT-6 Luna | Asian vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.2 pts [-0.6, +0.1] | .167 | .368 | 12/20 |
| D | GPT-6 Luna | Asian vs White, V identity-linked pick, bought without asking (H4 type) | -1.8 pts [-4.8, +1.2] | .229 | .425 | 12/20 |
| D | GPT-6 Luna | Hispanic vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.1 pts [-0.4, +0.2] | .458 | .638 | 12/20 |
| D | GPT-6 Luna | Hispanic vs White, V identity-linked pick, bought without asking (H4 type) | +2.8 pts [+0.1, +5.6] | .044 | .230 | 12/20 |
