# Audit: Analog Primitive Resistor Instance

- Task id: `v3_481_analog_primitive_resistor_instance`
- Category: `veriloga_analog_primitive_semantics`
- Required syntax focus: `Instantiate a Spectre analog resistor primitive inside a Verilog-A module.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `kcl-syntax-candidate`
- EVAS status: `primitive-instantiation smoke tests staged, but EVAS issue #54: https://github.com/Arcadia-1/EVAS/issues/54 blocks execution because resistor is treated as an unknown child module`
- Blocking issue: `https://github.com/Arcadia-1/EVAS/issues/54`

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_TB_COMPILE`.
- Current failure summary: simulator_error=Unknown child module: resistor in analog_primitive_resistor_instance.rload
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/54.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 481 --end 481 --tasks 481 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_issue_481_481.json`
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
