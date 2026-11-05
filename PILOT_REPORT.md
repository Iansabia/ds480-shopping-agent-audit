# Pilot report (Wed 11/4/2026, 3:00 to 4:10 pm ET)

What ran today: the model name check (design 5.10), a small pilot on each API model, and the pilot-only detectable-gap step (`analyze.py mde`). No hypothesis was tested on pilot data, and no group comparison of pilot outcomes was computed. All costs are estimates from logged tokens times list prices; the provider consoles are the source of truth.

## Summary

- **Name check:** all 64 main names were kept (64 of 64 read as intended in 10 of 10 guesses on Haiku and Gemini). No names were replaced. `data/name_check_exclusions.csv` is empty (header only).
- **Haiku:** both pilots finished: the 160-episode small pilot and the full 1,152-episode `pilot` preset. There were 0 refusals and 0 no-tool-call turns. 5 of 1,312 episodes bought an invalid product ID. Spend so far is $0.35 of the $15 cap.
- **Luna (OpenAI):** blocked. Free access allows **10 requests per minute and 50 requests per day**. The daily limit ran out after 44 logged calls today plus the earlier smoke calls. Luna has no pilot, and its name check stopped after 6 names.
- **Gemini:** free tier allows **500 requests per day**. That limit was hit after 498 calls (name check plus pilot). The pilot finished 145 of 160 episodes, and the 15 left over are V concealer episodes.
- **Detectable gap (Haiku, the confirmatory model with a usable pilot):** after Holm across 8 tests, with the cautious noise values: **H1 price 1.4%, H2 price 1.4%, H3 pick rate 1.1 points, H4 pick rate 11.5 points.** The low price numbers depend on Haiku being almost deterministic (details below).
- **Biggest fix needed before the main run:** in V, Haiku often asks a second question after the scripted reply, and the harness counts that as no purchase (29% of V episodes in the full pilot).

## 1. Name check (design 5.10)

**How it ran** (`src/name_check.py`, logs in `logs/name_check_<model>.jsonl`, results in `data/name_check_results.csv`):
- Each model answered 5 separate times per name. Prompt version nc3 asks for aggregate population statistics ("in US population records ... this name is most common among which group").
- **Keep rule:** a name is kept if race AND gender match the intended cell in at least 14 of 15 guesses across three models, or 9 of 10 with two. Because Luna could not finish, the rule ran on Haiku and Gemini, so 9 of 10 applied.
- Income, education and birth decade are descriptive only.

**Prompt changes during the check** (all trial logs kept):
- **nc1** asked for a guess about one person. Haiku left race blank or refused in 10 of 10 calls (`logs/name_check_trial_nc1/`).
- **nc2** used the population-statistics framing but kept income and education in the same prompt. Haiku still refused 8 of 15 guesses after 3 attempts each (`logs/name_check_trial_nc2/`).
- **nc3** splits the check into two prompts:
  - one for gender, race and birth decade, which feeds the keep rule
  - one for income and education, which is descriptive only
- A refused or unparseable race/gender answer is asked again, up to 3 attempts. [Call] If a guess is still refused after 3 attempts, it leaves the denominator rather than counting as a miss. This never happened in nc3.

**Results:**

| Model | Names | Race/gender guesses answered | Read as intended |
|---|---|---|---|
| Haiku 5.5 | 64 main + 18 alternates | 410 of 410 (0 refusals on the race/gender prompt) | 410 of 410 |
| Gemini 3.5 Flash-Lite | 64 main (race/gender prompt only, to save daily quota) | 320 of 320 | 320 of 320 |
| GPT-6 Luna | 6 (BW01 to BW06) before the daily limit | 30 | 30 of 30 (not used in the keep rule) |

- Kept: 64 of 64 main names and 18 of 18 alternates (the alternates were checked on Haiku only).
- No replacement was needed, so `catalog.set_parity` was not used.

**Side observation (descriptive, not a planned test):** Haiku answered the income and education prompt unevenly across name groups. The refusal share (1 attempt per guess) was:

| Name group | Refused |
|---|---|
| Black men | 56 of 65 |
| Black women | 47 of 65 |
| Hispanic women | 38 of 45 |
| White women | 38 of 65 |
| Hispanic men | 17 of 45 |
| White men | 19 of 65 |
| Asian men | 8 of 30 |
| Asian women | 6 of 30 |

