# Honest SOP Audit: Task 046 Successive Approximation Calibration Search FSM

## Scope

Task boundary is one Verilog-A DUT, `successive_approximation_calibration_search_fsm.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A SAR-style calibration search controller is a practical mixed-signal calibration block.
- Reasonable task: pass. The public prompt fixes reset, clocked bit-search progression, direction response, and analog-coded output behavior.
- Complete tests: pass for EVAS. Hidden samples check reset value, output span, step direction, and decreasing step size. Five concrete negatives cover wrong search direction, missing SAR step reduction, reset mistakes, stuck output, and non-clocked behavior.
- Fair evaluation: pass for EVAS. The checker uses public voltage-coded observables and the stated calibration-search behavior.

## Checker And Evidence

- Checker id: `v3_046_successive_approximation_calibration_search_fsm`
- Runner mapping: `CHECKS["v3_046_successive_approximation_calibration_search_fsm"] = check_release_sar_calibration_fsm`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been rerun from this working tree; use EVAS-only wording unless fresh dual-simulator evidence is attached.
