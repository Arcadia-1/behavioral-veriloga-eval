# Audit: Generate Genvar Replicated Stage

- Task id: `v3_449_generate_genvar_replicated_stage`
- Category: `veriloga_generate_semantics`
- Required syntax focus: `Use generate/genvar to replicate a behavioral stage.`
- EVAS status: `gold and five negative variants pass after simple generate/genvar assignment subset support`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: behavior-certified AMS/wreal generate/genvar extension task.

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_449_after_generate_subset.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 449 --end 449 --tasks 449 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_449_after_generate_subset.json`
- Acceptance basis: EVAS accepts the simple generate-for named block used here, records `wreal stage[0:0]` as an internal array, propagates `a` through the generated stage to `y`, and rejects all five behavior-specific negative variants.
