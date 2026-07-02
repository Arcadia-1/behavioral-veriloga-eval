# Audit: Table Model String Param Source

- Task id: `v3_488_table_model_string_param_source`
- Category: `veriloga_table_model_semantics`
- Required syntax focus: `Use a string parameter as the $table_model() data source.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `syntax-extension-candidate`
- EVAS status: `executable tests added, but gold behavior is blocked by EVAS issue #40: https://github.com/Arcadia-1/EVAS/issues/40 because string-parameter $table_model data source returns 0`
- Blocking issue: `https://github.com/Arcadia-1/EVAS/issues/40`

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: out@10ns=0.0000 expected=0.1000 tol=0.0400
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/40.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 488 --end 488 --tasks 488 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_issue_488_488.json`
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
