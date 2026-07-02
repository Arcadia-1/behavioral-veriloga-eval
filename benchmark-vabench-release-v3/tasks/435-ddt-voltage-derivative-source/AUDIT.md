# Audit: Ddt Voltage Derivative Source

- Task id: `v3_435_ddt_voltage_derivative_source`
- Category: `veriloga_dynamic_operator_semantics`
- Required syntax focus: `Use ddt() to form a voltage-domain derivative source.`
- EVAS status: `pending EVAS issue #44: https://github.com/Arcadia-1/EVAS/issues/44: https://github.com/Arcadia-1/EVAS/issues/44`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: executable behavioral-continuous-time candidate staged; behavior certification is blocked by continuous-time operator support.

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: staged_dynamic_solver_boundary operator=ddt out_range=8.653e+05 metric_range=8.653e+05 expected=certified_continuous_time_response
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/44.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 435 --end 494 --tasks 435,436,437,438,439,440,441,442,443,444,469,470,471,472,491,492,493,494 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_issue_435_494.json`
- Issue-level acceptance: After EVAS support lands, promote the listed 18 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 18/18 gold PASS, 90/90 negative variants rejected, and zero expectation_fail in the verification report.
