# Audit: Generate Genvar Replicated Stage

- Task id: `v3_449_generate_genvar_replicated_stage`
- Category: `veriloga_generate_semantics`
- Required syntax focus: `Use generate/genvar to replicate a behavioral stage.`
- EVAS status: `pending EVAS issue #45: https://github.com/Arcadia-1/EVAS/issues/45: https://github.com/Arcadia-1/EVAS/issues/45`
- Boundary: language coverage candidate; KCL/current solving is outside this task unless explicitly required by the syntax itself.
- Status: AMS/wreal generate candidate staged; behavior certification is blocked by generate/genvar elaboration plus wreal continuous assign support.

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: y@10ns=0.0000 expected=0.8000 tol=0.0500
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/45.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 449 --end 449 --tasks 449 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_issue_449_449.json`
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
