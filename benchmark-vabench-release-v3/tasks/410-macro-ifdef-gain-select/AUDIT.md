# Audit: Macro Ifdef Gain Select

- Task id: `v3_410_macro_ifdef_gain_select`
- Category: `veriloga_preprocessor_control_semantics`
- Required syntax focus: `Use `ifdef selection to alter a behavioral gain constant.`
- Boundary: behavioral voltage/digital modeling only; no `I(...)` current contribution.
- Status: language extension candidate pending full behavioral certification.
- Blocking issue: local `define/`ifdef support is not yet behavior-certified in EVAS; see https://github.com/Arcadia-1/EVAS/issues/42.

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: out@160ns=0.4800 expected=0.8000 tol=0.0800
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/42.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 410 --end 410 --tasks 410 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_issue_410_410.json`
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
