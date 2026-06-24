# Honest SOP Audit: Task 036 Loop Filter Abstraction

## Scope

Task boundary is one Verilog-A DUT, `loop_filter_abstraction.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A PI-style loop-filter abstraction is a common PLL/control-loop behavioral primitive.
- Reasonable task: pass. The public prompt fixes UP/DOWN response, proportional decay, integral residual, reset clearing, metric windows, and voltage-domain constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks positive and negative PI responses, residual integral behavior, metric timing, and reset clearing. Five concrete negatives cover missing PI response, wrong direction, no proportional decay, missing reset behavior, and collapsed output.
- Fair evaluation: pass for EVAS. The checker scores public loop-filter response windows rather than implementation internals.

## Checker And Evidence

- Checker id: `v3_036_loop_filter_abstraction`
- Runner mapping: `CHECKS["v3_036_loop_filter_abstraction"] = check_release_loop_filter`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
