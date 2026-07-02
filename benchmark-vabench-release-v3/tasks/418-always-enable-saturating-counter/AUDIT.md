# Audit: Always Enable Saturating Counter

- Task id: `v3_418_always_enable_saturating_counter`
- Category: `verilogams_digital_mixed_semantics`
- Required syntax focus: `Use an always block for enabled saturating state update.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: executable AMS/digital mixed-signal candidate pending full behavioral certification.
- EVAS tracking: https://github.com/Arcadia-1/EVAS/issues/43

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: q0@90ns=0.0000 expected=1.0000 tol=0.0800
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/43.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 415 --end 455 --tasks 415,416,418,455 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_issue_415_455.json`
- Issue-level acceptance: After EVAS support lands, promote the listed 4 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 4/4 gold PASS, 20/20 negative variants rejected, and zero expectation_fail in the verification report.
