# Audit: Laplace Nd Lowpass Filter

- Task id: `v3_437_laplace_nd_lowpass_filter`
- Category: `veriloga_laplace_filter_semantics`
- Required syntax focus: `Use laplace_nd() for continuous-time transfer modeling.`
- EVAS status: `behavior-certified with first-order laplace_nd support in b2d3609`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: promoted to behavior-certified extension; certification covers this task's event-sampled first-order `laplace_nd(V(vin), {1.0}, {1.0, 1.0})` behavior and does not claim high-order Laplace, Z-domain, or conservative-current/KCL support.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Probe status: `PASS`.
- Behavior checker: repository checker interpolates `clk` rising crossings, verifies the first sample initializes the low-pass state to `vin`, and verifies the second sample follows `y2 = y1 + (1-exp(-dt/tau))*(vin2-y1)` for the task's `tau=1.0`.
- EVAS evidence: `b2d3609 Support first-order laplace_nd behavior`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 437 --end 437 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_437_after_checker.json`
- Result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
