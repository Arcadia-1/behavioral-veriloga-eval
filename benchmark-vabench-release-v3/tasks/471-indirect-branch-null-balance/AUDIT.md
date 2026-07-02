# Audit: Indirect Branch Null Balance

- Task id: `v3_471_indirect_branch_null_balance`
- Category: `veriloga_indirect_branch_semantics`
- Required syntax focus: `Use an indirect branch assignment target/equation form.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavioral-continuous-time-candidate`
- EVAS status: `behavior-certified with narrow indirect branch voltage-equation support`
- Boundary: voltage-domain indirect equation certification for `V(out) : V(out) - expr == 0`; KCL/current solving and general nonlinear indirect branch equations are outside this task.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Repository checker: `check_v3_471_indirect_branch_null_balance`.
- Checker behavior: verifies that `out` tracks `inp` across visible and hidden PWL segments, rejecting zero, offset, inverse-polarity, and half-scale indirect-equation variants.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 471 --end 471 --tasks 471 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_471_after_indirect_branch_support.json`
- Per-task result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
- EVAS support commit: `1c193f6`.
- Boundary: does not claim complete indirect branch solver coverage, nonlinear equation solving, or conservative current-domain behavior.
