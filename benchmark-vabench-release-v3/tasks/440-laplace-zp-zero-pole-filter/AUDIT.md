# Audit: Laplace Zp Zero Pole Filter

- Task id: `v3_440_laplace_zp_zero_pole_filter`
- Category: `veriloga_laplace_filter_semantics`
- Required syntax focus: `Use laplace_zp() for zero/pole transfer modeling.`
- EVAS status: `behavior-certified with first-order laplace_zp support in EVAS commit a50b507`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: behavior-certified extension task with event-sampled first-order zero/pole response checking.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Repository checker: `check_v3_440_laplace_zp_zero_pole_filter`.
- Checker behavior: verifies the initial clock sample initializes the filter state, the second clock sample matches the first-real-pole exponential update, and `out`/`metric` track the same value.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 440 --end 440 --tasks 440 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_440.json`
- Per-task result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
- Boundary: validates only the first-order `laplace_zp(V(x), {z0}, {p0,...})` behavioral form used by this task; high-order, complex-zero/pole, Z-domain, and KCL/MNA forms remain outside this certification.
