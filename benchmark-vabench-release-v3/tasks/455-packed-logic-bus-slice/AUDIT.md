# Audit: Packed Logic Bus Slice

- Task id: `v3_455_packed_logic_bus_slice`
- Category: `verilogams_vector_semantics`
- Required syntax focus: `Use a packed-style logic bus with slices and concatenation.`
- EVAS status: `pending EVAS issue #43: https://github.com/Arcadia-1/EVAS/issues/43: https://github.com/Arcadia-1/EVAS/issues/43`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: AMS/digital packed-bus candidate staged; behavior certification is blocked by digital vector port and continuous assign support.

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: y3@50ns=0.0000 expected_a7=1.0000 y1@50ns=0.0000 expected_a1=1.0000 y0@50ns=0.0000 expected_a0=1.0000 y3@90ns=0.0000 expected_a7=1.0000
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/43.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 455 --end 455 --tasks 455 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_455.json`
- Per-task acceptance: Promote `455-packed-logic-bus-slice` only after adding repository sim_correct evidence, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the per-task report.
- Issue-level acceptance: After EVAS support lands, promote the listed 4 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 4/4 gold PASS, 20/20 negative variants rejected, and zero expectation_fail in the verification report.
