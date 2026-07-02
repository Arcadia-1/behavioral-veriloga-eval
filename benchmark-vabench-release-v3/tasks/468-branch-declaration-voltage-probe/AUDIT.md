# Audit: Branch Declaration Voltage Probe

- Task id: `v3_468_branch_declaration_voltage_probe`
- Category: `veriloga_branch_semantics`
- Required syntax focus: `Declare an explicit branch and read its voltage.`
- EVAS status: `pending EVAS explicit branch voltage probe support; see https://github.com/Arcadia-1/EVAS/issues/50`

## Staged Promotion Gate

- Score claim: `excluded_until_behavior_promotion`.
- Current probe status: `FAIL_SIM_CORRECTNESS`.
- Current failure summary: out@10ns=0.0000 expected=0.1000 tol=0.0350
- Blocking issue(s): https://github.com/Arcadia-1/EVAS/issues/50.
- Promotion requirements: repository `sim_correct` checker evidence, gold PASS, five useful negative variants rejected, and zero expectation_fail in the promotion report.
- Per-task promotion command: `PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 468 --end 468 --tasks 468 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_468.json`
- Per-task acceptance: Promote `468-branch-declaration-voltage-probe` only after adding repository sim_correct evidence, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the per-task report.
- Issue-level acceptance: After EVAS support lands, promote the listed 1 task(s) by adding sim_correct behavior contracts/checkers if missing, then require 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail in the verification report.
