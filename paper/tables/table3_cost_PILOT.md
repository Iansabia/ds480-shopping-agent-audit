**PILOT DATA, NOT RESULTS**

*Table 3. Scale and cost.*

| Run | Model | Episodes finished | API calls | Input tokens (M) | Output tokens (M) | Est. spend | $ per 1,000 episodes | Wall clock (h) |
|---|---|---|---|---|---|---|---|---|
| pilot_haiku | Claude Haiku 5.5 | 1,152 | 1,542 | 4.23 | 0.140 | $0.25 | $0.21 | 0.2 |
| vfollowup_haiku | Claude Haiku 5.5 | 144 | 312 | 0.83 | 0.036 | $0.10 | $0.70 | 0.0 |
| pilotsmall_flashlite | Gemini 3.5 Flash-Lite | 145 | 169 | 0.24 | 0.005 | $0.00 | $0.00 | 0.3 |
| main-run estimate (COST_ESTIMATE.md) | Claude Haiku 5.5 |  | 59,893 |  |  | $9.70 (batch, expected) |  |  |
| main-run estimate (COST_ESTIMATE.md) | GPT-6 Luna |  | 59,893 |  |  | $5.21 (batch, expected) |  |  |
| main-run estimate (COST_ESTIMATE.md) | Gemini 3.5 Flash-Lite |  | 7,702 |  |  | $2.04 (batch, expected) |  |  |

Spend is estimated from logged token counts (billed_usd_est in the turn logs) times published prices; provider consoles are the record. Estimate rows are from COST_ESTIMATE.md, made before the main run.

**PILOT DATA, NOT RESULTS**
