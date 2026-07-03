# Honest SOP Audit: Always Resettable Toggle

## Scope

This task belongs to the AMS mixed-signal extension set. It is not part of the original full-300 Verilog-A-only claim.

## Four Standards

- Useful scenario: exercises `Use edge-triggered always with async reset.`
- Reasonable task: the prompt fixes the target artifact and keeps the task behavioral.
- Complete tests: visible/hidden harness placeholders and five concrete negative variants are materialized for evaluator integration.
- Fair evaluation: negatives are intended to compile under an AMS-capable simulator while changing small behavior details that should fail full checks.

Certification status: behavior-certified AMS mixed-signal extension. Former EVAS tracking issue: https://github.com/Arcadia-1/EVAS/issues/39.

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_tasks_353_476_487_probe.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 353 --end 353 --tasks 353 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_tasks_353_476_487_probe.json`
- Acceptance basis: EVAS now executes the resettable `always` behavior and the five negative variants fail the waveform checker.
