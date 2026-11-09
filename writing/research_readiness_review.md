# Research readiness review

Review date: November 5, 2026

**Verdict: ready to draft a DA401 final research paper, with specific measurement and reproducibility issues to resolve before submission.** The completed data support a focused observational study of human-rated difficulty and assisted one-move performance. They do not establish broad chess reasoning ability, direct human-versus-model disagreement, or a general model ranking. The existing final report is a substantial draft foundation. Course-specific completeness still depends on the instructor's rubric.

## Scope of this review

Read the original proposal, revised research design and literature review; notebook narratives and relevant preparation, collection, scoring and final-analysis code; protocol and amendments; historical evidence table; final report and tables; and saved response logs and analysis artifacts. Inspected Git history/status and the final regression figure. Performed offline checks described below without calling model providers, changing existing analyses, or executing collection notebooks. This was not a fresh validation of all six million source records, an independent authentication of provider records, or a comprehensive literature/citation audit.

## Development from the proposal to the completed study

The proposal initially envisioned approximately 10,000+ puzzles and emphasized human–LLM difficulty disagreement, including multi-step puzzles. The revised research design reduced the intended sample to approximately 1,500–2,000, retained multi-step solving, and specified pooled logistic regression with puzzle-clustered standard errors plus XGBoost prediction. The completed study instead uses 1,000 shared one-move positions and three hosted deployments.

The historical evidence table records 0/225 complete solutions in the local pilot, 6/144 correct assisted local first moves, and later hosted feasibility results of 21/60 and 32/60. These explain why the task changed. Samples and prompts differed, so the stages cannot establish a controlled improvement or local-versus-hosted performance difference.

The frozen one-move study progressed through a 100-puzzle pilot, a 400-training-puzzle exploratory checkpoint, and 3,000 completed answers. Claude, tolerant scoring and the final three-model plan were added through disclosed amendments. This is a legitimate exploratory development history, but it should not be described as an unchanged preregistered experiment. The existing final report handles much of this distinction well.

Primary local sources: `writing/Victor_Le_Proposal401.pdf`, `writing/Victor_Le_ResearchDesignRevised.pdf`, `writing/Victor_Le_LiteratureReview_DA401-1.pdf`, `experiments/one_move_v1/protocol.md`, and the adjacent amendment files.

## Findings independently checked

- All 19 files listed in `data/analysis/one_move_v1/final/final_data_audit.json` match their saved hashes. Hash consistency verifies preservation relative to those records, not historical authenticity by itself.
- The sample contains 1,000 unique puzzle IDs with an 800/200 split. Reconstructing every solver board after the initiating move reproduced FEN, legal-move count, piece count and solver-relative material balance without discrepancies.
- Replaying the scoring functions on the raw responses reproduced both saved binary scores for 2,999 answers. One GPT-OSS answer triggers a scorer exception, described below; its saved failure label is substantively reasonable.
- Independently fitting the specified pooled logistic regression reproduced the saved coefficients to floating-point precision. The rating odds ratio is 0.564455 per 500 points, with clustered 95% CI 0.510749–0.623809 and p=3.608e-29.
- An additional exploratory check using strict outcomes gives a rating odds ratio of 0.589590, CI 0.532267–0.653087, p=4.327e-24. Thus, the central negative rating association persists under both existing scoring definitions. This review-time sensitivity check is not part of the original final plan.
- Recomputed held-out accuracy, balanced accuracy, AUC and Brier scores from cached predictions; they agree with the report. Test IDs and labels match the frozen inputs and do not overlap training IDs. This check did not retrain XGBoost or rerun the full notebook.

| Deployment | Strict success | Official-move mention success | Held-out XGBoost accuracy | Majority baseline |
| --- | ---: | ---: | ---: | ---: |
| GPT-OSS 120B | 41.8% | 42.1% | 58.0% | 60.5% |
| Gemini 3.5 Flash-Lite | 54.5% | 55.7% | 70.0% | 56.0% |
| Claude Haiku 5.5 | 28.6% | 49.0% | 54.5% | 51.0% |

These findings make sense together: a clear average association with rating can coexist with weak prediction of individual answers. The GPT-OSS and Claude predictive results should remain modest secondary findings. There is no requirement that every model or predictor perform well for this to be a worthwhile research paper.

## Measurement issues to address

**1. Separate formatting compliance, move recommendation and move mention.** Of Claude's 204 newly credited responses, 182 become strictly correct simply by removing surrounding `**` bold markers. This explains most of the increase and argues against interpreting strict scores as pure chess ability. The remaining cases and a sample of unchanged successes/failures should receive a documented manual review. Freeze a review rubric before coding; if possible, have another reviewer independently check ambiguous cases.

The current any-mention definition can credit alternatives, quotations or negation. The extractor can also interpret a square mentioned in prose as a legal pawn move. The five flagged multiple-move responses are not all genuine lists of competing recommendations. For example, some explanatory text names squares that the extractor resolves as moves. Do not equate that flag with five intentionally ambiguous answers. Preserve existing outcomes and report any narrower recommendation-based scoring as a separately labeled sensitivity analysis.

**2. Official-answer matching differs from chess correctness.** Exhaustive legal-move checks found 37 sampled positions with multiple immediate mating moves. Six GPT-OSS, five Gemini and nine Claude failures contain an alternative legal checkmating move. For example, GPT-OSS answers `d7d8` on puzzle `1Bxs2`, while the official answer is `c7c8`; both mate immediately.

