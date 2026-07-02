# Audit: Zi Zd Discrete Filter

- Task id: `v3_443_zi_zd_discrete_filter`
- Category: `veriloga_z_domain_filter_semantics`
- Required syntax focus: `Use zi_zd() for discrete-time zero/denominator filtering.`
- EVAS status: `behavior-certified with first-order zi_zd support in EVAS commit 7bc6fdd`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: behavior-certified extension task with sampled-data first-order difference-equation checking.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Repository checker: `check_v3_443_zi_zd_discrete_filter`.
- Checker behavior: verifies the first clock sample initializes the sampled-data state and the second sample follows the `{1.0}/{1.0,1.0}` difference equation `y[n] = x[n] - y[n-1]`, with hidden stimulus distinguishing stateful behavior from passthrough behavior.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 443 --end 443 --tasks 443 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_443.json`
- Per-task result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
- Boundary: validates only the first-order `zi_zd(V(x), {1.0}, {1.0,1.0}, 1n)` behavioral form used by this task; full zero/denominator, multirate, and KCL/MNA behavior remain outside this certification.
