# Honest SOP Audit: Task 028 Digital Phase Accumulator With Modulo Wrap

## Scope

Task boundary is one Verilog-A DUT, `phase_accumulator_timer_wrap_ref.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A modulo phase accumulator is a common PLL/NCO timing primitive.
- Reasonable task: pass. The public prompt fixes timer-based phase accumulation, modulo wrap behavior, clock output, phase observable, and voltage-domain constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks phase span, multiple wraps, and clock rising edges. Five concrete negatives cover missing accumulation, missing wrap, wrong phase drive, missing clock output, and stuck behavior.
- Fair evaluation: pass for EVAS. The checker uses public `phase_out` and `clk_out` observables and only scores the stated modulo phase behavior.

## Checker And Evidence

- Checker id: `v3_028_digital_phase_accumulator_with_modulo_wrap`
- Runner mapping: `CHECKS["v3_028_digital_phase_accumulator_with_modulo_wrap"] = check_phase_accumulator_timer_wrap`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
