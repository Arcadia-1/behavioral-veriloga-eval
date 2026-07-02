# Audit: Packed Logic Bus Slice

- Task id: `v3_455_packed_logic_bus_slice`
- Category: `verilogams_vector_semantics`
- Required syntax focus: `Use a packed-style logic bus with slices and concatenation.`
- EVAS status: `gold and five negative variants pass after bracketed bus instance parsing support`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: behavior-certified AMS/digital packed-bus extension task.

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_455_after_bracketed_bus.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 455 --end 455 --tasks 455 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_455_after_bracketed_bus.json`
- Acceptance basis: EVAS flattens bracketed bus groups in instance nodes, the output bus drives `y3:y0`, and adjacent-bit slice negative variants are rejected.
