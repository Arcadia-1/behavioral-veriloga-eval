# Audit: Kcl Inductor Idt Voltage

- Task id: `v3_492_kcl_inductor_idt_voltage`
- Category: `veriloga_kcl_contribution_semantics`
- Required syntax focus: `Use voltage contribution with idt() of branch current for an inductor-style model.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `conservative-current/KCL-behavior-certified`
- EVAS status: `behavior-certified-candidate`
- EVAS fix: `c83cc63 Support branch-current idt in evas-rust`
- Closed blocker: `https://github.com/Arcadia-1/EVAS/issues/88`

## Promotion Evidence

- Score claim: `extension_row_behavior_certified_candidate`.
- Checker: `check_v3_492_kcl_inductor_idt_voltage`.
- Behavior contract: hidden Spectre PWL `isource` drives branch current `I(p,n)`; the DUT must produce `V(p,n) = 1n * idt(I(p,n), 0.0)` using Spectre's independent-source branch-current sign convention, with the expected rise, hold, reversal, and negative recovery samples.
- Negative variants: five near-miss variants compile/run but fail full behavior checks: zeroed integral, 2x scale, negated branch-current integral, nonzero idt initial condition, and 0.8x scale.
- Verification command: `PYTHONPATH=/Users/mac/Documents/github-repos/EVAS:$PWD/runners VAEVAS_DEFAULT_EVAS_ENGINE=evas-rust VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 492 --end 492 --tasks 492 --include-staged --timeout 120 --jobs 1 --out benchmark-vabench-release-v3/reports/verify_task_492_spectre_recalibrated_20260704.json --md-out benchmark-vabench-release-v3/reports/verify_task_492_spectre_recalibrated_20260704.md`
- Verification result: `1/1 gold PASS`, `5/5 negative variants rejected`, and `0 expectation_fail`.
- Evidence report: `benchmark-vabench-release-v3/reports/verify_task_492_spectre_recalibrated_20260704.json`.
