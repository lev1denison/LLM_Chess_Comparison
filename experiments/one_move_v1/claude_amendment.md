> Subsequent scoring update: I adopted [tolerant scoring for every deployment](scoring_amendment.md) at the user's request. Claude's amended pilot is 46/100; the strict pilot described below remains preserved. No bulk run has started.

# Claude Haiku 5.5 pilot amendment

I add Anthropic Claude Haiku 5.5 as a third deployment to study how puzzle difficulty and board characteristics relate to assisted one-move success. I made this amendment after inspecting the existing pilot and collection progress; it is not an original preregistration. I retain GPT-OSS 120B and Gemini 3.5 Flash-Lite, rather than silently replacing either model. I have not added GPT-6 Luna.

I use the same frozen 1,000 puzzle IDs, board features, prompt, alphabetical complete legal-move lists, official-move scoring, collection order and 800/200 split. I send no ratings, theme/phase labels, official answers, tools, search or engine assistance. The sample remains predominantly mate-in-one tagged. I use the same first 100 training puzzles for the pilot; no Claude test puzzles are requested or evaluated.

I freeze `claude-haiku-5-5`, adaptive thinking, low effort and a 6,000-token output ceiling. I omit temperature, top-p and seed for compatibility. These provider-specific settings do not establish equal reasoning compute across models. I record returned model IDs and stop for review if they change. The exact settings and price reference are in `claude_pilot.json`.

I first run the existing eight capability checks (side to move, legal moves and simple mates), requiring both side checks, both legal checks and at least two mate checks, with all eight responses usable. I then collect the existing 20-puzzle operational prefix and verify that replay sends zero new generation requests before advancing to 100 training puzzles. Completed wrong answers are retained; infrastructure failures remain pending. Generation limits and invalid answers count as failures.

I authorize only this pilot. Notebook 04 selects Claude alone, and an explicit guard rejects Claude bulk mode. I stop after at most 100 research answers, plus eight capability checks and identical-request infrastructure retries. I report correctness, failure categories, raw token usage and estimated API charges before requesting approval for the remaining 900. I do not select models or tune prompts on held-out accuracy.

I calculate standard API cost from actual response usage: input $0.10/million and output (including billed thinking) $0.50/million for these short prompts. No batch or caching discounts are assumed. Invoice charges may differ through taxes, credits or provider adjustments. I project the remaining 900 from the observed pilot average and state the uncertainty.

My original two-model pilot figures, fitted objects, raw responses, PDFs, configuration and plans remain preserved. I save the previous collector and manifest plus protected-file hashes in the ignored amendment provenance record. The current manifest records the extended collector; old audit records remain tied to their original manifest. I do not refit the original early checkpoint.

If I approve Claude bulk collection, I must explicitly amend the final analysis implementation before using three-model results: add a second model indicator to the pooled regression with puzzle-clustered errors and a separate fixed XGBoost model using the same 800 training/200 test cases. Notebook 06 currently implements the original two-model final plan and must not be described as a completed three-model analysis.

Official references: [model and pricing](https://platform.claude.com/docs/en/models/haiku-5-5/overview), [Messages API](https://platform.claude.com/docs/en/api/messages/create), [effort](https://platform.claude.com/docs/en/build-with-claude/effort).

## Capability-format amendment before research collection

My initial eight Claude calls had five strict successes and three formatting failures: `White` instead of `white`, and two otherwise correct mate moves in outer Markdown bold. I retained every original raw answer and strict outcome. Before collecting any Claude research answers, I added a post-check, capability-only diagnostic that lowercases side labels and removes one outer pair of Markdown bold markers. I use its board-understanding gate to allow the pilot; this is a disclosed departure from the initial strict capability gate, not a claim that all eight original answers followed instructions. The 100 research answers retain the identical strict scorer used for GPT-OSS and Gemini: I do not strip Markdown or repair research answers. I do not regenerate capability calls. I record both strict and diagnostic gate results.

## Bulk authorization after tolerant pilot review

I explicitly approved Claude bulk collection after reviewing 46/100 tolerant accuracy and the approximately $0.52 estimate for the remaining 900. I preserve the 100-puzzle checkpoint and reuse all pilot answers. I freeze the same request bodies, adaptive thinking at low effort, 6,000 output-token ceiling, prompt, sample, split and tolerant scoring revision. Notebook 04 selects Claude alone in bulk mode with WAIT_FOR_QUOTA=False. I save every answer and pause at actual provider limits. I do not fit final models or tune on held-out answers during collection. This authorization supersedes the earlier pilot-only restriction; it does not authorize GPT-6 Luna or change the scoring rule.
