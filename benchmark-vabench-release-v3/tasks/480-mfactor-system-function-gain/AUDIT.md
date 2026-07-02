# Audit: Mfactor System Function Gain

- Task id: `v3_480_mfactor_system_function_gain`
- Category: `veriloga_mfactor_semantics`
- Required syntax focus: `Use $mfactor() to scale behavioral gain.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `behavior-certified-extension`
- EVAS status: `gold and five negative variants pass the staged promotion gate after EVAS $mfactor() support`
- Former blocking issue: `https://github.com/Arcadia-1/EVAS/issues/53`

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_480_after_mfactor.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 480 --end 480 --tasks 480 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_480_after_mfactor.json`
- Acceptance basis: EVAS reads the Spectre instance `m=` parameter as the runtime `$mfactor()` value; the checker rejects zero, threshold, bias, metric-offset, and scale-output negative variants.
