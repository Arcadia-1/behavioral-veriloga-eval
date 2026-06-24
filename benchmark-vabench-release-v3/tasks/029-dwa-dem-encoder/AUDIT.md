# Honest SOP Audit: Task 029 DWA DEM Encoder

## Scope

Task boundary is Verilog-A DUT artifact `dwa_ptr_gen.va` plus companion converter `v2b_4b.va`, with EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A data-weighted-averaging DEM encoder is a realistic calibration/control primitive for unit-element DACs.
- Reasonable task: pass. The public prompt fixes pointer reset, unsigned code decode, pointer update `(ptr_prev + code) % 16`, one-hot pointer output, selected-cell MSB span, LSB boundary cell, and voltage-domain constraints.
- Complete tests: pass for EVAS. Hidden stimulus drives multiple codes, wraparound, split windows, pointer one-hot behavior, and active-cell masks. Five concrete negatives cover pointer offset, wrong span/window, missing boundary cell, reset/state mistakes, and stuck selection.
- Fair evaluation: pass for EVAS. The checker reconstructs expected pointer/cell masks from public observables and does not use hidden implementation details.

## Checker And Evidence

- Checker id: `v3_029_dwa_dem_encoder`
- Runner mapping: `CHECKS["v3_029_dwa_dem_encoder"] = check_dwa_dem_encoder_release`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`
- Runner fix applied: multi-artifact tasks now stage the primary candidate under the first target artifact and fill missing companion artifacts from `solution/` or `starter/` without overwriting them.

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
