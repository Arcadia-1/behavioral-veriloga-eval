# Audit: Laplace Np Pole Filter

- Task id: `v3_438_laplace_np_pole_filter`
- Category: `veriloga_laplace_filter_semantics`
- Required syntax focus: `Use laplace_np() for pole-form continuous-time transfer modeling.`
- EVAS status: `behavior-certified with first-order laplace_np support in de978be`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: promoted to behavior-certified extension; certification covers this task's event-sampled first-real-pole `laplace_np(V(vin), {1.0}, {1.0, 1.0})` behavior and does not claim high-order, complex-pole, Z-domain, or conservative-current/KCL support.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Probe status: `PASS`.
- Behavior checker: repository checker interpolates `clk` rising crossings, verifies the first sample initializes the pole-filter state to `vin`, and verifies the second sample follows `y2 = y1 + (1-exp(-dt/tau))*(vin2-y1)` for the task's first real pole `tau=1.0`.
- EVAS evidence: `de978be Support first-order laplace_np behavior`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 438 --end 438 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_438_after_checker.json`
- Result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
