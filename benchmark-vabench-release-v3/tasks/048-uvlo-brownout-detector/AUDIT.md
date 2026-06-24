# Honest SOP Audit: Task 048 UVLO Brownout Detector

## Scope

Task boundary is one Verilog-A DUT, `uvlo_brownout_detector.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. UVLO/brownout detection is a practical power-management protection macro.
- Reasonable task: pass. The public prompt fixes undervoltage thresholding, hysteresis hold, brownout detection, and recovery behavior.
- Complete tests: pass for EVAS. Hidden samples check initial low state, power-good hold, brownout/lower-threshold behavior, and recovery. Five concrete negatives cover missing hysteresis, wrong polarity, missing brownout, stuck output, and bad recovery.
- Fair evaluation: pass for EVAS. The checker uses public voltage observables and behavior stated in the prompt.

## Checker And Evidence

- Checker id: `v3_048_uvlo_brownout_detector`
- Runner mapping: `CHECKS["v3_048_uvlo_brownout_detector"] = check_uvlo_brownout_detector`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
