# First-move pilot and project reorganization

## What was done

1. Preserved all prior code, prompts, configurations and executed notebooks in a
   verified ZIP archive. Prior raw data and figures were retained. The original
   checkpoint is verified by SHA-256 even after its code is relocated to the archive.
2. Reviewed all five previously correct assisted first moves. Each is legal and
   exactly matches its official first move; later failures were retained. This
   does not establish that other legal alternatives were objectively wrong.
3. Created a new, fixed first-move experiment. The outcome is assisted official
   first-move selection, a change from the earlier full-sequence outcome.
4. Sampled 48 fresh puzzles: 8 in each of three rating groups crossed with one-move
   versus multi-move solutions. Excluded all 75 original and all 75 previously
   reserved puzzles. The earlier reserved sample remains unused.
5. Froze a 36/12 puzzle train/test split before inference. All three models see
   the same 48 puzzles, with fresh independent requests and no answer metadata.
6. Used FEN, an explicit piece list, alphabetically sorted legal UCI choices and
   output constrained to those choices. Qwen thinking is disabled. Temperature 0,
   seed 401, 256 output tokens and 4096 context are fixed across models.
7. Logged all raw requests/responses and scored one move per puzzle. Exact official
   matching is the primary outcome; infrastructure failures are unscored. An audit
   reconstructs requests and verifies every outcome.
8. Compared each model with the exact uniform-random legal-move expectation using
   a Poisson-binomial tail calculation, with Holm adjustment for three comparisons.
9. Fit preliminary predictive models only if the fixed training data contain at
   least 5 successes and 5 failures. This is a computational readiness check, not
   a statistical power claim. Sparse inference remains explicitly limited.

## Primary results

| llm_name | n | correct | accuracy | random_expected_correct | random_expected_accuracy | accuracy_minus_chance | exact_p_above_chance | holm_adjusted_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gemma3:4b | 48 | 1 | 0.020833 | 1.983845 | 0.04133 | -0.020497 | 0.87272 | 1.0 |
| llama3.1:8b | 48 | 2 | 0.041667 | 1.983845 | 0.04133 | 0.000337 | 0.599529 | 1.0 |
| qwen3:8b | 48 | 3 | 0.0625 | 1.983845 | 0.04133 | 0.02117 | 0.318256 | 0.954769 |

## Modeling status

Fitted regularized logistic regression and shallow decision tree. Sparse pilot results are exploratory demonstrations, not stable estimates.

Clustered coefficient inference deferred: only six successes in the entire pilot; not enough information for reliable association estimates.

| model | test_n | test_successes | predicted_successes | accuracy | balanced_accuracy | roc_auc | brier_score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| majority_baseline | 36 | 1 | 0 | 0.972222 | 0.5 | 0.5 | 0.027349 |
| logistic_regression | 36 | 1 | 0 | 0.972222 | 0.5 | 0.485714 | 0.02934 |
| decision_tree | 36 | 1 | 0 | 0.972222 | 0.5 | 0.285714 | 0.034038 |

Only one of 36 test attempts was correct. At the default decision threshold, all three classifiers predicted every test attempt as incorrect. Their 97.2% accuracy therefore matches the majority baseline and does not show useful success detection. ROC-AUC is particularly unstable with one positive test observation.

## Recommended next decision

This pilot does not establish above-chance assisted first-move performance after correcting for three model comparisons. Do not scale the same protocol yet; assess a more capable deployment or narrow the research question before further main-study collection.

## Interpretation limits and design amendment

The 48-puzzle sample deliberately balances rating and solution length and is not
population representative. Inference concerns these quantized local deployments
under the specified assistance and generation limits. Correctness is official-line
agreement; no engine adjudicates alternative first moves. First-move success does
not mean a multi-step puzzle was solved. The frozen research-design PDFs are
historical documents; the revised primary outcome and assistance level must be
described explicitly in the next research-design draft before a main study.

The random baseline tests one specific guessing policy. Failure to reject it is
not proof of equivalence to random. A classifier fitted to this small pilot does
not establish a stable relationship with human difficulty. Test results from only
12 puzzles are particularly uncertain; higher accuracy may reflect class imbalance.

## Project organization and reproduction

The active workflow is four numbered notebooks in `notebooks/`. Experiment inputs
are in `experiments/first_move_v1/`. Raw and derived data remain under `data/`, and
figures under `figures/first_move_v1/`. Start with notebook 04 to read results; run
notebook 03 only to resume or reproduce collection. Its manifest rejects changes
to source cells, sample, prompt, settings, archive or model digests.

All former `.py` scripts and legacy notebooks are archived instead of being silently
discarded. `archive/README.md` explains byte-exact restoration of their original
paths in a separate project copy. The unused template linear-regression R file
is removed from the active workflow and retained only in that historical snapshot.
Temporary notebook-builder scripts are removed after generation. No Git commit or
push is performed automatically. Existing Git ignore rules exclude raw data, so
back up `data/experiments/first_move_v1/` and derived outputs separately.
