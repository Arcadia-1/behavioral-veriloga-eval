# Honest SOP Audit: Task 038 Power On Reset Detector

## Scope

Task boundary is one Verilog-A DUT, `power_on_reset_detector.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. Power-on reset behavior is a practical power-management macro for mixed-signal startup and brownout handling.
- Reasonable task: pass. The public prompt fixes active-high reset behavior, supply threshold, clocked release delay, and brownout reassertion.
- Complete tests: pass for EVAS. Hidden samples check reset assertion below threshold, delayed release after power-good, and brownout recovery. Five concrete negatives cover missing thresholding, wrong delay, missing brownout, inverted reset, and stuck metric/output behavior.
- Fair evaluation: pass for EVAS. The checker uses public voltage observables and timing behavior that are stated in the prompt.

## Checker And Evidence

- Checker id: `v3_038_power_on_reset_detector`
- Runner mapping: `CHECKS["v3_038_power_on_reset_detector"] = check_power_on_reset_detector`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
