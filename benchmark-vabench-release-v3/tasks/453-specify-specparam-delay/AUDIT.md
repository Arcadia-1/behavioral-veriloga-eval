# Audit: Specify Specparam Delay

- Task id: `v3_453_specify_specparam_delay`
- Category: `verilogams_specify_semantics`
- Required syntax focus: `Use specify/specparam delay syntax.`
- EVAS status: `gold and five negative variants pass after simple specify/specparam path-delay support`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: behavior-certified AMS/digital specify/specparam path-delay extension task.

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_453_after_specify_delay.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 453 --end 453 --tasks 453 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_453_after_specify_delay.json`
- Acceptance basis: EVAS parses `specparam tpd = 1n` and `(a => y) = tpd`, schedules delayed output breakpoints, and the repository checker measures y threshold crossings about 1 ns after a while rejecting 0 ns and 2 ns variants.
