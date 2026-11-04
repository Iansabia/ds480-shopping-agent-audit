# Cost estimate for the main runs (Wed 11/4/2026)

No new paid calls were made. The basis is the token counts in `logs/*.turns.jsonl` (pilots and smoke tests). Prices are official batch list prices, checked 11/4. The numbers are in `results/cost_estimate.json`.

## How it was computed

- **Episodes:** `run_agents.py plan`, with no calls.
  - Haiku and Luna: `main` 32,640 + `planted` 800 + `validity` 640 + `m1` 7,040 = **41,120** each.
  - Gemini: `reduced` **7,040**.
- **Tokens per episode by arm:**
  - Haiku: the full 1,152-episode pilot.
  - Gemini: the 145-episode small pilot.
  - There were 0 errors, 0 retries and 0 refusals in every agent log.
  - Gemini logged 0 thinking tokens and Luna 0 reasoning tokens.
- **Scenarios:**
  - **Low:** the measured tokens.
  - **Expected:** low, plus the V second-ask fix. In the pilot, 29% of V episodes asked a second time. If those episodes get one more scripted turn, each adds about 3,050 input and 45 output tokens. This applies to Haiku and Luna. Gemini almost never asked twice.
  - **High:** expected tokens x 1.5, plus 10% retries (x 1.65 in all).
- **Luna (weaker basis):** Luna has only 4 logged smoke calls and 30 name-check calls, all with token counts.
  - On the same prompts, Luna used about the same input tokens as Gemini (0.97 to 1.0x). It used 0.53 to 0.73x Haiku's input tokens, because Haiku's tokenizer counts more. Luna's output was 0.64x Gemini's.
  - Per-call tokens were taken from Gemini's pilot.
  - Calls per episode were set two ways: Gemini's (about 1.0, for low) and Haiku's (1.14 to 1.54, plus the V fix, for expected). Luna's own ask rate is unknown.

| Per episode (expected) | Calls | Input | Output |
|---|---|---|---|
| Haiku | 1.46 | 4,068 | 130 |
| Luna | 1.46 | 2,297 | 47 |
| Gemini | 1.09 | 1,615 | 38 |

## Results (Batch prices)

| Model | Batch price in / out per 1M tokens | Low | Expected | High | At standard prices (expected) |
|---|---|---|---|---|---|
| Haiku 5.5 | $0.05 / $0.25 | $9.01 | **$9.70** | $16.00 | $19.40 |
| GPT-6 Luna | $0.05 / $0.25 | $3.54 | **$5.21** | $8.59 | $10.42 |
| Gemini 3.5 Flash-Lite | $0.15 / $1.25 | $2.04 | **$2.04** | $3.36 | $4.08 |

Luna extras: its pilot (1,152 episodes) would cost about $0.13, and finishing its name check (290 calls) under $0.03.

## Credit to add

| Provider | Add | Why |
|---|---|---|
| OpenAI | **$10** | Covers the high case ($8.59) plus extras, and matches the approved $5 to $10 and the $10 cap. $5 alone would unlock the paid tier, but it is below the expected cost. |
| Google | **$5** (minimum prepay) | Covers the high case ($3.36). Linking billing moves the project to Tier 1. The harness Google cap is $0 and has to be raised to $5 first. |
| Anthropic | **$0** if Max plan API credits of at least $15 show in the Console, **otherwise $15** | Expected total with today's $0.35 is about $10. **The high case ($16.35 total) passes the $15 cap.** If the 200-call projection runs high, the guard stops the run. Then use the money cut order: M1 down to one run saves about $0.9. |

## Rate limits and finishing by Friday 11/6

- **Anthropic (Start tier):** Batch allows 200,000 queued requests and 100,000 per batch. The pilot finished 1,152 episodes in about 10 minutes. 41,120 episodes in about 60,000 calls should finish within hours.
- **OpenAI:** paying $5 or more total moves the account to the Build tier: 5,000 requests per minute, 2M tokens per minute, and a Batch queue of 20M tokens for Luna.
  - The harness submits every pending turn at once, in batches of 5,000. Luna's first turns are about 63M tokens, so batches after the first few would be refused at the queue limit.
  - Rerunning the same command later collects the finished batches and submits the rest, so submit in waves.
  - Flex sync also works at 5,000 per minute. The 6.5-second pacing in `config.py` is for free access. Leaving it on would take about 4.5 days.
- **Google:** linking billing gives Tier 1, with Batch at 10M queued tokens. The reduced preset's first turns are about 10.2M tokens, just over that. The second batch may need a rerun after the first finishes.
  - The docs page does not list Tier 1 requests per minute or per day for Flash-Lite. The AI Studio console shows them.
  - Even at the current 13 per minute, about 7,700 calls take about 10 hours.
- **Spend guard:** it reserves the worst case (512 output tokens) for every queued turn. Luna's `main` reserves about $7.40 of its $10 cap. Run Luna's presets one at a time, so reservations do not stack past the cap.

## Sources

- Anthropic pricing: https://platform.claude.com/docs/en/about-claude/pricing
- Anthropic rate limits: https://platform.claude.com/docs/en/api/rate-limits
- OpenAI pricing: https://developers.openai.com/api/docs/pricing
- OpenAI Luna model page: https://developers.openai.com/api/docs/models/gpt-6-luna
- OpenAI rate limits and tiers: https://developers.openai.com/api/docs/guides/rate-limits
- Gemini pricing: https://aistudio.google.com/docs/pricing
- Gemini rate limits: https://aistudio.google.com/docs/rate-limits
- Gemini billing: https://aistudio.google.com/docs/billing
