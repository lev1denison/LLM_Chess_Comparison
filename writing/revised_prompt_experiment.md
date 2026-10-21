# Revised prompt experiment: board_prompt_v1

## What changed

The original FEN-only experiment, its prompt, configuration, raw data, notebook,
and figures were preserved. SHA-256 fingerprints in the new experiment folder
verify that the protected checkpoint files remain unchanged.

A separate experiment now tests FEN plus an explicit piece list with constrained
JSON/UCI output, and that same representation plus legal-move choices with output
constrained to those choices. This is a change in task assistance and response
format, not a direct replacement for the original scores.

## Design and execution

- Development: 12 puzzles (4 per rating stratum), selected deterministically from
  the original 75 before the revised model responses were observed.
- Sanity checks: side to move, any legal move, and a verified mate-in-one, each for
  White and Black. Fixtures are separate from research data.
- Direct generation: temperature 0, seed 401, 256 output tokens, 4096 context;
  Qwen thinking disabled.
- Thinking probe: Qwen only, one development puzzle per stratum, thinking enabled,
  2048 output tokens. This exploratory condition cannot select the shared protocol.
- Fresh evaluation: 75 preselected puzzles, excluding every original-pilot puzzle,
  using the original rating cutoffs and eligibility. These were reserved before
  development inference. A 60/15 puzzle train/test assignment was saved in advance.
- Readiness rule: all 36 condition attempts completed, at least 3 full solves
  across at least 2 distinct puzzles, and at least 90% format-and-legality rate.
  Choose the condition with more full solves; ties prefer the unassisted move set.
  These are operational thresholds, not a statistical power calculation.
- Every request/response is logged. Official solution sequences remain outside
  the prompt. Incorrect, illegal, unparseable, and budget-limited answers stop a
  puzzle; infrastructure errors remain unscored.

## Matched development results

| condition | llm_name | n | solved | solve_rate |
| --- | --- | --- | --- | --- |
| legal_choices_json | gemma3:4b | 12 | 0 | 0.0 |
| legal_choices_json | llama3.1:8b | 12 | 0 | 0.0 |
| legal_choices_json | qwen3:8b | 12 | 0 | 0.0 |
| original_fen_uci | gemma3:4b | 12 | 0 | 0.0 |
| original_fen_uci | llama3.1:8b | 12 | 0 | 0.0 |
| original_fen_uci | qwen3:8b | 12 | 0 | 0.0 |
| piece_list_json | gemma3:4b | 12 | 0 | 0.0 |
| piece_list_json | llama3.1:8b | 12 | 0 | 0.0 |
| piece_list_json | qwen3:8b | 12 | 0 | 0.0 |

## First-move diagnostic (post-hoc, descriptive only)

| condition | llm_name | n | first_moves_correct | full_solves |
| --- | --- | --- | --- | --- |
| legal_choices_json | gemma3:4b | 12 | 2 | 0 |
| legal_choices_json | llama3.1:8b | 12 | 1 | 0 |
| legal_choices_json | qwen3:8b | 12 | 2 | 0 |
| piece_list_json | gemma3:4b | 12 | 0 | 0 |
| piece_list_json | llama3.1:8b | 12 | 0 | 0 |
| piece_list_json | qwen3:8b | 12 | 1 | 0 |

This does not replace full-line scoring or affect selection. The random development
subset happened to contain only multi-step puzzles; this limits what a small
zero-full-success result can establish about single-move tactical selection.

## Sanity results

| condition | llm_name | n | passed |
| --- | --- | --- | --- |
| legal | gemma3:4b | 2 | 2 |
| legal | llama3.1:8b | 2 | 2 |
| legal | qwen3:8b | 2 | 1 |
| mate | gemma3:4b | 2 | 0 |
| mate | llama3.1:8b | 2 | 0 |
| mate | qwen3:8b | 2 | 0 |
| side | gemma3:4b | 2 | 1 |
| side | llama3.1:8b | 2 | 1 |
| side | qwen3:8b | 2 | 1 |

## Decision and modeling status

```json
{
  "selection": {
    "selected_condition": null,
    "development": {
      "piece_list_json": {
        "n": 36,
        "solves": 0,
        "distinct_solved_puzzles": 0,
        "format_and_legality_rate": 0.19444444444444445,
        "ready": false
      },
      "legal_choices_json": {
        "n": 36,
        "solves": 0,
        "distinct_solved_puzzles": 0,
        "format_and_legality_rate": 1.0,
        "ready": false
      }
    },
    "rule": {
      "eligible_conditions": [
        "piece_list_json",
        "legal_choices_json"
      ],
      "minimum_full_solves": 3,
      "minimum_distinct_solved_puzzles": 2,
      "minimum_format_and_legality_rate": 0.9,
      "require_all_36_attempts_completed": true,
      "ranking": "most full solves, then prefer piece_list_json on ties",
      "reasoning_probe": "Qwen only, one predetermined development puzzle per stratum; exploratory and ineligible for protocol selection"
    },
    "status": "No condition met readiness criteria; evaluation not run"
  },
  "total_recorded_outcomes": 93,
  "infrastructure_errors": 0,
  "model_status": "Not fitted to development data. Fresh evaluation requires a condition to meet the pre-specified readiness checks.",
  "notes": [
    "Development includes 12 known original-pilot puzzles and is exploratory.",
    "Fresh sample excludes all 75 original-pilot IDs; 60/15 puzzle split was saved before evaluation.",
    "JSON/UCI syntax is constrained in both revised conditions; legal choices condition additionally constrains legality.",
    "These are protocol bundles, not an isolated causal estimate of board representation.",
    "Thinking probe is Qwen-only, has a larger output budget, and is not eligible for protocol selection.",
    "No solution or engine evaluation enters model inputs. Exact official-line scoring may reject legal alternatives.",
    "The fixed random development subset contains only multi-step puzzles; mate-in-one fixtures are a separate sanity task.",
    "First-move correctness is reported post-hoc as a descriptive diagnostic only; it does not replace the primary full-solution outcome.",
    "Readiness checks do not establish statistical power or population representativeness."
  ],
  "first_alphabetical_choice_rates": {
    "gemma3:4b": 0.0,
    "llama3.1:8b": 0.07692307692307693,
    "qwen3:8b": 0.0
  },
  "audit": {
    "scored_outcomes_checked": 75,
    "sanity_outcomes_recorded": 18,
    "original_checkpoint_hashes_match": true,
    "status": "passed"
  },
  "sanity_audit": {
    "sanity_outcomes_verified": 18,
    "status": "passed"
  }
}
```

## Reproduce and inspect

Run the commands in `code/experiments/board_prompt_v1/README.md`. Open
`code/revised_prompt_experiment.ipynb` for executed tables and figures. Raw logs,
manifests, and reserved samples are in `data/experiments/board_prompt_v1/`; the
existing Git ignore policy excludes data, so retain a separate backup.

The main-study sample and XGBoost remain later stages. Do not merge development
outcomes into fresh evaluation or reinterpret assisted accuracy as unaided skill.
