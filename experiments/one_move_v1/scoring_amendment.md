# Tolerant solution-move scoring amendment

I changed scoring at the user's explicit request after inspecting the strict results. I now count the official move if it appears as a standalone, board-resolvable move in the visible response, regardless of surrounding wording, Markdown or code formatting. I apply the identical rule to GPT-OSS 120B, Gemini 3.5 Flash-Lite and Claude Haiku 5.5, both retrospectively and for future evaluation answers.

I accept UCI (including uppercase coordinates and hyphen-separated squares) and standard algebraic notation, including castling and promotions. I resolve SAN on the supplied solver board. I require token boundaries so an arbitrary substring inside a longer word is not a move. I do not search hidden reasoning, tool arguments, prompts or the supplied legal-move list; I inspect only the visible returned answer text. A correct visible move counts even if termination was truncated. An absent answer or a response without the correct move remains incorrect.

I follow the requested any-mention definition: if the official move appears among alternatives, inside a quotation, or in a negation, I still count it. This is solution-move mention success, and does not guarantee the model uniquely selected that move. I record the distinct board-legal moves found and flag responses containing multiple moves. None of the currently saved research answers has multiple board-legal move mentions under this extractor.

I made this amendment post hoc after results were inspected, including the completed Gemini collection. I did not use test answers to fit a model, search hyperparameters or choose parsing expressions. I tested parsing on constructed boards and responses. I disclose the timing rather than describe this scoring rule as originally preregistered. The outcome/scoring paragraphs in this amendment supersede the original strict formatting rules; I leave the original plans and PDFs intact.

I preserved raw request and outcome logs unchanged. Their historical `success` fields retain the score assigned at collection time. Current `results.csv` files are derived views containing both `strict_success` and tolerant `success`, scoring version, failure category and recognized moves. I independently verify each historical outcome against the scorer in effect when it was recorded before generating the amended view. Future outcome rows identify their scoring version. I preserved strict result tables and audits in ignored `data/experiments/one_move_v1/strict_scoring_checkpoint/`.

I added offline rescoring and cost-report cells to notebook 04. Rescoring does not connect to a provider and makes no API calls. I verify the same fixed puzzle IDs, 800/200 split and model response IDs; no answers are regenerated or replaced. Claude stays at 100 training puzzles, with zero test answers and bulk blocked. Existing strict pilot regression/tree figures remain historical strict results; I have not refitted them or trained a final XGBoost model under this amendment. Notebook 06 now requires audits with this scoring revision before it can fit.

## Updated saved-answer scores

| Model | Saved answers | Strict correct | Tolerant correct |
| --- | ---: | ---: | ---: |
| GPT-OSS 120B | 402 | 162 | 164 |
| Gemini 3.5 Flash-Lite | 1,000 | 545 | 557 |
| Claude Haiku 5.5 | 100 | 28 | 46 |

On the same 100 training pilot puzzles, tolerant scores are GPT-OSS 35/100, Gemini 54/100 and Claude 46/100. The different overall sample sizes above are not a matched model ranking. Claude's measured API cost is unchanged: approximately $0.0589 including capability checks, with another 900 projected at $0.52 if the pilot token average persists.

The machine-readable policy is `scoring_amendment.json`. I save the scored summary and audits in `data/experiments/one_move_v1/` and keep the credential files ignored. I have not committed or pushed this amendment.
