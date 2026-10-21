# Local Ollama pilot protocol

The researcher selected three locally hosted models instead of the API-backed
model originally listed in the research design: Qwen 3 8B, Llama 3.1 8B, and Gemma
3 4B. Ollama model tags are `qwen3:8b`, `llama3.1:8b`, and `gemma3:4b`.
All are the installed Q4_K_M distributions; exact digests and model details are
saved in `data/experiments/local_pilot_v2/manifest.json`. This is a comparison of
these deployments, not an isolated comparison of model family or parameter count.

The existing stratified sample contains 75 puzzles, 25 from each human-rating
stratum. All models receive all puzzles. A predetermined five-puzzle subset
(two low, two middle, one high) checks the runner. Its results are retained in
the pilot because no prompt, parsing, or scoring changes followed inspection.

Each solver turn is an independent request containing the current FEN and side
to move, with the shared prompt in `code/chess_prompt_v1.txt`. There is no prior
puzzle context, no legal-move list, no engine, and no official solution metadata
in the input. Generation settings are temperature 0, seed 401, context 4096,
and at most 128 generated tokens. Qwen thinking is explicitly disabled. The
settings favor a reproducible direct-answer protocol and do not measure maximum
reasoning performance. Deterministic settings do not guarantee bitwise-identical
outputs across platforms or software versions.

Responses must be one lowercase UCI move after trimming surrounding whitespace.
Other notations and explanations are unparseable. A legal move must match the
next official solver move exactly. Correct solver moves are followed by the
official opponent move and a new request. Full success requires every required
solver move. Legal alternative solutions are not engine-adjudicated. Generation
budget exhaustion is a protocol failure. HTTP/network/provider failures are
logged separately, retried once, and left unscored if both requests fail.

Raw request/response logs are saved after each call; outcomes are saved after
each puzzle. Resume skips completed puzzle-model pairs under the same frozen
manifest. Changing a model digest, prompt, sample, or settings requires a new
experiment directory. The outcome audit reconstructs model inputs and replays
the score for each recorded attempt.

The analysis first reports full-line solve rates and failure categories.
Classifier training requires both success and failure observations. Where
available, a fixed 80/20 puzzle-level holdout is shared by L2 logistic regression,
a depth-3 decision tree, and a majority baseline. Numeric preprocessing is fit
only on training data. Puzzle-clustered statistical inference is separate and
is deferred with sparse or separated outcomes. The planned main-study XGBoost
analysis is not replaced by the preliminary single tree.

If outcomes lack variation, this pilot remains a documented protocol result.
Any subsequent board representation, legal-move assistance, or reasoning-budget
experiment must be separately versioned and evaluated as a different condition;
scores must not be retrospectively relabeled to enable modeling.
