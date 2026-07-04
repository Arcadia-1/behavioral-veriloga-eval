# Audit: Kcl Inductor Idt Voltage

- Task id: `v3_492_kcl_inductor_idt_voltage`
- Category: `veriloga_kcl_contribution_semantics`
- Required syntax focus: `Use voltage contribution with idt() of branch current for an inductor-style model.`
- Certification scope: `language_extension_not_part_of_original_full_300_claim`
- Tier: `conservative-current/KCL-behavior-certified`
- EVAS status: `spectre-divergent pending branch-current idt parity`
- Blocking issue: `https://github.com/Arcadia-1/EVAS/issues/88`

## Promotion Evidence

- Score claim: `excluded_until_spectre_parity_promotion`.
- Checker: `check_v3_492_kcl_inductor_idt_voltage`.
- Behavior contract: hidden Spectre PWL `isource` drives branch current `I(p,n)`; the DUT must produce `V(p,n) = 1n * idt(I(p,n), 0.0)` with the expected rise, hold, reversal, and negative recovery samples.
- Negative variants: five near-miss variants compile/run but fail full behavior checks: zeroed integral, 2x scale, negated branch-current integral, nonzero idt initial condition, and 0.8x scale.
- Current Python command: `PYTHONPATH=/Users/mac/Documents/github-repos/EVAS:$PWD/runners VAEVAS_DEFAULT_EVAS_ENGINE=python VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH="$PWD/.venv-evas/bin:$PATH" .venv-evas/bin/python scripts/run_v3_gold_negative_verification.py --start 492 --end 492 --tasks 492 --include-staged --timeout 120 --jobs 1 --out scratch/verify_492_python_current.json`
- Current Python result: `gold_fail=1`, `negative_accepted=1`, `expectation_fail=2`.
- Current evas-rust result: `gold_fail=1`; strict Rust path rejects this DUT before `tran.csv` with `RustSimProgram rejection: model:0:kcl_inductor_idt_voltage_Model:no_continuous_linear_ir`.
- Promotion gate: fix EVAS #88, add/verify evas-rust lowering coverage, then recalibrate this checker/golden against Spectre and require `1/1 gold PASS`, `5/5 negative variants rejected`, and `0 expectation_fail`.
