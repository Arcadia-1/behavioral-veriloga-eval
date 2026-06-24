# Honest SOP Audit: Task 027 DAC Mismatch Unit Weighting Model

## Scope

Task boundary is one Verilog-A DUT, `dac_mismatch_unit_weighting_model.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A DAC unit-weighting model with mismatch is a realistic data-converter behavioral primitive.
- Reasonable task: pass. The prompt fixes the unit weighting, mismatch behavior, reference scaling, output smoothing, and voltage-only implementation constraints.
- Complete tests: pass for EVAS. Hidden samples check representative unit-weighted output levels, including low-code, mid-code, and full-scale behavior. Five concrete negatives cover gain errors, wrong weighting, swapped/missing units, saturation, and endpoint mismatch.
- Fair evaluation: pass for EVAS. The checker enforces the public transfer levels with tolerance and does not rely on implementation internals.

## Checker And Evidence

- Checker id: `v3_027_dac_mismatch_unit_weighting_model`
- Runner mapping: `CHECKS["v3_027_dac_mismatch_unit_weighting_model"] = check_release_dac_mismatch_unit_weighting`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
