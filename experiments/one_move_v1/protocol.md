# My revised study protocol

I study **assisted one-move chess-puzzle accuracy**: whether the model chooses the official solution move when exactly one solver move is required. I supply FEN, a piece list and all legal moves in alphabetical order, without strength rankings. I do not measure unaided move generation, multi-step solving, causal effects or human first-move accuracy.

I freeze 1,000 fresh positions for both GPT-OSS 120B and Gemini 3.5 Flash-Lite. I exclude all earlier sampled/reserved IDs and solver positions, including the stopped mixed-length bulk study. I allocate 334/333/333 puzzles to the existing low/middle/high rating bands, then freeze 800 training and 200 held-out cases. My first 100 training puzzles are the pilot and remain part of the final study if the protocol does not change.

I record rating, legal moves, piece count, solver-relative material balance, tactical tags, phase, side, FEN, official move and source metadata. Themes are multi-label; my candidate themes and feature-frequency rules are fixed in `analysis_plan.json`. Phase labels use the existing dataset tags, with missing/ambiguous phases labeled unknown. I freeze encoding from training puzzle characteristics before responses. A solution-length predictor is inappropriate because it is constant.

My fuller final regression pools both deployments, includes model identity, and clusters standard errors by puzzle. My smaller early regression includes rating and numeric board characteristics plus identity; the 100-case pilot is too small to promise reliable coefficients for many theme categories. A descriptive early tree accompanies it where supported. My final tree uses the fixed training split and is evaluated once on held-out puzzles. The JSON analysis plan defines all thresholds and settings.

I made this revision after inspecting earlier exploratory results. My local full-solution pilot yielded no complete solutions, and the assisted local first-move pilot yielded few successes. Hosted pilots provided enough successes and failures to study associations. These historical pilots used different samples/prompts and are practical feasibility evidence, not a controlled model ranking or results of this revised study. `background_evidence.csv` contains counts and source hashes.

I stop preparation before any new API request. I retain old raw logs under ignored `data/` for evidence, exclusions and quota accounting; they are never pooled into this new analysis. My original PDFs remain unchanged. The new protocol supersedes their outcome, model list, sample size and predictive-tree implementation details; a shallow CART is not XGBoost.

My frozen sample contains 979 mate-in-one-tagged puzzles out of 1,000. That is a limitation of this one-move sample; I do not generalize the results to multi-step puzzles or broad strategic play. Rare tactical themes remain descriptive. I selected theme encoding from training puzzle characteristics before any new responses.
