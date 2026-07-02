# Audit: Branch Current Probe Contribution

- Task id: `v3_470_branch_current_probe_contribution`
- Category: `veriloga_kcl_contribution_semantics`
- Required syntax focus: `Use a named branch with current contribution and current probing.`
- EVAS status: `compile-supported KCL syntax candidate; behavior requires KCL/MNA and branch-current certification`
- Blocking issue: branch-current behavior requires continuous-time/KCL support in EVAS; see https://github.com/Arcadia-1/EVAS/issues/44.

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: out@50ns=0.0000 expected_branch_current=0.5000 out@90ns=0.0000 expected_branch_current=0.2000
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/44.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 435 --end 494 --tasks 435,436,437,438,439,440,441,442,443,444,469,470,471,472,491,492,493,494 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_issue_435_494.json`
- Issue-level acceptance: After EVAS support lands, promote the listed 18 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 18/18 gold PASS, 90/90 negative variants rejected, and zero expectation_fail in the verification report.
