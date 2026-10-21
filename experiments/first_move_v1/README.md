# Assisted first-move pilot, version 1

Implementation: `notebooks/03_first_move_pilot.ipynb`. Analysis:
`notebooks/04_first_move_results.ipynb`. No separate active Python runner is needed.

`config.json` fixes the outcome, models, generation settings, sample design,
baseline, multiple-testing correction, split and modeling gate. `prompt.txt` is
shared across models and contains no official answer or human rating.

The 48 fresh puzzles balance three rating groups and two solution-length groups.
All 150 original or reserved IDs are excluded. Sampling and the 36/12 puzzle
train/test split precede inference. The previous reserved 75 remain unused.

Success means matching the official first solver move. Inputs include FEN, a
piece list and legal UCI choices; JSON output is constrained to those choices.
This is assisted move selection, not spontaneous legality or complete solving.
Qwen thinking is disabled. All models use the same 256-token output budget.

Baseline success is exactly `1 / legal_moves` per puzzle. Notebook 04 computes
the exact Poisson-binomial upper tail and Holm-adjusted comparisons for the three
LLMs. These are exploratory results on a balanced pilot, not population estimates.
Legal alternatives are not engine-adjudicated.

The manifest freezes executable source cells, prompt, config, model digests,
sample hash and archive hash. Completed attempts are skipped on rerun. Changed
inputs require a new experiment version. Raw records and audits are written to
`data/experiments/first_move_v1/`; derived outputs to `data/analysis/first_move_v1/`.
These data folders need a separate backup.

Official references: [chat API](https://docs.ollama.com/api/chat) and
[structured outputs](https://docs.ollama.com/capabilities/structured-outputs).
