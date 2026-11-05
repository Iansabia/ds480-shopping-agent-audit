**PILOT DATA, NOT RESULTS**

*Table A1. Validity checks and data quality.*

| Check | Rule (PLAN) | Model | Value | Result |
|---|---|---|---|---|
| Name check | read as intended in 9 of 10 guesses (design 5.10) | all | 64 of 64 main names kept (PILOT_REPORT.md) | pass |
| Main-grid completion | at least 95% of 32,640 (PLAN 3) | Claude Haiku 5.5 | 1,152 finished | below 95% (pilot or partial) |
| Planted bias | 8.1 | Claude Haiku 5.5 | PB arm not run | not run |
| Shuffled-label null, H1 | share p < 0.05 at most 8.5% (8.2) | Claude Haiku 5.5 | 5.8% of 1,000 | pass |
| Shuffled-label null, H2 | share p < 0.05 at most 8.5% (8.2) | Claude Haiku 5.5 | 6.9% of 1,000 | pass |
| Shuffled-label null, H3 | share p < 0.05 at most 8.5% (8.2) | Claude Haiku 5.5 | 5.9% of 1,000 | pass |
| Shuffled-label null, H4 | share p < 0.05 at most 8.5% (8.2) | Claude Haiku 5.5 | 4.6% of 1,000 | pass |
| Arm P validity | best quality minus cheapest > 0, p < 0.05 (8.3) | Claude Haiku 5.5 | arm P not run | not run |
| Outcome types (S0, S1, V) | descriptive (8.4) | Claude Haiku 5.5 | bought 1,111, no_purchase 36, invalid_product 5 | read |
| Model IDs returned | descriptive (8.4) | Claude Haiku 5.5 | claude-haiku-5-5 (1,152) | read |
| Position effect | reversed minus forward, log price (5.2) | Claude Haiku 5.5 | -4.0%, p < 0.001; top slot 22% of picks | read |
| Main-grid completion | at least 95% of 32,640 (PLAN 3) | Gemini 3.5 Flash-Lite | 135 finished | below 95% (pilot or partial) |
| Planted bias (a): own shift | PB minus S0 negative, p < 0.05 (8.1a) | Gemini 3.5 Flash-Lite | -5.8%, p 0.374 | fail |
| Planted bias (b): swapped H1 | 95% CI covers expected gap (8.1b) | Gemini 3.5 Flash-Lite | expected -2.3%, CI -7.2 to +2.7%; detection not required | pass |
| Shuffled-label null, H1 | share p < 0.05 at most 8.5% (8.2) | Gemini 3.5 Flash-Lite | 25.8% of 1,000 | fail: permutation p used |
| Shuffled-label null, H2 | share p < 0.05 at most 8.5% (8.2) | Gemini 3.5 Flash-Lite | 9.3% of 1,000 | fail: permutation p used |
| Shuffled-label null, H3 | share p < 0.05 at most 8.5% (8.2) | Gemini 3.5 Flash-Lite | 25.4% of 1,000 | fail: permutation p used |
| Shuffled-label null, H4 | share p < 0.05 at most 8.5% (8.2) | Gemini 3.5 Flash-Lite | 27.5% of 1,000 | fail: permutation p used |
| Arm P validity | best quality minus cheapest > 0, p < 0.05 (8.3) | Gemini 3.5 Flash-Lite | arm P not run | not run |
| Outcome types (S0, S1, V) | descriptive (8.4) | Gemini 3.5 Flash-Lite | bought 134, no_purchase 1 | read |
| Model IDs returned | descriptive (8.4) | Gemini 3.5 Flash-Lite | gemini-3.5-flash-lite (150) | read |
| Position effect | reversed minus forward, log price (5.2) | Gemini 3.5 Flash-Lite | +0.2%, p 0.929; top slot 60% of picks | read |
| Same-group noise floor, H1 | SD of within-group half splits (5.2) | Claude Haiku 5.5 | 1.82 (x100 log price) vs gap -1.67 | read |
| Same-group noise floor, H2 | SD of within-group half splits (5.2) | Claude Haiku 5.5 | 1.83 (x100 log price) vs gap -0.76 | read |
| Same-group noise floor, H3 | SD of within-group half splits (5.2) | Claude Haiku 5.5 | 1.58 pts vs gap +1.25 | read |
| Same-group noise floor, H4 | SD of within-group half splits (5.2) | Claude Haiku 5.5 | 8.21 pts vs gap +5.06 | read |

**PILOT DATA, NOT RESULTS**
