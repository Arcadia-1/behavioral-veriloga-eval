# Honest SOP Audit: Task 018 Strongarm Style Latch Comparator

## Scope

Task boundary is one Verilog-A DUT, `cmp_strongarm.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A clocked latch comparator is a common ADC/comparator behavioral primitive.
- Reasonable task: pass. The public prompt fixes the StrongARM-style interface, rising-edge decision, falling-edge reset, latched high-phase behavior, complementary outputs, latch-state observables, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks positive and negative decisions, reset-low behavior on falling clock, output toggling, and held decisions despite input swaps. Five concrete negatives cover missing complementary toggle/decision behavior and reset/hold mistakes.
- Fair evaluation: pass for EVAS. Hidden scoring follows the public edge-latched comparator contract; exact waveform timing remains private.

## Checker And Evidence

- Checker id: `v3_018_strongarm_style_latch_comparator`
- Runner mapping: `CHECKS["v3_018_strongarm_style_latch_comparator"] = check_release_strongarm_latch_comparator`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
