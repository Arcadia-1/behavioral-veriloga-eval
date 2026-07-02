# Audit: Oomr String Voltage Probe

- Task id: `v3_476_oomr_string_voltage_probe`
- Category: `veriloga_oomr_semantics`
- Required syntax focus: `Use a string out-of-module reference in a voltage probe.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavior-certified-extension`
- EVAS status: `gold and five negative variants pass the staged promotion gate after string OOMR voltage probe support`
- Former blocking issue: `https://github.com/Arcadia-1/EVAS/issues/51`

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_tasks_353_476_487_probe.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 476 --end 476 --tasks 476 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_tasks_353_476_487_probe.json`
- Acceptance basis: EVAS resolves the string OOMR `V(sigpath)` to the top-level voltage source, including the hidden negative-voltage segment.
