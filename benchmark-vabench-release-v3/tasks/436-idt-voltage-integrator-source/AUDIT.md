# Audit: Idt Voltage Integrator Source

- Task id: `v3_436_idt_voltage_integrator_source`
- Category: `veriloga_dynamic_operator_semantics`
- Required syntax focus: `Use idt() to form a voltage-domain integrator source.`
- EVAS status: `behavior-certified with event-sampled idt trapezoidal support`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: promoted to behavior-certified extension; certification covers this task's event-sampled voltage-domain `idt(V(vin))` behavior and does not claim conservative-current/KCL support.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Probe status: `PASS`.
- Behavior checker: repository checker interpolates `clk` rising crossings, verifies the first `idt` event initializes to zero, and verifies the second event output equals the trapezoidal integral `0.5*(vin1+vin2)*(t2-t1)` within tolerance.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 436 --end 436 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_436_after_checker.json`
- Result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
