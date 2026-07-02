# Audit: Mfactor System Function Gain

- Task id: `v3_480_mfactor_system_function_gain`
- Category: `veriloga_mfactor_semantics`
- Required syntax focus: `Use $mfactor() to scale behavioral gain.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `syntax-extension-candidate`
- EVAS status: `executable tests added, but gold compile is blocked by EVAS issue #53: https://github.com/Arcadia-1/EVAS/issues/53 because $mfactor() is unsupported`
- Blocking issue: `https://github.com/Arcadia-1/EVAS/issues/53`

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_DUT_COMPILE`.
- Current failure summary: simulator_error=Failed to compile Verilog-A file mfactor_system_function_gain.va: Spectre-incompatible/unsupported Verilog-A function call: $mfactor()
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/53.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 480 --end 480 --tasks 480 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_480.json`
- Per-task acceptance: Promote `480-mfactor-system-function-gain` only after adding repository sim_correct evidence, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the per-task report.
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
