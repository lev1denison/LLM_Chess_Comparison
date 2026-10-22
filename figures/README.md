# My new study figures

I keep my completed 100-puzzle-per-model pilot figures in `one_move_v1/early/`:
accuracy, adjusted logistic-regression curves and descriptive trees, generated
by notebook 05 from frozen audited training answers. GPT-OSS scored 35/100;
Gemini scored 53/100. I use puzzle-clustered uncertainty for the pooled core
regression. These are exploratory results, not held-out tree performance.

Notebook 06 creates final accuracy, regression and **XGBoost feature-importance**
figures only after complete audited collection. It does not present a single
CART as the final ensemble. The pilot CART figures above remain unchanged.
My 200 held-out puzzles remain unused. The frozen early checkpoint does not
change when collection resumes. Older study figures were removed at restart.