If the existing mention policy were extended to accept these alternative mating moves, rates would be 42.7%, 56.2% and 49.9%, respectively. The ordering remains unchanged. These are diagnostic sensitivity counts, not replacement primary results; they do not validate alternative nonmating solutions. Either retain explicit official-reference matching as the outcome and disclose its limitation, or add a carefully documented chess-correctness sensitivity analysis.

**3. Narrow the scope of the claim.** There are 979 mate-in-one tags; independent board checks find an immediate mating move in 986 positions. Tags and actual board properties are distinct. This is overwhelmingly a short mating-task study. Human ratings serve as a proxy for difficulty, with no matched human participants tested under the assisted prompt. One answer per deployment per puzzle also cannot estimate each puzzle's stable model success probability.

## What the analysis does and does not establish

The strongest result is the negative adjusted association between human rating and success. The positive hanging-piece association is a useful secondary finding; kingside attack is weaker and should remain exploratory given multiple secondary coefficients. An interval crossing one does not establish absence of a relationship.

The current report does not directly establish that the full feature set improves prediction **beyond rating alone**. XGBoost gain importance and beating a constant majority classifier do not answer that question. Before making this claim, specify a rating-only benchmark and compare it with the fuller model using identical training partitions and predictions. Since the final holdout has already been inspected, label subsequent comparisons exploratory and avoid repeatedly tuning to that holdout. Training-only cross-validation can support a transparent supplemental comparison; a future fresh holdout would provide stronger confirmation.

As an additional descriptive check, training-prevalence probability baselines have test Brier scores of 0.2400, 0.2464 and 0.2499 for GPT-OSS, Gemini and Claude. The reported XGBoost values are 0.2424, 0.2142 and 0.2475. This reinforces that Gemini provides the clearest predictive result, while GPT-OSS does not improve even on this simple probability baseline.

Model comparisons involve the same puzzles. If making significance claims about raw differences, use paired inference, such as a puzzle-level bootstrap or an appropriate paired binary test; do not infer paired significance from separate Wilson intervals. The current clustered regression already accounts for repeated observations by puzzle for its specified adjusted contrasts.

Rating reliability also merits reporting: 57 puzzles have fewer than 30 plays and 64 have rating deviation above 150. These are descriptive thresholds used in this review, not proposed automatic exclusions. Consider a disclosed sensitivity check if rating quality is central; do not selectively filter until results improve.

## Reproducibility issues

The strict scorer calls `chess.Move.from_uci` without catching an invalid same-square move. GPT-OSS puzzle `7wsdj` has raw answer `f8f8`; the saved result calls it `illegal_move`, but the current scorer raises `InvalidMoveError`. `audit_model` calls this scorer directly. Fix the exception handling through a documented code amendment and replay the raw scoring audit. No answer regeneration is needed. This does not establish that the reported success total is wrong; it establishes that the current raw-scoring replay is not complete.

Notebooks 03 and 04 compare a constructed manifest against the original manifest, including the code hash of notebook 06. The current final notebook has a different hash, as expected from its documented extension, but those older setup paths do not apply the separate final binding before asserting equality. A fresh run of those cells would stop. Preserve the historical manifest and make the supported offline replay path explicit; do not silently replace historical hashes. Notebook 06 has its own amended binding logic.

`experiments/stage_index.json` still reports an unfinished 400-case stage and 402 GPT-OSS answers. Some collection notebook prose also describes earlier states. Label historical snapshots clearly and update the current navigation/status separately. Git status shows final report/code/figures that are modified or untracked. The frozen data are ignored by Git, so a clone alone cannot reproduce the final results. Prepare a versioned, credential-free analysis bundle with the frozen sample, scored responses, environment, code and provenance before handoff.

## Recommended paper framing and remaining writing

Suggested title: **Human-Rated Difficulty and LLM Performance on Assisted One-Move Chess Puzzles**.

Suggested central conclusion: “In a rating-balanced sample dominated by immediate mating tasks, higher human-rated difficulty was associated with lower official-solution-move mention success across three hosted LLM deployments. Predictive performance varied by deployment, and measured comparisons depended on response scoring.”

Use the existing `writing/final_report.md` as the methods/results foundation. Add an integrated introduction and related-work section, explicit research questions, a short study-development timeline, sampling eligibility and rating-quality details, actual collection dates and deployment settings, representative scoring examples, and a complete bibliography. Keep the early feasibility studies in a brief methods rationale or appendix rather than pooling them with final results.

The original literature review needs reframing around the completed one-move assisted task. Two cited benchmarks were spot-checked against their primary records: [LLM CHESS](https://arxiv.org/abs/2512.01992) and [ChessQA](https://arxiv.org/abs/2510.23948). They study broader or different aspects of chess behavior, so comparisons require explicit task distinctions. Verify the remaining references and claim-level support before submission. The [Lichess database documentation](https://database.lichess.org/#puzzles) is the primary source for the dataset format and provenance.

**Priorities:** begin drafting now; resolve scoring replay and explain measurement first; add a rating-only comparison if retaining an incremental-prediction claim; then finish references, methods detail and the reproducibility bundle. More API collection is not necessary merely to begin a credible final-paper draft. A stronger generalization or publication claim would require additional design and validation beyond this review.
