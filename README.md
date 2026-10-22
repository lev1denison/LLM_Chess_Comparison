# Assisted one-move chess-puzzle accuracy

Victor Le - DA401

I study **whether human-rated difficulty and board characteristics predict an
LLM's accuracy on chess puzzles requiring exactly one solver move**. I evaluate
GPT-OSS 120B and Gemini 3.5 Flash-Lite on the same 1,000 fresh positions.

## What assisted means

I give each model the board in FEN, a piece list and **every legal move in
alphabetical order**. I do not rank the choices or provide the answer, rating,
theme labels, game-phase labels or engine scores. A correct answer must match
the official solution move. This is assisted one-move solving, not unaided move
generation or multi-step puzzle solving.

## Current status and next step

I completed the same 100-puzzle training pilot for both models:

| Model | Correct / puzzles | Accuracy |
| --- | --- | --- |
| GPT-OSS 120B | 35 / 100 | 35% |
| Gemini 3.5 Flash-Lite | 53 / 100 | 53% |

**Open [05 - Early results](notebooks/05_early_results.ipynb).** My three figures
are [accuracy](figures/one_move_v1/early/accuracy.png),
[logistic regression](figures/one_move_v1/early/logistic_regression.png) and
[decision trees](figures/one_move_v1/early/decision_trees.png).

My provisional pooled regression estimates an odds ratio of **0.50 per 500
rating points** (ordinary 95% interval **0.35-0.73**), adjusting for numeric
board characteristics and model identity, with puzzle-clustered standard
errors. I label these exploratory training results; the trees are descriptive.
The fuller theme/phase regression and held-out evaluation remain pending.

All 216 raw responses (200 research answers plus 16 capability checks) passed
the audit. Both 100-case answer sets replayed with zero new network requests
and unchanged saved responses. My 200 held-out puzzles remain unused, and I
have **900 puzzles left per model**. No bulk run is running.

My first GPT-OSS attempt stopped at a conservative local token estimate. On
retry I temporarily bypassed only that daily estimate; **Groq accepted all
94 remaining requests without a rate-limit error**. I kept the prompt, model
settings, scoring, sample and analysis plan unchanged. This operational retry
is recorded in `data/experiments/one_move_v1/gpt_oss/provider_retry_audit.json`.
I have now removed automatic stops based on local daily usage estimates.
The collector follows provider headers and errors: short rate limits wait and
retry; an actual daily limit saves progress and pauses only that provider.
I resume later without requesting completed answers again.

My bulk preparation is complete, but **bulk collection has not started**.
When I am ready, I open notebook 04 and set `RUN_MODE = "bulk"` to collect the
remaining 900 puzzles per model. `WAIT_FOR_QUOTA = False` saves and pauses at
actual limits so I can resume the next day; `True` waits for the saved retry
time while the computer and kernel remain running. The saved mode is `setup`,
which makes no API or metadata requests.

The sample contains **979 mate-in-one-tagged puzzles**, so conclusions mainly
concern mating tactics. I reserve 800 puzzles for training and 200 for held-out evaluation. The first
100 training puzzles, shared by both models, form my early checkpoint and
count toward the final 1,000 if the protocol stays unchanged.

## My notebook order

The numbers follow the workflow, not file creation dates.

| Step | Notebook | Purpose |
| --- | --- | --- |
| 01 | [Data inspection](notebooks/01_data_inspection.ipynb) | Completed source-data inspection |
| 02 | [Chess validation](notebooks/02_chess_validation.ipynb) | Completed position validation and feature extraction |
| 03 | [Prepare study](notebooks/03_prepare_study.ipynb) | Freeze fresh puzzles, split and board features; no API calls |
| 04 | [Collect answers](notebooks/04_collect_answers.ipynb) | Run/resume the 100-case pilot, then the 1,000-case collection |
| 05 | [Early results](notebooks/05_early_results.ipynb) | Freeze pilot accuracy and supported provisional regression/tree graphs |
| 06 | [Final analysis](notebooks/06_final_analysis.ipynb) | Fuller pooled regression and held-out XGBoost evaluation after complete collection |

I do not rerun 01 or 02 unless the source data changes. Notebook 04 is saved in
**setup mode** so running it for verification makes no API requests.

## What I analyze

I record human rating, legal-move count, piece count, solver-relative material
balance, tactical tags, game phase and side to move. My smaller early regression
uses the numeric board features and model identity. My fuller final regression
adds frozen theme and phase encoding and accounts for repeated puzzles through
puzzle-clustered standard errors. Solution length is constant and is excluded.
My final predictive models are **XGBoost**, following my research design:
150 boosted trees per deployment, maximum depth 3, learning rate 0.05 and fixed
regularization. I train on 800 puzzles per model and evaluate once on 200
held-out puzzles. I perform no hyperparameter search, early stopping or test
set tuning. The current pilot's small CART trees remain descriptive figures;
they are not XGBoost. Training feature importance is descriptive, not causal.

My [final XGBoost plan](experiments/one_move_v1/final_analysis_plan.json) records
this amendment after the pilot and before held-out evaluation. The original
`analysis_plan.json` remains frozen for the pilot; the new plan supersedes its
final CART and quota sections. The primary regression and feature recipe are
unchanged. I have not trained XGBoost on actual research outcomes yet.

## Why I switched from local to hosted models

My earlier feasibility checks produced:

| Earlier experiment | Correct / completed | What was scored |
| --- | --- | --- |
| Three local models | 0 / 225 | Complete puzzle solutions |
| Three local models | 6 / 144 (4.2%) | Assisted first moves |
| Hosted GPT-OSS 120B | 21 / 60 (35.0%) | Assisted first moves |
| Hosted Gemini | 32 / 60 (53.3%) | Assisted first moves |

I moved to hosted models because I needed enough successes and failures to
analyze board characteristics. **These are historical feasibility results, not
results of the new one-move study or a controlled local-versus-hosted ranking.**
The local and hosted samples and prompt formats differ. The two hosted pilots
used the same 60 puzzles. [Evidence counts and source hashes](experiments/one_move_v1/background_evidence.csv)
link back to saved raw-data tables; notebook 03 displays this evidence clearly.

## Project folders

- `experiments/one_move_v1/`: my [revised protocol](experiments/one_move_v1/protocol.md), fixed settings, frozen pilot plan, final XGBoost amendment, prompt and sample index.
- `notebooks/`: the six workflow notebooks above.
- `figures/one_move_v1/`: only the new study's figures, created after real answers exist.
- `data/validation/`: my reusable validated puzzle features.
- `data/experiments/one_move_v1/`: my new frozen sample and, later, raw responses and audits.
- `data/analysis/one_move_v1/`: my new early/final analysis outputs.
- Older raw data under ignored `data/` remains only for provenance, exclusions and quota accounting; it is not pooled into the new study.
- `writing/`: my original three PDFs, unchanged. The revised protocol documents differences from those earlier plans.

I removed the old archive and superseded active experiments, figures and
notebooks at this restart. I keep credentials in ignored `api_key.txt` and
`google_api.txt`; I never commit them. The large source and all `data/` files
are also Git-ignored, so a clone needs those local data files to reproduce the
notebooks. I back up the new study's data separately. I have not committed or
pushed this revamp.
