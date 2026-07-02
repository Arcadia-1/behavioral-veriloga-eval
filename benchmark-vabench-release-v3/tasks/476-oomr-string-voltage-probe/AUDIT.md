# Audit: Oomr String Voltage Probe

- Task id: `v3_476_oomr_string_voltage_probe`
- Category: `veriloga_oomr_semantics`
- Required syntax focus: `Use a string out-of-module reference in a voltage probe.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `syntax-extension-candidate`
- EVAS status: `executable tests added, but gold behavior is blocked by EVAS issue #51: https://github.com/Arcadia-1/EVAS/issues/51 because V(sigpath) resolves to 0`
- Blocking issue: `https://github.com/Arcadia-1/EVAS/issues/51`

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: out@50ns=0.0000 expected=0.2000 tol=0.0350
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/51.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 476 --end 476 --tasks 476 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_issue_476_476.json`
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
