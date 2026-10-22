# Chess difficulty and LLM success

Victor Le - DA401

**My research question:** Does human-rated Lichess puzzle difficulty predict an LLM's success?
I evaluate **GPT-OSS 120B** and **Gemini 3.5 Flash-Lite**. I measure whether each
model selects the official first move, with the board and legal choices supplied.

## My current results

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

## My next steps

**My pilot supports moving to bulk collection. I still need to prepare the bulk
workflow before launching it; I have not started a bulk run.**

1. I will freeze a fresh shared sample of **1,000 puzzles**, excluding all previously exposed or reserved puzzles, and record the sampling seed.
2. I will create a separate bulk notebook with the existing prompts/settings, automatic saving, provider-specific pacing and pause/resume across daily quotas. My reference collectors are fixed to 60 cases.
3. I will collect both models' answers on the same sample without retrying wrong answers or replacing completed responses.
4. I will audit the results and fit separate regressions and trees. I will decide any holdout split and analysis changes before seeing the bulk answers.

On the free tiers, I budget roughly **2-3 quota days for Gemini** and **9-12 days
for GPT-OSS**, based on my pilot usage, with checks and retries included as a
planning buffer. I will verify the account limits before starting:
[Groq](https://console.groq.com/docs/rate-limits) and
[Google AI Studio](https://aistudio.google.com/rate-limit).

## My project layout

- `notebooks/01_*` and `02_*`: my completed data inspection and validation; I do not rerun them unless the source changes.
- `notebooks/03_early_results.ipynb`: my current two-model results and next steps.
- `notebooks/08_*`, `09_*`, `10_*`: my validated pilot collection/analysis references, retained to support the bulk implementation.
- `experiments/`: my frozen protocols and stage index; earlier numbered stages are historical.
- `data/`: my raw responses, audits and fitted models. It is Git-ignored, so I back it up separately.
- `figures/early_results/`: my current three figures.
- `writing/`: my three original PDFs, unchanged, and a short README.
- `archive/`: my retired expansion notebooks and superseded figures, with verified hashes.

I use the project's `.venv` kernel. I keep the Groq and Google keys in
Git-ignored `api_key.txt` and `google_api.txt`. I have not committed or pushed
this cleanup.
