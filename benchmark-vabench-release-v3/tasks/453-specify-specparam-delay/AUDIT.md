# Audit: Specify Specparam Delay

- Task id: `v3_453_specify_specparam_delay`
- Category: `verilogams_specify_semantics`
- Required syntax focus: `Use specify/specparam delay syntax.`
- EVAS status: `pending EVAS issue #48: https://github.com/Arcadia-1/EVAS/issues/48: https://github.com/Arcadia-1/EVAS/issues/48`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: specify/specparam timing candidate staged; behavior certification is blocked by timing block support.

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_DUT_COMPILE`.
- Current failure summary: simulator_error=Failed to compile Verilog-A file specify_specparam_delay.vams: Parse error at L4:5: Unsupported Verilog-AMS module block 'specify' is outside the EVAS behavioral subset
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/48.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 453 --end 453 --tasks 453 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_453.json`
- Per-task acceptance: Promote `453-specify-specparam-delay` only after adding repository sim_correct evidence, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the per-task report.
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
