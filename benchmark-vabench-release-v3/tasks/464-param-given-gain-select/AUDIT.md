# Audit: Param Given Gain Select

- Task id: `v3_464_param_given_gain_select`
- Category: `veriloga_environment_function_semantics`
- Required syntax focus: `Use $param_given() to choose behavior based on parameter override presence.`
- EVAS status: `pending EVAS instance parameter override semantics; see https://github.com/Arcadia-1/EVAS/issues/49`

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: out_ovr@12ns=0.6000 expected=0.3000 metric_ovr@12ns=0.0000 expected=1.0000 out_ovr@52ns=0.3000 expected=0.1500 metric_ovr@52ns=0.0000 expected=1.0000
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/49.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 464 --end 464 --tasks 464 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_464.json`
- Per-task acceptance: Promote `464-param-given-gain-select` only after adding repository sim_correct evidence, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the per-task report.
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
