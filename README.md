# Assisted one-move chess-puzzle accuracy

Victor Le - DA401

I study how human-rated puzzle difficulty and board characteristics relate to LLM success. I give each model the FEN, a piece list and every legal move in alphabetical order. I count the official solution move when it appears in the visible answer, including explanations or formatting. I use the same tolerant extraction rule for all models. I do not provide the answer, rating, theme labels, engine scores or tools.

## Current results and next step

| Model | Saved research answers | Status |
| --- | ---: | --- |
| GPT-OSS 120B | 402 / 1,000 | 164 correct (40.8%); paused at Groq quota |
| Gemini 3.5 Flash-Lite | 1,000 / 1,000 | 557 correct (55.7%); collection complete |
| Claude Haiku 5.5 | 1,000 / 1,000 | 490 correct (49.0%); collection complete |

### Early results 2: the same first 400 puzzles

I created [05b - Early results on 400 shared puzzles](notebooks/05b_early_results_400.ipynb) as a separate checkpoint using tolerant scoring:

| Model | Correct / puzzles | Accuracy |
| --- | ---: | ---: |
| GPT-OSS 120B | 164 / 400 | 41.0% |
| Gemini 3.5 Flash-Lite | 229 / 400 | 57.25% |
| Claude Haiku 5.5 | 200 / 400 | 50.0% |

I fitted a pooled logistic regression with the full frozen board-feature recipe and model identity, using 400 puzzle clusters. I also saved three XGBoost models trained on these 400 puzzles. The [accuracy](figures/one_move_v1/early_results_400/accuracy.png), [logistic regression](figures/one_move_v1/early_results_400/logistic_regression.png) and [XGBoost feature-importance](figures/one_move_v1/early_results_400/xgboost_feature_importance.png) figures are in `early_results_400`.

All selected cases are original training puzzles. My shared five-fold cross-validation within these 400 cases predicts LLM success; it is exploratory and does not use or replace the final 200-puzzle test set. I made no API calls. My [checkpoint plan](experiments/one_move_v1/early_400_plan.json) records the selection and fixed settings. I can review these early results now while GPT-OSS collection remains incomplete.

My original strict 100-puzzle pilot scored **35% for GPT-OSS** and **53% for Gemini**. Under my amended tolerant scoring, the same 100 training puzzles score **35% GPT-OSS, 54% Gemini and 46% Claude**. The overall counts in the table use different sample sizes and are not a matched comparison. I preserve its [early-results notebook](notebooks/05_early_results.ipynb) and figures unchanged. The original graphs retain strict scoring and are historical results, not the current tolerant analysis.

I am adding Claude as a third deployment, retaining GPT-OSS and Gemini. My [Claude amendment](experiments/one_move_v1/claude_amendment.md) records its settings and the capability-format diagnostic. I now use the [documented tolerant scoring amendment](experiments/one_move_v1/scoring_amendment.md). Claude scored **46/100 (46%)**, compared with 28/100 under strict formatting; all 24 formerly unparseable answers are now recognizable, and 18 become correct. I preserve strict scores and raw answers. The 100 puzzle calls cost approximately **$0.0577**, or **$0.0589 including eight capability checks**. At the pilot average, another 900 puzzles would cost about **$0.52**; this is an estimate rather than a spending guarantee. I approved Claude bulk collection after reviewing its pilot accuracy and cost. The [notebook 04 report](notebooks/04_collect_answers.ipynb) and ignored `data/experiments/one_move_v1/claude_haiku/pilot_report.json` record the result. I have not added GPT-6 Luna.

I use the same frozen **1,000 unique puzzles** and **800 training / 200 test split** for every deployment. The 100-puzzle pilot is part of the training set, so it leaves 900 answers per model. Completed answers are reused. I rescore saved responses locally without new calls; current `results.csv` files contain tolerant `success` and original `strict_success`, while immutable raw outcome logs retain historical scores. Because **979 puzzles carry the mate-in-one tag**, my conclusions mainly concern mating tactics rather than all chess puzzles.

## Notebook order

| Step | Notebook | Purpose |
| --- | --- | --- |
| 01 | [Data inspection](notebooks/01_data_inspection.ipynb) | Inspect source data |
| 02 | [Chess validation](notebooks/02_chess_validation.ipynb) | Validate boards and extract characteristics |
| 03 | [Prepare study](notebooks/03_prepare_study.ipynb) | Freeze sample, features and split; no API calls |
| 04 | [Collect answers](notebooks/04_collect_answers.ipynb) | Resume collection; currently Claude-only bulk mode |
| 05 | [Early results](notebooks/05_early_results.ipynb) | Preserve the original two-model strict pilot graphs |
| 05b | [Early results 2: 400 puzzles](notebooks/05b_early_results_400.ipynb) | Current three-model regression and exploratory XGBoost checkpoint |
| 06 | [Final analysis](notebooks/06_final_analysis.ipynb) | Original two-model pooled regression and held-out XGBoost; pending complete collection |

I do not rerun 01-03 to collect more answers. Notebook 04 saves each response, preserves completed wrong answers and pauses at provider limits. Its current controls select only Claude in bulk mode. Claude has completed all 1,000 cases, so its saved answers are reused on rerun. I must select GPT-OSS explicitly to resume its remaining 598 cases. Analysis notebook 05b makes no API calls.

## My analysis

I record rating, legal-move count, piece count, solver-relative material balance, tactical themes, game phase and side to move. The final regression uses the frozen numeric, theme and phase predictors plus model identity, with puzzle-clustered standard errors. Solution length is constant. Side to move is descriptive rather than a fixed regression predictor.

I plan separate XGBoost models with 150 trees, depth 3 and learning rate 0.05, trained on 800 puzzles and evaluated on 200 held-out puzzles, without tuning on test answers. The original strict pilot's small CART plots are descriptive and are not XGBoost. I created separate tolerant-scoring figures and exploratory models in notebook 05b; the original strict figures remain unchanged. I have not fitted final models. Before analyzing three deployments, I must explicitly extend notebook 06's two-model implementation and final plan; I have not fitted a final three-model analysis.

## Why I switched from local to hosted models

| Historical feasibility check | Correct / completed |
| --- | ---: |
| Three local models, full puzzle solutions | 0 / 225 |
| Three local models, assisted first moves | 6 / 144 |
| Hosted GPT-OSS, assisted first moves | 21 / 60 |
| Hosted Gemini, assisted first moves | 32 / 60 |

I needed enough successes and failures to study puzzle characteristics. These historical checks used different samples and prompts, so they are not a controlled local-versus-hosted comparison or results for the current study. I retain the [evidence counts and source hashes](experiments/one_move_v1/background_evidence.csv).

## Files and credentials

- `experiments/one_move_v1/`: protocol, frozen original plans, prompt, settings, sample index, Claude pilot amendment and tolerant scoring amendment
- `data/experiments/one_move_v1/`: frozen sample and separate `gpt_oss/`, `gemini/` and `claude_haiku/` response logs, outcomes, checkpoint CSVs and audits. Live counts come from `outcomes.jsonl`; summaries refresh at stops
- `data/analysis/one_move_v1/` and `figures/one_move_v1/`: analysis artifacts, original pilot figures and the new `early_results_400` checkpoint
- `writing/`: my three original PDFs writing

