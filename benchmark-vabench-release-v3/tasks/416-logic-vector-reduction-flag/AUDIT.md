# Audit: Logic Vector Reduction Flag

- Task id: `v3_416_logic_vector_reduction_flag`
- Category: `verilogams_digital_mixed_semantics`
- Required syntax focus: `Use logic vector reduction in a continuous assignment.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: behavior-certified AMS/digital mixed-signal extension task.
- Former EVAS tracking: https://github.com/Arcadia-1/EVAS/issues/43

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_416_after_msb_only_vector.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 416 --end 416 --tasks 416 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_416_after_msb_only_vector.json`
- Acceptance basis: hidden stimulus now covers endpoint single-bit vector reductions, so implementations that omit one bit from `|code` are rejected by the behavior checker.
