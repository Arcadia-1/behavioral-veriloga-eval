# Audit: Table Model String Param Source

- Task id: `v3_488_table_model_string_param_source`
- Category: `veriloga_table_model_semantics`
- Required syntax focus: `Use a string parameter as the $table_model() data source.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavior-certified-extension`
- EVAS status: `gold and five negative variants pass the staged promotion gate after EVAS $table_model filename/control-argument support`
- Former blocking issue: `https://github.com/Arcadia-1/EVAS/issues/40`

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_488_after_table_model_string_param.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 488 --end 488 --tasks 488 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_488_after_table_model_string_param.json`
- Acceptance basis: EVAS reads the 1D table filename from the string parameter argument in `$table_model(V(in), tmdata, "1L")`; the trailing control string no longer masks the table data source.
