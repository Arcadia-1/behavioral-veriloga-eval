# Audit: Always Async Reset Counter

- Task id: `v3_417_always_async_reset_counter`
- Category: `verilogams_digital_mixed_semantics`
- Required syntax focus: `Use an always block with asynchronous reset sensitivity.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: executable AMS/digital mixed-signal candidate pending full behavioral certification.
- EVAS tracking: https://github.com/Arcadia-1/EVAS/issues/39

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: q@100ns=-1.0000 expected=1.0000 tol=0.0800
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/39.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 417 --end 417 --tasks 417 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_417.json`
- Per-task acceptance: Promote `417-always-async-reset-counter` only after adding repository sim_correct evidence, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the per-task report.
- Issue-level acceptance: After EVAS support lands, promote the listed 2 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 2/2 gold PASS, 10/10 negative variants rejected, and zero expectation_fail in the verification report.
