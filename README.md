# Does Race or Gender Affect How Shopping Agents Buy? A Paired-Name Audit

Code, data and results for a paired-name audit of two AI shopping agents, Claude Haiku 5.5 and GPT-6 Luna, for DS480 Data, Society, and AI Ethics (Boston University, Fall 2026). Each agent got the same shopping requests on a mock store, and only the buyer's account name changed.

- **Paper:** [`Sabia_Ian_DS480_Paper2.pdf`](Sabia_Ian_DS480_Paper2.pdf)
- **Technical Appendix:** [`APPENDIX.md`](APPENDIX.md). Section labels such as A4 or B2 match the citations in the paper.
- **Frozen analysis plan:** [`PLAN.md`](PLAN.md)
- **Test harness:** [`HARNESS_README.md`](HARNESS_README.md)
- **Pilot and cost:** [`PILOT_REPORT.md`](PILOT_REPORT.md), [`COST_ESTIMATE.md`](COST_ESTIMATE.md)

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