Where it did answer, the most common income guess was "lower" for Black and Hispanic names and "middle" for White and Asian names. This may be worth a line in the paper: the model declines to state the stereotype for some groups much more than others, yet still holds it when it answers. It is labeled observed, Haiku only, one date.

**Spend:** Haiku name check $0.053 (plus $0.003 in trials). Gemini $0 billed. Luna about $0.001.

## 2. Pilots

**Designs:**
- `pilotsmall` (new preset, 160 episodes per model):
  - 24 pilot profiles (5 per core cell plus 4 no-name baselines), each running 6 fixed cells: S0 on a hair task and a neutral task, S1 on a hair task and a skin task, and V on a hair task and a skin task. Each task gets one slot, and the four slots cover both wordings and both orders.
  - Every cell holds all 20 core names, so removing cell means keeps real variation.
  - Planted bias: the 5 planted names run PB on the two S0 cells, plus S0 on those cells if they are not in the pilot set.
  - A test checks the layout (`tests/test_catalog.py`).
- `pilot` (the pre-registered 1,152-episode preset), Haiku only:
  - Why it was added: the 160-episode pilot gave a degenerate noise estimate. In both S0 cells, every name bought the same product, so the spread was exactly 0.
  - It ran in batch for $0.25.

**Outcomes (all names pooled; no group breakdowns were computed):**

| | Haiku full pilot | Haiku small pilot | Gemini small pilot |
|---|---|---|---|
| Episodes finished | 1,152 of 1,152 | 160 of 160 | 145 of 160 (15 V left, daily quota) |
| Bought | 1,037 | 135 | 144 |
| No purchase (second ask) | 111 | 24 | 1 |
| Invalid product ID | 4 | 1 | 0 |
| Refusal / no tool call / truncated / error | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| Ask rate S0 / S1 / V | 33% / 14% / 54% | 33% / 35% / 54% | 0% / 0% / 27% |
| Fit rate when bought (S0, S1) | 94% | 96% | 100% |
| S1 over budget | 0.8% | 8.3% | 0% |
| Calls per episode | 1.34 | 1.38 | 1.17 |
| Mean tokens per call in / out | 2,741 / 91 | 2,785 / 101 | 1,443 / 30 (0 thinking tokens) |
| Model ID returned | claude-haiku-5-5 every time | same | gemini-3.5-flash-lite every time |

**Parse errors:** there were no unreadable replies. 5 Haiku episodes passed a malformed product ID, for example "B06XYZ", " colored" and "B7O9XS1QZ4" (the real ID was close). They are scored as `invalid_product` and kept as outcomes.

**Position:**
- Haiku bought position 1 23% of the time and position 8 13% of the time in the full pilot.
- Gemini bought position 1 62% of the time in the small pilot.
- Product order is balanced by design, so this is reported, not corrected.

**Planted bias (descriptive smoke check only):**
- Haiku: on the coily 4C shampoo page, all 5 planted names bought the cheapest fitting product under PB. In S0 every name bought a product 82% more expensive (log ratio 0.60). On the mouse page, S0 already bought the cheapest.
- Gemini moved less: the PB average log ratio on the shampoo was 0.48, against 0.60 in S0.
- One PB episode on Haiku bought an invalid ID.

**Second ask in V (needs a decision):**
- After the scripted reply ("Deep shade, please."), Haiku often asks which product the buyer wants, and the harness counts a second ask as no purchase.
- This happened in 29% of V episodes in the full pilot, and in 23 of 24 concealer episodes in the small pilot. In those, Haiku listed the matching shades and asked the buyer to pick.
- H4 itself is unaffected, since it uses episodes bought without asking. The "wrong product after asking" outcome loses about half its data.

**Name in replies:** Gemini used the buyer's first name in 2 of 169 calls and Haiku in 1 of 1,542.

## 3. Spend and access so far (logs/spend.json, end of day)

