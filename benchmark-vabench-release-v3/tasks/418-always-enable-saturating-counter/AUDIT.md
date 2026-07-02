# Audit: Always Enable Saturating Counter

- Task id: `v3_418_always_enable_saturating_counter`
- Category: `verilogams_digital_mixed_semantics`
- Required syntax focus: `Use an always block for enabled saturating state update.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: behavior-certified AMS/digital vector-output always extension task.
- Former EVAS tracking: https://github.com/Arcadia-1/EVAS/issues/43

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_tasks_417_418_after_digital_fixes.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 417 --end 418 --tasks 417,418 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_tasks_417_418_after_digital_fixes.json`
- Acceptance basis: the packed vector output is connected high-to-low as `q1 q0`, and the hidden checker rejects hold, early-saturation, reset-bias, wrong-step, and enable-polarity mistakes.
