# Audit: Zi Nd Discrete Filter

- Task id: `v3_441_zi_nd_discrete_filter`
- Category: `veriloga_z_domain_filter_semantics`
- Required syntax focus: `Use zi_nd() for discrete-time numerator/denominator filtering.`
- EVAS status: `behavior-certified with first-order zi_nd support in EVAS commit 159fb92`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: behavior-certified extension task with sampled-data first-order difference-equation checking.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Repository checker: `check_v3_441_zi_nd_discrete_filter`.
- Checker behavior: verifies the first clock sample initializes the sampled-data state and the second sample follows the `{1.0}/{1.0,1.0}` difference equation `y[n] = x[n] - y[n-1]`, with `out` and `metric` tracking the same value.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 441 --end 441 --tasks 441 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_441.json`
- Per-task result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
- Boundary: validates only the first-order `zi_nd(V(x), {1.0}, {1.0,1.0}, 1n)` behavioral form used by this task; full Z-domain, multirate, and KCL/MNA behavior remain outside this certification.
