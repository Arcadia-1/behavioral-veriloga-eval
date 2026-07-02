# Audit: Table Model 2d Array Surface

- Task id: `v3_487_table_model_2d_array_surface`
- Category: `veriloga_table_model_semantics`
- Required syntax focus: `Use two independent arrays and one output array in a 2D $table_model().`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavior-certified-extension`
- EVAS status: `gold and five negative variants pass the staged promotion gate after 2D array-backed $table_model support`
- Former blocking issue: `https://github.com/Arcadia-1/EVAS/issues/56`

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_487_after_table_model_2d.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 487 --end 487 --tasks 487 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_487_after_table_model_2d.json`
- Acceptance basis: EVAS evaluates the four-corner 2D array table surface, and `neg_003_reset_bias` now perturbs `z[0]` so the zero-corner bias error is checker-visible.
