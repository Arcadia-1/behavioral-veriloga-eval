# Honest SOP Audit: Task 019 Unit Element Thermometer DAC

## Scope

Task boundary is one Verilog-A DUT, `thermometer_dac_15seg.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A 15-segment thermometer DAC is a useful unit-element data-converter behavioral model.
- Reasonable task: pass. The prompt fixes the 15 segment ports, thresholding rule, endpoint scaling by active segment count over 15, smoothed voltage output, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden safe-time samples cover active counts 0, 1, 2, 7, 14, and 15, including full-scale use of `seg14`, monotonicity, and endpoint scaling. Five concrete negatives cover gain error, wrong nonlinear weighting, inverted count, missing final segment, and scaling error.
- Fair evaluation: pass for EVAS. The hidden checker enforces only the public unit-element transfer function and uses tolerant safe-time samples.

## Checker And Evidence

- Checker id: `v3_019_unit_element_thermometer_dac`
- Runner mapping: `CHECKS["v3_019_unit_element_thermometer_dac"] = check_vbm1_thermometer_dac_15seg`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
