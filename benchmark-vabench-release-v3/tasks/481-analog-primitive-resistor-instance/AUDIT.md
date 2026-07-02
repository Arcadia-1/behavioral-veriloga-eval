# Audit: Analog Primitive Resistor Instance

- Task id: `v3_481_analog_primitive_resistor_instance`
- Category: `veriloga_analog_primitive_semantics`
- Required syntax focus: `Instantiate a Spectre analog resistor primitive inside a Verilog-A module.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `kcl-syntax-candidate`
- EVAS status: `gold and five negative variants pass after inert analog primitive metadata support`
- Boundary: structure-certified primitive instantiation only; resistor current and MNA/KCL behavior remain outside this task.

## Staged Promotion Gate

- Score claim: `structure-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_481_482_after_primitive_metadata.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 481 --end 482 --tasks 481,482 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_481_482_after_primitive_metadata.json`
- Acceptance basis: EVAS compiles and stages the inert `resistor` primitive metadata, and the repository artifact checker requires exactly one `resistor #(.r(1000.0))` instance connected as `(p, n)` while rejecting five wrong resistor values.
