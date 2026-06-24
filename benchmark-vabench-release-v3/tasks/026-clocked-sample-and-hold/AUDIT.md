# Honest SOP Audit: Task 026 Clocked Sample And Hold

## Scope

Task boundary is one Verilog-A DUT, `sample_hold.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A clocked sample-and-hold is a common sampling/analog-memory primitive.
- Reasonable task: pass. The public prompt fixes the module interface, edge-triggered sampling behavior, held output behavior, voltage-domain logic threshold, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks repeated sampling edges and hold windows. Five concrete negatives cover wrong sampling edge, transparent behavior, stuck output, missing hold, and wrong sampled level behavior.
- Fair evaluation: pass for EVAS. The checker uses public `vin`, `clk`, and `vout` observables and does not require hidden structural implementation.

## Checker And Evidence

- Checker id: `v3_026_clocked_sample_and_hold`
- Runner mapping: `CHECKS["v3_026_clocked_sample_and_hold"] = check_sample_hold`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
