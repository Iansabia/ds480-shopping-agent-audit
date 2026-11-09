# First-name counts in OLMo training data (olmo_name_counts.csv)

Fetched 2026-11-05, 22:19 to 22:33 UTC. Feeds Figure A3 (log count of each first name in OLMo's
training index vs that name's clear-request price gap, Spearman rho).

## What is in the file

Long format, one row per first name per index: 82 names x 5 indexes = 410 rows.

| Column | Meaning |
|---|---|
| first | First name from `names.csv` (all 82 distinct; none were blank) |
| index | Which index the count comes from (table below) |
| query | Exact string sent. Always one space plus the capitalized name, e.g. `" Jamal"`. The leading space is part of the value |
| count | Exact number of matches in that index |
| retrieved_at | UTC time of the reply (ISO 8601) |
| approx | Whether the server estimated the count. False for every row |
| tokens, token_ids | How the index's tokenizer split the query |
| endpoint | URL the request went to |
| index_total_tokens | Size of the index in tokens (from an empty-string count query), for per-token rates |
| token_check | `ok` if the tokens show the name as a word that follows a space. All 410 rows are `ok` |
| word_ambiguity_flag | Filled in for 16 names that are also a common word, title, place or religious figure (my judgment, not measured) |

## Indexes

| index | What it is | Tokens | Endpoint |
|---|---|---|---|
| `olmo-3-0625-32b-instruct` | **OLMo 3 32B Instruct training data** (Ai2's own infini-gram service, the one behind OlmoTrace) | 4.66T | infinigram-api.allen.ai |
| `v4_olmo-mix-1124_llama` | OLMo 2 pretraining mix (OLMo-mix-1124) | 4.58T | api.infini-gram.io |
| `v4_olmo-2-1124-13b-instruct_llama` | OLMo 2 13B Instruct, all training stages | 4.61T | api.infini-gram.io |
| `v4_dolma-v1_7_llama` | Dolma v1.7 (OLMo 1.7 data) | 2.60T | api.infini-gram.io |
| `v4_piletrain_llama` | The Pile, train split | 0.38T | api.infini-gram.io |

**How OLMo 3 was reached.** The public API (api.infini-gram.io) knows the OLMo 3 index names
(`v4_olmo-3-7b-instruct_olmo2` and the two Think indexes) but every query to them failed with
HTTP 500 and a server-side storage error ("InvalidAccessKeyId" on S3). A made-up index name gives
HTTP 400 "Invalid index" instead, so the indexes exist but are broken on the server. The Hugging
Face web demo shows "Error" for them too. Ai2's separate service at
`https://infinigram-api.allen.ai` (source: github.com/allenai/infinigram-api) lists
`olmo-3-0625-32b-instruct` and answered every query, exactly, in about 1.3 seconds. The attempts
on the public API are saved in `raw/infini_gram/olmo3_public_api_probe.json`.

**Which OLMo 3 data this is.** Our agent is OLMo 3 **7B** Instruct. The working index is the
**32B** Instruct model's data. Per Ai2's index config, both are built on the same shared base
index (`dolma2-0625-base-shared`). The 32B index adds 32B-specific data, and it does not include
the 7B-specific parts (`dolma2-0625-v01-7b`, `dolci-instruct-sft-7b`). So the paper should say
"OLMo 3 training data (the 32B Instruct index, which shares its base pretraining data with
7B)", not "OLMo 3 7B's exact training data". The index holds 4.66T tokens, less than the roughly
5.9T-token pretraining mix Ai2 reports and the 6.0T the web demo lists for the 7B index, so it may
not cover every token the model saw (not verified). The other four indexes are related corpora,
not OLMo 3's data.

## Query rule

- Case-sensitive, capitalized name, preceded by one space: `" " + first`. The same string goes to every index.
- Why the space: OLMo 3 uses a GPT-style tokenizer where a word after a space is a different token
  (`ĠJamal`) from the same letters with no space (`Jam` `al`). In running text a name almost always
  follows a space. On the Llama-2 indexes, `"Jamal"` and `" Jamal"` tokenize the same way
  (`▁Jam` `al`), so the rule means the same thing on every index.
- Matching is on token sequences. A count includes the name followed by anything that starts a new
  token, so "Jamal's" counts. For multi-token names (36 of 82 on OLMo 3, e.g. `ĠT ion na`) a longer
  word with the same opening tokens would also count.

## Caveats

1. These are counts of a string, not of people with that name. They include surnames (Scott, Lamar),
   famous people, and other meanings. The 16 flagged names are the worst cases. May (377M on OLMo
   3) is mostly the month, and Salvador picks up "El Salvador". Several core names are flagged (Heaven,
   Ebony, Hilary, Tyrone, Luke, and alternates Precious, Marquise, Lamar, Jay). Run Figure A3 with and
   without flagged names.
2. Names at the start of a line or after a quote or bracket are missed, so counts are lower bounds.
   For OLMo 3 the no-space matches are saved separately in
   `raw/infini_gram/olmo3_nospace_counts.csv` (median about 22% of the with-space count). That
   query also matches inside longer words, so it is not in the main file.
3. Raw counts include duplicate documents. Use log counts or ranks, not raw ratios.
4. The indexes agree closely. Spearman rho between log counts on any two indexes is 0.99 or higher.
   Each index correlates with SSA births (1950 to 2005) at rho of about 0.80.
5. Counts are a snapshot of the services on 2026-11-05. Ai2 can change or remove its index.

## Reproduce

The fetch script and its cached replies sit under `data/raw/`, which is not part of this repository. With a local copy:

`.venv/bin/python data/raw/infini_gram/fetch_name_counts.py` (add `--skip-probe` to skip the public
OLMo 3 attempts). Requests go one at a time with a 1.5 second pause and up to 6 tries with backoff.
Every raw reply is cached in `raw/infini_gram/responses.jsonl`, so a rerun only asks for what is
missing. Log: `raw/infini_gram/run.log`. This file is deliberately not named `name_freq.csv`, so the
frozen main analysis keeps its SSA covariate.
