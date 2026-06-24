# Honest SOP Audit: Task 015 Segmented DAC

## Scope

Task boundary is one Verilog-A DUT, `segmented_dac.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A segmented DAC transfer model is a realistic data-converter block and tests mixed binary plus thermometer weighting.
- Reasonable task: pass. The public prompt states the exact interface, binary LSB weighting, thermometer segment weighting, reference scaling, smoothed voltage output, and voltage-only subset constraints.
- Complete tests: pass for EVAS. Hidden safe-time samples cover zero, LSB, binary combination, thermometer contribution, monotonicity, and full-scale behavior. Five concrete negatives cover gain error, wrong binary weights, swapped bit weights, missing thermometer segment weight, and scaling error.
- Fair evaluation: pass for EVAS. The hidden checker enforces the public transfer function with tolerance away from transitions.

## Checker And Evidence

- Checker id: `v3_015_segmented_dac`
- Runner mapping: `CHECKS["v3_015_segmented_dac"] = check_vbm1_segmented_dac`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
