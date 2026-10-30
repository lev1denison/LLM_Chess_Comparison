# My study figures

I keep two clearly separate early checkpoints:

- `one_move_v1/early/`: original strict-scoring 100-puzzle results for GPT-OSS and Gemini, including descriptive single CART trees. I preserve these historical figures unchanged.
- `one_move_v1/early_results_400/`: current tolerant-scoring results for the same first 400 puzzles across GPT-OSS, Gemini and Claude. Notebook 05b creates accuracy, adjusted logistic-regression curves with observed dots, and XGBoost training-gain feature importance.

My 400-puzzle checkpoint uses 1,200 answers and only original training puzzles. I use five-fold cross-validation within these 400 cases for exploratory XGBoost prediction metrics. I do not use the final 200 test puzzles. A feature-importance chart summarizes the boosted ensemble; I do not label a single CART as XGBoost.

Final notebook 06 remains a separate, pending workflow requiring complete collection and a three-model implementation update. No final test evaluation has been performed. I have not replaced historical figures with the new checkpoint.
