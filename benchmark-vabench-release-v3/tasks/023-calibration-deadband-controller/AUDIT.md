# Honest SOP Audit: Task 023 Calibration Deadband Controller

## Scope

Task boundary is one Verilog-A DUT, `calibration_deadband_controller.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A deadbanded calibration controller is a common mixed-signal trim/control primitive.
- Reasonable task: pass. The public prompt fixes reset/initial behavior, update direction, deadband hold behavior, output trim range, and voltage-domain constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks reset level, trim span, correction direction, and hold behavior inside the deadband. Five concrete negatives cover stuck trim, reversed direction, missing deadband hold, insufficient span, and wrong hold behavior.
- Fair evaluation: pass for EVAS. The checker uses public error/trim behavior and does not require hidden structural implementation.

## Checker And Evidence

- Checker id: `v3_023_calibration_deadband_controller`
- Runner mapping: `CHECKS["v3_023_calibration_deadband_controller"] = check_release_deadband_calibration`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
