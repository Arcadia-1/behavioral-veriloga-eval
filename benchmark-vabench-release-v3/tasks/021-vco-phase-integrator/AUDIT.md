# Honest SOP Audit: Task 021 VCO Phase Integrator

## Scope

Task boundary is one Verilog-A DUT, `vco_phase_integrator.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A VCO phase integrator is a core PLL/clock-timing behavioral primitive.
- Reasonable task: pass. The public prompt fixes voltage-domain control, phase accumulation/wrap behavior, clock output observables, and implementation constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks phase growth, phase span/wrap behavior, and generated clock edge activity. Five concrete negatives cover no integration/clocking and wrong phase/edge behavior.
- Fair evaluation: pass for EVAS. The checker uses public phase and clock observables rather than hidden structural assumptions.

## Checker And Evidence

- Checker id: `v3_021_vco_phase_integrator`
- Runner mapping: `CHECKS["v3_021_vco_phase_integrator"] = check_vbm1_vco_phase_integrator`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
