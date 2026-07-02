# Audit: Macro Ifdef Gain Select

- Task id: `v3_410_macro_ifdef_gain_select`
- Category: `veriloga_preprocessor_control_semantics`
- Required syntax focus: `Use ifdef selection to alter a behavioral gain constant.`
- EVAS status: `behavior-certified`
- Score claim: `extension_behavior_certified_outside_original_300`.

## Behavior Certification

- Checker: `macro_ifdef_gain_select_contract`.
- Required behavior: compile-time macro selection changes the gain used by the behavioral output.
- Visible/hidden coverage: hidden stimulus exercises the non-default gain path and calibrated output samples.
- Negative evidence: 5/5 variants are rejected by `FAIL_SIM_CORRECTNESS`.
- Evidence: `benchmark-vabench-release-v3/reports/verify_301_494_layered.json`.

## Boundary

This task certifies the repository transient/checker contract for preprocessor-controlled behavioral modeling. It is not part of the original full-300 denominator.
