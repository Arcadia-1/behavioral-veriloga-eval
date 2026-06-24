# Honest SOP Audit: Task 030 Higher Order Filter

## Scope

Task boundary is one Verilog-A DUT, `higher_order_filter.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A higher-order low-pass/filter macro is a common baseband behavioral block.
- Reasonable task: pass. The prompt fixes the intended lagged two-pole-like response, rise/fall behavior, output range, smoothing, and voltage-domain constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks lagged rising response, later settling, falling response, and metric span. Five concrete negatives cover passthrough, stuck/midscale behavior, wrong polarity/dynamics, missing lag, and inadequate response span.
- Fair evaluation: pass for EVAS. The checker uses public `vin`/`vout` response windows and tolerant dynamic behavior, not a hidden equation implementation.

## Checker And Evidence

- Checker id: `v3_030_higher_order_filter`
- Runner mapping: `CHECKS["v3_030_higher_order_filter"] = check_release_two_pole_filter`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
