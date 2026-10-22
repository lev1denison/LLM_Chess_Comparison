# Chess difficulty and LLM success

Victor Le - DA401

**My research question:** Does human-rated Lichess puzzle difficulty predict an LLM's success?
I evaluate **GPT-OSS 120B** and **Gemini 3.5 Flash-Lite**. I measure whether each
model selects the official first move, with the board and legal choices supplied.

## My latest results: early_results_2

I started full collection and paused at the configured usage guards. My new
training-only checkpoint contains **404 Gemini answers: 174 correct (43.1%)**.
GPT-OSS has **no new bulk answers** because its local rolling-budget guard
paused collection before generation. I do not report that as 0% accuracy.

I fitted Gemini's provisional logistic regression and descriptive decision tree.
Its estimated odds ratio is **0.57 per 500 rating points** (ordinary 95% interval
0.46-0.71), adjusting for whether the puzzle requires multiple solver moves.
Success decreases as difficulty increases in this checkpoint. The tree selected
rating for its splits. These are exploratory training results; my 200 held-out
test puzzles remain unused and my final analysis plan is unchanged.

**Open [05 - Early results 2](notebooks/05_early_results_2.ipynb).**
My new figures are [accuracy](figures/early_results_2/accuracy.png),
[logistic regression](figures/early_results_2/logistic_regression.png) and
[decision trees](figures/early_results_2/decision_trees.png). I freeze this
checkpoint separately so later collection cannot overwrite it.

## My original 60-puzzle pilot

I completed and audited a pilot using the same 60 puzzles for both models.

| Model | Correct first moves | Incorrect legal moves | Format failures |
| --- | --- | --- | --- |
| GPT-OSS 120B | 21/60 (35%) | 38 | 1 |
| Gemini 3.5 Flash-Lite | 32/60 (53.3%) | 26 | 2 |

Both models returned all 60 responses without provider failures. I fitted
separate logistic regressions and descriptive decision trees. Gemini's odds
ratio is 0.51 per 500 rating points (95% interval 0.29-0.90); GPT-OSS's is 0.67
(0.39-1.17). These are exploratory results from a balanced, assisted sample.
I do not claim full puzzle solving, future accuracy or a model-family ranking.

**Start with [03 - Early results](notebooks/03_early_results.ipynb).**
It has two code cells, reads my saved results and makes no API calls.
My three figures are [accuracy](figures/early_results/accuracy.png),
[logistic regression](figures/early_results/logistic_regression.png) and
[decision trees](figures/early_results/decision_trees.png).

## My bulk run

I froze **1,000 fresh shared puzzles** with an **800 training / 200 test** split.
I kept my pilot prompts, model settings, scoring and final analysis plan.
I started full collection in notebook 04. Each provider advances independently
after its own capability and immutable-resume checks. I stop and save progress
when a provider completes or reaches a local/provider limit.

Both collectors are now paused. Gemini stopped at the conservative **480
logged project requests per provider day**, including earlier usage, with
404 research answers saved. GPT-OSS stopped at a saved local rolling-token
budget retry time. Neither stop was a new API rate-limit error in this session.
All 412 Gemini raw responses (8 capability checks plus 404 research answers)
passed the independent audit.

My saved earliest retry times are **October 22, 2026 at 1:17 AM New York** for
GPT-OSS and **3:00 AM New York** for Gemini. These are local guard eligibility
times, not guarantees of available provider quota; another pause is possible.
I have **596 Gemini puzzles and all 1,000 GPT-OSS puzzles** left to collect.

I use **[05 - Early results 2](notebooks/05_early_results_2.ipynb)** to freeze a
training-only checkpoint when collection stops. It estimates a provisional
regression and descriptive tree only when enough new training data exist.
It does not substitute pilot results for a model without new answers or use
my held-out test outcomes. My original pilot graphs remain in notebook 03.

I resume with **[04 - Bulk collection](notebooks/04_bulk_collection.ipynb)**,
`RUN_MODE = "bulk"` and `WAIT_FOR_QUOTA = False`. If I choose automatic waiting,
I set `WAIT_FOR_QUOTA = True` and keep my computer and kernel running.
I use **[06 - Final analysis](notebooks/06_final_analysis.ipynb)** after complete
audited collection for the unchanged primary regressions and held-out tree
prediction evaluation. I do not tune from interim graphs.

## My notebook order

The active numbers describe **the logical workflow**, not creation dates.

| Step | My notebook | Purpose |
| --- | --- | --- |
| 01 | `01_data_inspection.ipynb` | Inspect the source dataset |
| 02 | `02_chess_validation.ipynb` | Validate positions and extract features |
| 03 | `03_early_results.ipynb` | Review the completed 60-puzzle pilot |
| 04 | `04_bulk_collection.ipynb` | Collect/resume the frozen 1,000-puzzle study |
| 05 | `05_early_results_2.ipynb` | Review a separate frozen interim training checkpoint |
| 06 | `06_final_analysis.ipynb` | Run final regressions and held-out tree evaluation |

The old 08-10 numbers came from historical experiment stages. I moved those
notebooks, unchanged, into `notebooks/reference/` so they no longer look like
steps after the current workflow. Their frozen historical paths can be restored
from the verified archive when reproducing an older run.

## My project layout

- `notebooks/01_*` and `02_*`: my completed data inspection and validation; I do not rerun them unless the source changes.
- `notebooks/03_early_results.ipynb`: my completed 60-puzzle pilot results.
- `notebooks/04_bulk_collection.ipynb`: my frozen sample, operational check and resumable bulk collector.
- `notebooks/05_early_results_2.ipynb`: my separate exploratory bulk checkpoint.
- `notebooks/06_final_analysis.ipynb`: my prespecified final regressions and held-out tree evaluation.
- `notebooks/reference/`: my unchanged historical reliability, collection and analysis notebooks.
- `experiments/bulk_v1/`: my frozen bulk config, analysis plan, prompt and lightweight sample index. Earlier numbered protocols are historical.
- `data/`: my raw responses, audits and fitted models. It is Git-ignored, so I back it up separately.
- `figures/early_results_2/`: my latest three interim figures; `early_results/` preserves my original pilot figures.
- `writing/`: my three original PDFs, unchanged, and a short README.
- `archive/`: my retired expansion notebooks and superseded figures, with verified hashes.

I use the project's `.venv` kernel. I keep the Groq and Google keys in
Git-ignored `api_key.txt` and `google_api.txt`. I back up `data/experiments/bulk_v1/`, `data/analysis/early_results_2/` and `data/analysis/bulk_v1/` separately because they are Git-ignored. I have not committed or pushed this update.