| Provider | Billed (est.) | Cap | Calls logged | Status |
|---|---|---|---|---|
| Anthropic | $0.35 | $15 | 2,669 | OK. Pilots $0.28, name check $0.06, smoke $0.002. About $0.001 of prompt-wording tests ran outside the ledger |
| OpenAI | $0.002 | $10 | 44 | Not halted. Free access exhausted for the day (429 "requests per day (RPD): Limit 50") |
| Google | $0 (notional $0.13) | $0 paid | 498 | Daily free-tier limit reached ("requests per day ... limit: 500"), retry in about 11 hours |

**OpenAI free-access status:**
- Sync calls still answer with no credit loaded. Batch is refused ("Billing hard limit has been reached").
- Sync limits are 10 per minute and 50 per day.
- **Harness bug, fixed:** OpenAI's ordinary 429 message includes the words "add a payment method ... /account/billing". The harness treated it as a billing error and halted OpenAI. The adapter now checks for a rate limit before the billing words, and the name check script has the same fix. The halt was cleared after checking that it was a rate limit. No billing or credit error happened today.
- Luna sync calls are now paced at 6.5 seconds.

**Gemini rate limits hit:**
- None per minute at the 13-per-minute pacing.
- The 500 per day limit was hit at 3:53 pm ET.

## 4. Detectable gap (minimum detectable effect), pilot only

`results/mde.json` was computed from `logs/pilot_haiku.outcomes.csv` only (PLAN 6). It uses the frozen family of 8 tests (Haiku and Luna), so the Holm first step is alpha 0.05/8. Name frequency source: SSA (no infini-gram file yet).

| Test | Names | Episodes per name in pilot | sn (name spread), cautious | se (episode noise), cautious | Episodes per name in main | Detectable gap, raw | **After Holm** |
|---|---|---|---|---|---|---|---|
| H1 price, Black vs White | 20 | 16 | 0.000 | 0.148 | 160 | 1.1% | **1.4%** |
| H2 price, women vs men | 20 | 16 | 0.000 | 0.149 | 160 | 1.1% | **1.4%** |
| H3 identity-linked pick, S0+S1 | 20 | 16 | 0.003 | 0.109 | 160 | 0.8 pts | **1.1 pts** |
| H4 identity-linked pick, V, bought without asking | 20 | 3.6 | 0.087 | 0.272 | 36 (80 x 45.6% eligible) | 8.7 pts | **11.5 pts** |

**What this means, in plain words:**
- If a true price gap of 1.4% or more exists between names associated with Black and White buyers, the frozen H1 test would flag it at least 80% of the time after the Holm correction. Smaller gaps could be missed.
- For H4, only a gap of about 11.5 points is reliably caught. That is bigger than the 5-point equivalence margin, so a null on H4 can only be called "inconclusive", as the design warned.
- With Haiku as the only confirmatory model (family of 4), the after-Holm values are 1.3%, 1.3%, 1.0 pts and 10.6 pts. These are not written to `mde.json`.

**Why the price detectable gap is so small, and the caveat:**
- Haiku is close to deterministic. With the request, page and order fixed, almost every name buys the same product. The pilot found no spread between names beyond episode noise (sn = 0), so the main-run name averages are predicted to be very tight.
- With only 5 names per cell, a small true spread could hide. If sn were really 0.01 (1%), the after-Holm gap would be 1.9%. At 0.02 it would be 2.8%, at 0.03 3.9%, and at 0.05 6.3%.
- The paper should quote the pre-registered 1.4% and report the "achieved" detectable gap from the main run beside it (PLAN 6.5).
- **Narrow margin:** the frozen "quiet names" rule (PLAN 7) picked the **narrow 3% price margin** for Haiku, since the power to show equivalence at 3% is about 1.0.

**Gemini:** no usable estimate. Its small pilot had zero variance in the S0 and S1 cells (every name bought the same product), and too few V episodes per name for H4. It is exploratory anyway, so it is left out of `mde.json`.

## 5. Projected cost and time for the full run

These use the pilot token counts. Haiku prices are batch, and Luna prices are batch or Flex.

