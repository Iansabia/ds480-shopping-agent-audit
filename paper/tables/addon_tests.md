# Add-on test family (Benjamini-Hochberg, 10%)

Exploratory, added after the main results were seen. 34 tests in the family, separate from the frozen exploratory family. Name-level OLS on cell-adjusted name means, HC2 errors, t reference; z(log SSA name frequency) enters only when it correlates under 0.5 with the focal group (PLAN 5.3). Rows with no variation across names have no p and are left out (D5 rule).

| Part | Model | Test | Gap [95% CI] | p | q | Names (focal/other) |
|---|---|---|---|---|---|---|
| A | Claude Haiku 5.5 | S0 twin women's-line pick, gender-neutral vs men's names | +1.1 pts [-2.0, +4.3] | .466 | .610 | 5/20 |
| A | Claude Haiku 5.5 | S0 twin women's-line pick, gender-neutral vs women's names | -2.7 pts [-5.8, +0.4] | .084 | .312 | 5/20 |
| A | Claude Haiku 5.5 | V twin women's-line pick, gender-neutral vs men's names | +3.1 pts [-0.8, +7.0] | .111 | .341 | 5/20 |
| A | Claude Haiku 5.5 | V twin women's-line pick, gender-neutral vs women's names | -1.7 pts [-5.0, +1.5] | .273 | .463 | 5/20 |
| A | GPT-6 Luna | S0 twin women's-line pick, gender-neutral vs men's names | +3.9 pts [+2.2, +5.7] | <.001 | <.001 (discovery) | 5/20 |
| A | GPT-6 Luna | S0 twin women's-line pick, gender-neutral vs women's names | -7.6 pts [-10.3, -4.9] | <.001 | <.001 (discovery) | 5/20 |
| A | GPT-6 Luna | V twin women's-line pick, gender-neutral vs men's names | +22.3 pts [+17.1, +27.6] | <.001 | <.001 (discovery) | 5/20 |
| A | GPT-6 Luna | V twin women's-line pick, gender-neutral vs women's names | -16.7 pts [-19.7, -13.7] | <.001 | <.001 (discovery) | 5/20 |
| B | Claude Haiku 5.5 | STM wrong-line pick, women's vs men's names | -0.3 pts [-1.7, +1.0] | .634 | .743 | 20/20 |
| B | Claude Haiku 5.5 | STW wrong-line pick, women's vs men's names | -0.6 pts [-1.6, +0.3] | .195 | .390 | 20/20 |
| B | GPT-6 Luna | STM wrong-line pick, women's vs men's names | no name variation | n/a | n/a | 20/20 |
| B | GPT-6 Luna | STW wrong-line pick, women's vs men's names | no name variation | n/a | n/a | 20/20 |
| C | Claude Haiku 5.5 | MENA vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.3 pts [-0.6, +0.1] | .170 | .385 | 10/20 |
| C | Claude Haiku 5.5 | MENA vs White, S0 price (H1 type) | -0.21% [-1.83, +1.43] | .791 | .868 | 10/20 |
| C | Claude Haiku 5.5 | MENA vs White, V ask rate | +2.0 pts [-0.0, +4.0] | .054 | .280 | 10/20 |
| C | Claude Haiku 5.5 | MENA vs White, V identity-linked pick, bought without asking (H4 type) | +0.0 pts [-3.2, +3.2] | .993 | .996 | 10/20 |
| C | Claude Haiku 5.5 | South Asian vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.3 pts [-0.7, +0.1] | .159 | .385 | 8/20 |
| C | Claude Haiku 5.5 | South Asian vs White, S0 price (H1 type) | +0.60% [-1.50, +2.74] | .566 | .713 | 8/20 |
| C | Claude Haiku 5.5 | South Asian vs White, V ask rate | -1.1 pts [-3.4, +1.1] | .313 | .507 | 8/20 |
| C | Claude Haiku 5.5 | South Asian vs White, V identity-linked pick, bought without asking (H4 type) | -0.6 pts [-4.0, +2.8] | .708 | .802 | 8/20 |
| C | GPT-6 Luna | MENA vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.1 pts [-0.4, +0.2] | .425 | .602 | 10/20 |
| C | GPT-6 Luna | MENA vs White, S0 price (H1 type) | -0.53% [-1.68, +0.63] | .354 | .547 | 10/20 |
| C | GPT-6 Luna | MENA vs White, V ask rate | +0.0 pts [-2.2, +2.2] | .996 | .996 | 10/20 |
| C | GPT-6 Luna | MENA vs White, V identity-linked pick, bought without asking (H4 type) | +4.5 pts [+0.9, +8.1] | .016 | .107 | 10/20 |
| C | GPT-6 Luna | South Asian vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.3 pts [-0.8, +0.2] | .193 | .390 | 8/20 |
| C | GPT-6 Luna | South Asian vs White, S0 price (H1 type) | -0.92% [-2.09, +0.26] | .120 | .341 | 8/20 |
| C | GPT-6 Luna | South Asian vs White, V ask rate | +1.1 pts [-0.8, +2.9] | .237 | .425 | 8/20 |
| C | GPT-6 Luna | South Asian vs White, V identity-linked pick, bought without asking (H4 type) | +3.5 pts [-0.3, +7.3] | .066 | .280 | 8/20 |
| D | Claude Haiku 5.5 | Asian vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.0 pts [-0.5, +0.5] | .973 | .996 | 12/20 |
| D | Claude Haiku 5.5 | Asian vs White, V identity-linked pick, bought without asking (H4 type) | -0.8 pts [-3.6, +2.1] | .597 | .724 | 12/20 |
| D | Claude Haiku 5.5 | Hispanic vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.3 pts [-0.7, +0.1] | .092 | .312 | 12/20 |
| D | Claude Haiku 5.5 | Hispanic vs White, V identity-linked pick, bought without asking (H4 type) | +1.6 pts [-2.2, +5.4] | .403 | .596 | 12/20 |
| D | GPT-6 Luna | Asian vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.2 pts [-0.6, +0.1] | .167 | .385 | 12/20 |
| D | GPT-6 Luna | Asian vs White, V identity-linked pick, bought without asking (H4 type) | -1.9 pts [-5.0, +1.2] | .216 | .408 | 12/20 |
| D | GPT-6 Luna | Hispanic vs White, S0 identity-linked pick, need stated (H3 type, S0 only) | -0.1 pts [-0.4, +0.2] | .458 | .610 | 12/20 |
| D | GPT-6 Luna | Hispanic vs White, V identity-linked pick, bought without asking (H4 type) | +2.6 pts [-0.1, +5.4] | .059 | .280 | 12/20 |
