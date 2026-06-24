# Honest SOP Audit: Task 047 Threshold Comparator

## Scope

Task boundary is one Verilog-A DUT, `comparator.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A threshold comparator is a basic comparator/decision macro used throughout mixed-signal systems.
- Reasonable task: pass. The public prompt fixes voltage-threshold comparison, output polarity, transition behavior, and public observables.
- Complete tests: pass for EVAS. Hidden samples check high/low fractions, edge alignment, output span, and both rising/falling decisions. Five concrete negatives cover inverted polarity, wrong threshold, missing transitions, stuck output, and no falling-edge response.
- Fair evaluation: pass for EVAS. The checker uses public voltage observables and simple threshold behavior stated in the prompt.

## Checker And Evidence

- Checker id: `v3_047_threshold_comparator`
- Runner mapping: `CHECKS["v3_047_threshold_comparator"] = check_release_threshold_comparator`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been rerun from this working tree; use EVAS-only wording unless fresh dual-simulator evidence is attached.