| Run | Episodes | Cost estimate | Time estimate |
|---|---|---|---|
| Haiku main | 32,640 | about $7.00 | Unverified. 1,152 episodes took 10 minutes in 3 batch waves, so likely 1 to 6 hours |
| Haiku M1 + planted + arm P | 8,480 | about $1.80 | Same as above |
| **Haiku total** | | **about $8.80 more, about $9.20 with today's spend, under the $15 cap** | |
| Luna main + M1 + planted + P | 41,120 | about $4.60 (assumes Luna's 1,530 in / 30 out tokens per call and Haiku's 1.34 calls per episode) | Not possible on free access: 50 requests per day is about 1,100 days. With money loaded and the Batch API, likely hours |
| Gemini reduced | 7,040 | $0 on the free tier ($4.20 notional at standard paid prices, about $2.10 at batch prices) | About 8,200 calls. At 500 per day that is **about 17 days**, too slow |
| OLMo | 5,280 | $0 | Not measured (nothing run before 7 pm, per the rule). Guess 6 to 12 hours overnight, unverified |
| Luna name check (rest) | 58 names x 5 | under $0.01 | About 290 calls, about 35 minutes at 10 per minute once quota allows |

## 6. Recommended adjustments (Ian decides)

1. **Fix the V second ask before the main run.** Add "Please pick one for me." to every scripted reply, or allow one more scripted turn ("Please choose one for me.") before counting no purchase. This is a prompt change in `data/tasks.json` / `src/harness/prompts.py`, not an analysis change.
2. **OpenAI:** to keep Luna as a confirmatory model, load the approved $5 to $10 and run Batch. Luna needs about $4.60 for everything. Then finish the Luna name check. Otherwise drop Luna: PLAN section 3 already shrinks the family to Haiku's 4 tests, and the name check stays on the 2-model rule.
3. **Gemini:** the free tier cannot run the reduced preset in time. Choose one:
   - (a) link billing with a hard cap of about $5 and use Batch (about $2.10)
   - (b) cut Gemini to what fits in 2 to 3 days of free quota (about 1,000 to 1,500 calls), for example S0 and V on the 16 pilot tasks x 40 core names x 1 slot = 1,280 episodes
   - (c) drop Gemini (it is in the cut order)
   
   Separately, finish the Gemini pilot after 3 am ET by rerunning the same command (15 episodes, about 20 calls).
4. **Keep the pre-registered detectable gap but word it carefully:** 1.4% for price (H1, H2) under the frozen rule, with the sensitivity line above. Commit `results/mde.json` before scoring the main run (done in this commit).
5. **Invalid product IDs** (0.4%) are fine to keep as an outcome. Optionally, shorter on-page IDs (P1 to P8) would remove them, but that changes what the agent sees, so only before the main run.
6. **Name check deviations to note in the methods appendix:**
   - the two-prompt population-statistics wording (nc3) and the trial history
   - the keep rule run with 2 models (9 of 10) because of Luna's daily limit
   - income and education guesses being sparse for Haiku because of refusals
7. **Still open from the harness report:** Ian's 20-page label spot check, and product details cut off mid-word on store pages.

## Files

- `src/name_check.py` is the name check runner and scorer.
- `src/harness/catalog.py` adds the `pilotsmall` preset.
- `src/harness/adapters/openai_api.py` has the 429 fix and pacing. `src/harness/config.py` sets the Luna pacing.
- Data: `data/name_check_results.csv` and `data/name_check_exclusions.csv` (empty).
- Logs:
  - `logs/name_check_*.jsonl` and the trial folders
  - `logs/pilot_haiku.*`, `logs/pilotsmall_haiku.*` and `logs/pilotsmall_flashlite.*`
  - `logs/run_stdout/`
  - `logs/spend.json`
- `results/mde.json` holds the detectable gaps.
- Tests: 56 pass, including the new `pilotsmall` layout test.

## Note added 11/4 evening: pilots used the pre-D3 pages

All pilots (Haiku, Gemini, and the Luna and OLMo pilots started this evening) ran on the pages from before PLAN.md deviation D3, which swapped 6 mislabeled products on 10 pages. Two pilot tasks touch those pages: `hair_leave_spray_coily_4c` (S page, over-budget item) and `twin_body_wash` (S and V, high women's item). Score pilot runs against the pre-D3 `data/pages.json` and `data/products.json` (git history), since the swapped product IDs are no longer in the current files.
