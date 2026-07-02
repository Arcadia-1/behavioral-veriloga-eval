# Audit: Analog Node Alias Initial

- Task id: `v3_477_analog_node_alias_initial`
- Category: `veriloga_alias_semantics`
- Required syntax focus: `Use $analog_node_alias inside analog initial for hierarchical node aliasing.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavior-certified-extension`
- EVAS status: `gold and five negative variants pass the staged promotion gate after EVAS analog node alias support`
- Former blocking issue: `https://github.com/Arcadia-1/EVAS/issues/52`

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_477_after_analog_node_alias.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 477 --end 477 --tasks 477 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_477_after_analog_node_alias.json`
- Acceptance basis: EVAS maps the internal `aliased` node to `$root.vin` during `analog initial`, so the output follows the top-level source without adding an input port bypass.
