*Table A1. Validity checks and data quality.*

| Check | Rule (PLAN) | Model | Value | Result |
|---|---|---|---|---|
| Name check | read as intended in 9 of 10 guesses (design 5.10) | all | 64 of 64 main names kept (PILOT_REPORT.md) | pass |
| Main-grid completion | at least 95% of 32,640 (PLAN 3) | Claude Haiku 5.5 | 32,640 finished | enters family |
| Planted bias (a): own shift | PB minus S0 negative, p < 0.05 (8.1a) | Claude Haiku 5.5 | -22.7%, p < .001 | pass |
| Planted bias (b): swapped H1 | 95% CI covers expected gap (8.1b) | Claude Haiku 5.5 | expected -6.2%, CI -11.5 to -0.8%; detection not required | pass |
| Shuffled-label null, H1 | share p < 0.05 at most 8.5% (8.2) | Claude Haiku 5.5 | 5.6% of 1,000 | pass |
| Shuffled-label null, H2 | share p < 0.05 at most 8.5% (8.2) | Claude Haiku 5.5 | 5.6% of 1,000 | pass |
| Shuffled-label null, H3 | share p < 0.05 at most 8.5% (8.2) | Claude Haiku 5.5 | 5.3% of 1,000 | pass |
| Shuffled-label null, H4 | share p < 0.05 at most 8.5% (8.2) | Claude Haiku 5.5 | 4.3% of 1,000 | pass |
| Arm P validity | best quality minus cheapest > 0, p < 0.05 (8.3) | Claude Haiku 5.5 | +325.5%, p < .001, 16 names | pass |
| Outcome types (S0, S1, V) | descriptive (8.4) | Claude Haiku 5.5 | bought 32,478, invalid_product 132, no_purchase 30 | read |
| Model IDs returned | descriptive (8.4) | Claude Haiku 5.5 | claude-haiku-5-5 (32,640) | read |
| Position effect | reversed minus forward, log price (5.2) | Claude Haiku 5.5 | -2.2%, p < .001; top slot 23% of picks | read |
| Main-grid completion | at least 95% of 32,640 (PLAN 3) | GPT-6 Luna | 32,640 finished | enters family |
| Planted bias (a): own shift | PB minus S0 negative, p < 0.05 (8.1a) | GPT-6 Luna | -34.6%, p < .001 | pass |
| Planted bias (b): swapped H1 | 95% CI covers expected gap (8.1b) | GPT-6 Luna | expected -10.1%, CI -18.9 to -3.8%; detection not required | pass |
| Shuffled-label null, H1 | share p < 0.05 at most 8.5% (8.2) | GPT-6 Luna | 4.3% of 1,000 | pass |
| Shuffled-label null, H2 | share p < 0.05 at most 8.5% (8.2) | GPT-6 Luna | 4.9% of 1,000 | pass |
| Shuffled-label null, H3 | share p < 0.05 at most 8.5% (8.2) | GPT-6 Luna | 1.8% of 1,000 | pass |
| Shuffled-label null, H4 | share p < 0.05 at most 8.5% (8.2) | GPT-6 Luna | 4.8% of 1,000 | pass |
| Arm P validity | best quality minus cheapest > 0, p < 0.05 (8.3) | GPT-6 Luna | +318.9%, p < .001, 16 names | pass |
| Outcome types (S0, S1, V) | descriptive (8.4) | GPT-6 Luna | bought 32,626, no_purchase 11, invalid_product 3 | read |
| Model IDs returned | descriptive (8.4) | GPT-6 Luna | gpt-6-luna (32,640) | read |
| Position effect | reversed minus forward, log price (5.2) | GPT-6 Luna | -9.3%, p < .001; top slot 21% of picks | read |
| Main-grid completion | at least 95% of 32,640 (PLAN 3) | Gemini 3.5 Flash-Lite | 7,040 of 7,040 reduced-grid runs finished | exploratory, not in the family |
| Planted bias | 8.1 | Gemini 3.5 Flash-Lite | no PB arm in its reduced grid | not run |
| Shuffled-label null, H1 | share p < 0.05 at most 8.5% (8.2) | Gemini 3.5 Flash-Lite | 5.0% of 1,000 | pass |
| Shuffled-label null, H2 | share p < 0.05 at most 8.5% (8.2) | Gemini 3.5 Flash-Lite | 4.3% of 1,000 | pass |
| Shuffled-label null, H3 | share p < 0.05 at most 8.5% (8.2) | Gemini 3.5 Flash-Lite | no name variation | not testable |
| Shuffled-label null, H4 | share p < 0.05 at most 8.5% (8.2) | Gemini 3.5 Flash-Lite | 6.3% of 1,000 | pass |
| Arm P validity | best quality minus cheapest > 0, p < 0.05 (8.3) | Gemini 3.5 Flash-Lite | no arm P in its reduced grid | not run |
| Outcome types (S0, S1, V) | descriptive (8.4) | Gemini 3.5 Flash-Lite | bought 6,690, no_purchase 348, invalid_product 2 | read |
| Model IDs returned | descriptive (8.4) | Gemini 3.5 Flash-Lite | gemini-3.5-flash-lite (7,040) | read |
| Position effect | reversed minus forward, log price (5.2) | Gemini 3.5 Flash-Lite | -4.6%, p < .001; top slot 32% of picks | read |
| Main-grid completion | at least 95% of 32,640 (PLAN 3) | OLMo 3 7B | 7,040 of 7,040 reduced-grid runs finished | exploratory, not in the family |
| Planted bias | 8.1 | OLMo 3 7B | no PB arm in its reduced grid | not run |
| Arm P validity | best quality minus cheapest > 0, p < 0.05 (8.3) | OLMo 3 7B | no arm P in its reduced grid | not run |
| Outcome types (S0, S1, V) | descriptive (8.4) | OLMo 3 7B | bought 6,878, no_purchase 148, invalid_product 14 | read |
| Model IDs returned | descriptive (8.4) | OLMo 3 7B |  | read |
| Same-group noise floor, H1 | SD of within-group half splits (5.2) | Claude Haiku 5.5 | 0.90 (x100 log price) vs gap -0.09 | read |
| Same-group noise floor, H2 | SD of within-group half splits (5.2) | Claude Haiku 5.5 | 0.88 (x100 log price) vs gap -0.27 | read |
| Same-group noise floor, H3 | SD of within-group half splits (5.2) | Claude Haiku 5.5 | 0.29 pts vs gap -0.12 | read |
| Same-group noise floor, H4 | SD of within-group half splits (5.2) | Claude Haiku 5.5 | 2.39 pts vs gap +2.75 | read |
| Same-group noise floor, H1 | SD of within-group half splits (5.2) | GPT-6 Luna | 0.70 (x100 log price) vs gap -1.81 | read |
| Same-group noise floor, H2 | SD of within-group half splits (5.2) | GPT-6 Luna | 0.73 (x100 log price) vs gap -1.61 | read |
| Same-group noise floor, H3 | SD of within-group half splits (5.2) | GPT-6 Luna | 0.11 pts vs gap -0.06 | read |
| Same-group noise floor, H4 | SD of within-group half splits (5.2) | GPT-6 Luna | 2.10 pts vs gap +8.36 | read |
