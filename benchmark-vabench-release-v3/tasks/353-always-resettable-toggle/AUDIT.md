# Honest SOP Audit: Always Resettable Toggle

## Scope

This task belongs to the AMS mixed-signal extension set. It is not part of the original full-300 Verilog-A-only claim.

## Four Standards

- Useful scenario: exercises `Use edge-triggered always with async reset.`
- Reasonable task: the prompt fixes the target artifact and keeps the task behavioral.
- Complete tests: visible/hidden harness placeholders and five concrete negative variants are materialized for evaluator integration.
- Fair evaluation: negatives are intended to compile under an AMS-capable simulator while changing small behavior details that should fail full checks.

Certification status: ams-mixed-signal-candidate. EVAS support is currently incomplete for event-or async-reset `always` behavior; tracking issue: https://github.com/Arcadia-1/EVAS/issues/39.

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: q@50ns=0.0000 expected=1.0000 tol=0.0800
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/39.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 353 --end 417 --tasks 353,417 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_issue_353_417.json`
- Issue-level acceptance: After EVAS support lands, promote the listed 2 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 2/2 gold PASS, 10/10 negative variants rejected, and zero expectation_fail in the verification report.
