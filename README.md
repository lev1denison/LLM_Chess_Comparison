# Human-rated chess difficulty and local LLM performance

Victor Le — DA401 capstone

The project asks whether human-rated Lichess puzzle difficulty predicts LLM
performance and whether position features add predictive information.

## Start here

Open **[04 — First-move results](notebooks/04_first_move_results.ipynb)** for current
executed results, the exact random baseline and preliminary model status. Read
**[the current report](writing/first_move_pilot_report.md)** for methods, findings,
limitations, changes and the next research decision.

The original full-sequence pilot produced 0/225 successes. Revised prompt
development improved format and legality but produced no complete solutions.
The current experiment measures **assisted first-move correctness** as a separate
outcome. Earlier scores are unchanged; a correct first move does not imply that
a multi-step puzzle was solved.

## Notebook workflow

Use the project's `.venv` Python kernel. Start Jupyter/VS Code in this repository.
Installed package versions are recorded in `requirements.txt` for environment
recreation; the current environment is already configured.

| Notebook | Purpose | When to run |
| --- | --- | --- |
| [01 — Data inspection](notebooks/01_data_inspection.ipynb) | Original audit and distributions | Historical outputs retained; rerun if needed |
| [02 — Chess validation](notebooks/02_chess_validation.ipynb) | Board legality and feature extraction | Already completed for 6,157,341 puzzles; rerun for source/method changes only |
| [03 — First-move pilot](notebooks/03_first_move_pilot.ipynb) | Review, sample, freeze, collect and audit | Requires Ollama; resumes completed collection |
| [04 — First-move results](notebooks/04_first_move_results.ipynb) | Chance comparison and eligible models | Read or rerun; no inference calls |

Local models: `gemma3:4b`, `qwen3:8b`, `llama3.1:8b`. The current prompt and
settings are in [experiments/first_move_v1](experiments/first_move_v1/README.md).

## Project layout

```text
notebooks/                       Four active numbered notebooks
experiments/first_move_v1/        Current prompt, config and protocol
data/                            Source, samples, raw logs and tables (Git-ignored)
figures/first_move_v1/            Current plots; older folders retained
writing/                         Current report and historical documents
archive/                         Verified legacy code ZIP and restoration guide
```

Former loose scripts, duplicate setup notebooks and placeholder regression code
are preserved in [the archive](archive/README.md). Existing data and figures
retain their paths. Historical reports' `code/` references refer to the restorable
archived layout.

## Data and interpretation

Source: [Lichess puzzle database](https://database.lichess.org/#puzzles). Snapshot
hashes are saved in experiment metadata. Back up `data/` separately; it is ignored
by Git and is not included in the code archive.

The current balanced 48-puzzle sample is exploratory and uses legal-move assistance
and exact official first-move matching. It does not establish population accuracy
or general LLM chess ability. Model family, size and quantization differ. Merely
fitting a classifier does not establish above-chance ability or a stable human
difficulty relationship.
