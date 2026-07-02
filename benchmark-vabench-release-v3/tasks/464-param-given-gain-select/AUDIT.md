# Audit: Param Given Gain Select

- Task id: `v3_464_param_given_gain_select`
- Category: `veriloga_environment_function_semantics`
- Required syntax focus: `Use $param_given() to choose behavior based on parameter override presence.`
- EVAS status: `gold and five negative variants pass the staged promotion gate after EVAS $param_given() instance metadata support`
- Former blocking issue: `https://github.com/Arcadia-1/EVAS/issues/49`

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_464_after_param_given.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 464 --end 464 --tasks 464 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_464_after_param_given.json`
- Acceptance basis: EVAS tracks explicit Spectre instance parameter names separately from default parameter values, so `$param_given(gain)` returns 0 for the default instance and 1 for the instance with `gain=0.5`.
