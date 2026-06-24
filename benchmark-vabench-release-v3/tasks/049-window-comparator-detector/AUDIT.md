# Honest SOP Audit: Task 049 Window Comparator Detector

## Scope

Task boundary is one Verilog-A DUT, `window_comparator_ref.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A window comparator is a common threshold-monitoring and range-detection macro.
- Reasonable task: pass. The public prompt fixes in-window assertion, outside-window deassertion, output span, and transition behavior.
- Complete tests: pass for EVAS. Hidden samples check below-window, above-window, rising into-window, falling into-window, and output span. Five concrete negatives cover inverted window logic, one-sided thresholding, stuck output, wrong window limits, and missing transitions.
- Fair evaluation: pass for EVAS. The checker uses public voltage observables and stated window behavior.

## Checker And Evidence

- Checker id: `v3_049_window_comparator_detector`
- Runner mapping: `CHECKS["v3_049_window_comparator_detector"] = check_true_window_comparator`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been rerun from this working tree; use EVAS-only wording unless fresh dual-simulator evidence is attached.
