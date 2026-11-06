*Table A2. Full study design: arms, requests, accounts, tests and runs per model*

| Arm | Request | Page | Accounts | Tests | Status | Episodes per model (design) |
|---|---|---|---|---|---|---|
| S0 | Clear request | specified | core + extended + no name | H1, H2, H3 | confirmatory | 10,880 |
| S1 | Clear request plus a budget cap | specified | core + extended + no name | H3, cap violation | confirmatory | 10,880 |
| V | Vague request, need revealed only if asked | vague | core + extended + no name | H4, ask rate | confirmatory | 10,880 |
| PB | Clear request plus saved preference: lowest-priced product that meets the request | specified | 5 core names associated with Black buyers | planted bias check | check | 800 |
| PC / PQ | 'cheapest that fits' vs 'best quality' | specified | 16 core names | price validity | check | 640 |
| M1S0 / M1V | Clear or vague request plus a name-blind instruction | specified / vague | core names + no name | M1 fix | exploratory | 7,040 |
| Total main grid | 68 accounts x 40 tasks x 3 arms x 4 runs |  | 68 |  |  | 32,640 |
| Run: main_haiku | preset main, model Claude Haiku 5.5 |  |  | ask protocol: v_followup_1 | used here | 32,640 of 32,640 finished |
| Run: m1_haiku | preset m1, model Claude Haiku 5.5 |  |  | ask protocol: v_followup_1 | used here | 7,040 of 7,040 finished |
| Run: planted_haiku | preset planted, model Claude Haiku 5.5 |  |  | ask protocol: v_followup_1 | used here | 800 of 800 finished |
| Run: validity_haiku | preset validity, model Claude Haiku 5.5 |  |  | ask protocol: v_followup_1 | used here | 640 of 640 finished |
| Run: main_luna | preset main, model GPT-6 Luna |  |  | ask protocol: v_followup_1 | used here | 32,640 of 32,640 finished |
| Run: m1_luna | preset m1, model GPT-6 Luna |  |  | ask protocol: v_followup_1 | used here | 7,040 of 7,040 finished |
| Run: planted_luna | preset planted, model GPT-6 Luna |  |  | ask protocol: v_followup_1 | used here | 800 of 800 finished |
| Run: validity_luna | preset validity, model GPT-6 Luna |  |  | ask protocol: v_followup_1 | used here | 640 of 640 finished |
| Run: reduced_flashlite | preset reduced, model Gemini 3.5 Flash-Lite |  |  | ask protocol: v_followup_1 | used here | 7,040 of 7,040 finished |
| Run: reduced_olmo | preset reduced, model OLMo 3 7B |  |  | ask protocol: v_followup_1 | used here | 7,040 of 7,040 finished |

Design counts come from the catalog grids (no API calls). Run rows list the outcome files used for these figures.
