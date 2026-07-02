# Audit: Continuous Laplace Nd Filter

- Task id: `v3_493_continuous_laplace_nd_filter`
- Category: `veriloga_continuous_time_semantics`
- Required syntax focus: `Use laplace_nd() as a continuous-time behavioral transfer function.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavioral-continuous-time-candidate`
- EVAS status: `behavior-certified with first-order laplace_nd support`
- Boundary: voltage-domain behavioral low-pass certification only; KCL/current solving is outside this task.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Repository checker: `check_v3_493_continuous_laplace_nd_filter`.
- Checker behavior: verifies the `{1.0}/{1.0,1e-6}` first-order low-pass rise and hidden falling-step decay shape, rejecting zero, gain, input-bias, offset, and scale variants.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 493 --end 493 --tasks 493 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_493.json`
- Per-task result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
- Boundary: does not claim full Laplace operator coverage, KCL/MNA coupling, or simulator timestep-control equivalence.
