# Audit: Analog Node Alias Initial

- Task id: `v3_477_analog_node_alias_initial`
- Category: `veriloga_alias_semantics`
- Required syntax focus: `Use $analog_node_alias inside analog initial for hierarchical node aliasing.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `evas-unsupported-candidate`
- EVAS status: `executable tests added, but gold behavior is blocked by EVAS issue #52: https://github.com/Arcadia-1/EVAS/issues/52 because $analog_node_alias leaves the aliased node at 0`
- Blocking issue: `https://github.com/Arcadia-1/EVAS/issues/52`

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: out@50ns=0.0000 expected=0.2000 tol=0.0350
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/52.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 477 --end 477 --tasks 477 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_477.json`
- Per-task acceptance: Promote `477-analog-node-alias-initial` only after adding repository sim_correct evidence, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the per-task report.
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
