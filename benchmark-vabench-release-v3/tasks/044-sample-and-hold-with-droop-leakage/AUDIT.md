# Honest SOP Audit: Task 044 Sample And Hold With Droop Leakage

## Scope

Task boundary is one Verilog-A DUT, `leaky_hold.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. Sample/hold behavior with droop is a common analog-memory macro.
- Reasonable task: pass. The public prompt fixes sampled input capture, held output, leakage droop, reset behavior, and voltage-domain constraints.
- Complete tests: pass for EVAS. Hidden samples check held values, droop direction/magnitude, reset clear, and sample timing. Five concrete negatives cover no droop, wrong sampling, reset mistakes, output stuckness, and wrong hold direction.
- Fair evaluation: pass for EVAS. The checker uses public waveform observables and behavioral targets stated in the prompt.

## Checker And Evidence

- Checker id: `v3_044_sample_and_hold_with_droop_leakage`
- Runner mapping: `CHECKS["v3_044_sample_and_hold_with_droop_leakage"] = check_release_vin_sampled_droop_hold`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been rerun from this working tree; use EVAS-only wording unless fresh dual-simulator evidence is attached.
