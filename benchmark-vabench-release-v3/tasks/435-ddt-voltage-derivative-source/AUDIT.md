# Audit: Ddt Voltage Derivative Source

- Task id: `v3_435_ddt_voltage_derivative_source`
- Category: `veriloga_dynamic_operator_semantics`
- Required syntax focus: `Use ddt() to form a voltage-domain derivative source.`
- EVAS status: `behavior-certified with event-sampled ddt finite-difference support`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: promoted to behavior-certified extension; certification covers this task's event-sampled voltage-domain `ddt(V(vin))` behavior and does not claim conservative-current/KCL support.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Probe status: `PASS`.
- Behavior checker: repository checker interpolates `clk` rising crossings, verifies the first `ddt` event initializes to zero, and verifies the second event output equals `(vin2-vin1)/(t2-t1)` within tolerance.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 435 --end 435 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_435_after_checker.json`
- Result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
