# Audit: Continuous Laplace Nd Filter

- Task id: `v3_493_continuous_laplace_nd_filter`
- Category: `veriloga_continuous_time_semantics`
- Required syntax focus: `Use laplace_nd() as a continuous-time behavioral transfer function.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavioral-continuous-time-candidate`
- EVAS status: `continuous-time smoke tests staged; behavior certification requires EVAS continuous-time operator support tracked by issue #44`
- Blocking issue: `https://github.com/Arcadia-1/EVAS/issues/44`

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: staged_dynamic_solver_boundary operator=continuous_laplace_nd out_range=1 expected=certified_continuous_time_response
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/44.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 493 --end 493 --tasks 493 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_493.json`
- Per-task acceptance: Promote `493-continuous-laplace-nd-filter` only after adding repository sim_correct evidence, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the per-task report.
- Issue-level acceptance: After EVAS support lands, promote the listed 18 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 18/18 gold PASS, 90/90 negative variants rejected, and zero expectation_fail in the verification report.
