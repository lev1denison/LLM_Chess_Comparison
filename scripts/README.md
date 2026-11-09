# Analysis utilities

Run commands from the repository root after installing dependencies with `python -m pip install -r requirements.txt`.

- `python scripts/build_final_report.py`: rebuild the report and CSV tables from local frozen artifacts.
- `python scripts/plot_accuracy.py` (and the other `plot_*.py` scripts): render saved analysis figures.
- `python scripts/verify_final_analysis.py`: replay the final notebook and verify frozen inputs and cached evaluation. Requires ignored local study data; writes notebook outputs and verification receipts.
- `prepare_final_revision.py`: historical one-time amendment utility, retained for provenance. Do not rerun against the completed study.

Notebook 06 adds `scripts/` to its import path in a setup cell tagged `run_control`. The existing hash convention excludes environment setup cells, preserving the analysis code hash and frozen study bindings.
