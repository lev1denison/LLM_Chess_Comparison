# Code Folder

Run from the repository root using `.venv/Scripts/python.exe` on Windows.

1. `prepare_sample.ipynb`: completed reproducible 75-puzzle sample and official answer recovery.
2. `setup_llms.ipynb`: read-only checks for the three installed Ollama models; no API keys needed.
3. `test_puzzle_runner.py`: local scoring checks without inference.
4. `run_llm_puzzles.py --stage smoke`: fixed five-puzzle trial per model.
5. `run_llm_puzzles.py --stage pilot`: remaining 75-puzzle collection, reusing completed smoke attempts.
6. `audit_pilot_results.py`: independently replay all saved requests and verify outcomes.
7. `early_results.ipynb`: rebuild descriptive summaries and eligible preliminary models.

`llm_config.json` and `chess_prompt_v1.txt` define the local direct-answer experiment.
The manifest freezes configuration, prompt, sample hash, and model digests. Changing
any of these requires a separate experiment directory. Qwen thinking is explicitly
disabled. All models receive FEN and side to move, without solution metadata or tools.

Raw requests and outcomes are under `data/experiments/local_pilot_v2/`. Generated
analysis is under `data/analysis/local_pilot_v2/`, and figures under
`figures/local_pilot_v2/`. Existing Git rules exclude data; back up those folders separately.

Scores require the full official solver sequence. Legal alternatives are retained
as mismatches and have not been engine-adjudicated. Infrastructure failures are
unscored and retried on resume. Output-budget exhaustion counts as a protocol failure.
Strict UCI parsing excludes answers in other move notations. A one-class outcome
prevents fitting meaningful binary classifiers; the analysis reports this explicitly.
