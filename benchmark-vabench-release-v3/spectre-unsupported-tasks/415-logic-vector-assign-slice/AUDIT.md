# Audit: Logic Vector Assign Slice

- Task id: `v3_415_logic_vector_assign_slice`
- Category: `verilogams_digital_mixed_semantics`
- Required syntax focus: `Use logic vectors with continuous assign and slice selection.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: behavior-certified AMS/digital mixed-signal extension task.
- Former EVAS tracking: https://github.com/Arcadia-1/EVAS/issues/43

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_415_after_vector_port_order.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 415 --end 415 --tasks 415 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_415_after_vector_port_order.json`
- Acceptance basis: the harness now maps the packed vector port in high-to-low positional order, and hidden stimulus distinguishes `code[0]` from `code[1]` so wrong false-branch slices are rejected.
