# Audit: Indirect Branch Ddt Balance

- Task id: `v3_472_indirect_branch_ddt_balance`
- Category: `veriloga_indirect_branch_semantics`
- Required syntax focus: `Use indirect branch assignment with a ddt() equation term.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavioral-continuous-time-candidate`
- EVAS status: `behavior-certified with narrow indirect branch ddt-equation support`
- Boundary: voltage-domain behavioral integration for `V(out) : ddt(V(out)) == expr`; KCL/current solving and general dynamic equation solving are outside this task.

## Promotion Evidence

- Score claim: `extension_behavior_certified_outside_original_300`.
- Repository checker: `check_v3_472_indirect_branch_ddt_balance`.
- Checker behavior: compares `out` against the trapezoidal integral of the driven `inp` waveform across visible and hidden segments, rejecting zero-derivative, biased, leaky, and half-scale dynamic equation variants.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 472 --end 472 --tasks 472 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_472_after_indirect_branch_support.json`
- Per-task result: `1/1 gold PASS; 5/5 negative variants rejected; 0 expectation_fail`.
- EVAS support commit: `1c193f6`.
- Boundary: does not claim full `ddt()` simulator equivalence, nonlinear dynamic equation solving, or conservative current-domain behavior.
