# Historical code checkpoint

`pre_first_move_code.zip` preserves every former `code/` source, prompt,
configuration, test and executed notebook, including prompt-development work.
`code_snapshot_hashes.json` lists the SHA-256 of each of its 22 entries.
Files inside the ZIP retain their original `code/...` paths and exact bytes.

Old raw data, derived tables, manifests and figures stay at their original paths:

- `data/experiments/local_pilot_v2/`: original FEN-only full-sequence pilot.
- `data/experiments/board_prompt_v1/`: revised prompts, sanity tests, thinking
  probe, and still-unused reserved evaluation sample.
- Corresponding `data/analysis/` and `figures/` folders remain unchanged.

The active workflow is in `notebooks/`. Historical Python runners were retired
from the working tree rather than rewritten in place. The unused template
`linear_regression.R` is also retained only in this archive.

## Restore a historical experiment

Use a separate copy of this project with its data and Python dependencies.
From that copy's repository root:

```powershell
Expand-Archive -LiteralPath archive/pre_first_move_code.zip -DestinationPath .
```

This restores the original `code/` layout and its READMEs. Follow the restored
instructions. Collection requires the exact model digests in the historical
manifest. Do not overwrite existing derived data without a backup.

Notebook 03 verifies archive integrity and all 23 originally protected checkpoint
files, reading archived bytes for relocated code and the retained data/figures
for the others. Archival does not change historical scores. Raw data is not in
the ZIP and remains Git-ignored; back it up separately.
