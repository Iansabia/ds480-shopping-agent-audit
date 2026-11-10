# Does Race or Gender Affect How Shopping Agents Buy? A Paired-Name Audit

Code, data and results for a paired-name audit of two AI shopping agents, Claude Haiku 5.5 and GPT-6 Luna, for DS480 Data, Society, and AI Ethics (Boston University, Fall 2026). Each agent got the same shopping requests on a mock store, and only the buyer's account name changed.

- **Paper:** [`Sabia_Ian_DS480_Paper2.pdf`](https://iansabia.github.io/audit/Sabia_Ian_DS480_Paper2.pdf)
- **Technical Appendix:** [`APPENDIX.md`](APPENDIX.md). Section labels such as A4 or B2 match the citations in the paper.
- **Frozen analysis plan:** [`PLAN.md`](PLAN.md)
- **Test harness:** [`HARNESS_README.md`](HARNESS_README.md)
- **Pilot and cost:** [`PILOT_REPORT.md`](PILOT_REPORT.md), [`COST_ESTIMATE.md`](COST_ESTIMATE.md)

## Setup

Python 3.12 or newer.

```bash
python3 -m venv .venv
.venv/bin/pip install -r analysis/requirements.txt pytest google-genai
.venv/bin/python -m pytest -q tests
```

The tests and the analysis never call a model. The figure tests need a local Chrome for kaleido (see `analysis/requirements.txt`). Live agent runs also need `anthropic`, `openai` and `requests`, plus API keys in the environment (or in a `.env` file, read with `python-dotenv`).

This repository holds the study's code, data and results; the paper's own draft files are not part of it. For that reason commit hashes after `94dff45` (11/4) differ from the ones quoted in `logs/*.manifest.json`, `PLAN.md` and `PILOT_REPORT.md`, which come from my private working copy. Match those by commit date.

## Layout

| Folder | Contents |
|---|---|
| `src/` | Name sets, account profiles, catalog builder, mock store and agent runner |
| `data/` | Names, catalog and task files (raw Amazon review dumps are not included) |
| `logs/` | Outcomes of every run; full turn logs of the main runs are gzipped (`*.turns.jsonl.gz`) |
| `analysis/` | Analysis and figure scripts |
| `results/`, `paper/tables/` | Test results and the tables behind every number |
| `paper/figures/` | Figures |
| `tests/` | Harness and analysis tests |

## The course submission zip

`Sabia_Ian_DS480_Paper2_Code.zip`, submitted on Blackboard, is this repository at one commit with the large files left out so it stays small:

- **Included:** all code, tests, data, results and tables, the outcome file of every run (`logs/*.outcomes.csv`, with `logs/*.manifest.json` and `logs/spend.json`), the final figures (`paper/figures/paper/`), the data behind each figure (`paper/figures/*.csv`), and these documents.
- **Left out:** the raw turn-by-turn logs (`logs/*.jsonl`, `logs/*.turns.jsonl.gz`, `logs/run_stdout/`) and the draft and alternate versions of the figures in `paper/figures/`.

Everything left out is in the full repository: https://github.com/Iansabia/ds480-shopping-agent-audit. The tests and the analysis run on the zip alone. Three things need the raw turn logs from the full repository: re-scoring a run from scratch (`src/harness/score.py`), recounting tokens for the cost table, and `analysis/paperfigs/figA10_same_inputs.py` (Appendix Figure A5). Their outputs are included (`logs/*.outcomes.csv`, `paper/tables/table3_cost.md`, `paper/figures/figA10_same_inputs.csv`).
