# Audit: Branch Declaration Voltage Probe

- Task id: `v3_468_branch_declaration_voltage_probe`
- Category: `veriloga_branch_semantics`
- Required syntax focus: `Declare an explicit branch and read its voltage.`
- EVAS status: `gold and five negative variants pass the staged promotion gate after EVAS explicit branch voltage probe support`
- Former blocking issue: `https://github.com/Arcadia-1/EVAS/issues/50`

## Staged Promotion Gate

- Score claim: `behavior-certified-extension`.
- Current probe status: `PASS`.
- Current verification summary: 1/1 gold PASS, 5/5 negative variants rejected, and zero expectation_fail.
- Promotion evidence: `benchmark-vabench-release-v3/reports/verify_task_468_after_branch_probe.json`.
- Per-task promotion command: `PYTHONPATH="/Users/mac/Documents/github-repos/EVAS:$PWD/runners" VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 468 --end 468 --tasks 468 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_468_after_branch_probe.json`
- Acceptance basis: EVAS resolves explicit `branch (p, n) br;` declarations so `V(br)` follows `V(p,n)` with a non-zero reference node, and the task remains voltage-domain only with no current contribution.
