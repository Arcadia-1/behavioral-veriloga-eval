# Honest SOP Audit: Task 017 Slew Rate Limiter

## Scope

Task boundary is one Verilog-A DUT, `slew_rate_limiter.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A slew-rate limiter is a common baseband and control-loop behavioral block.
- Reasonable task: pass. The prompt states the 1 ns timer cadence, maximum 15 mV update step, bidirectional limiting, output smoothing, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden stimulus exercises a rising step and falling step, checks lagged response, eventual high/low reach, and both rising/falling slew limits. Five concrete negatives cover stuck output, passthrough behavior, wrong update logic, too-slow movement, and missing falling response.
- Fair evaluation: pass for EVAS. The checker uses public `vin`/`vout` behavior and tolerant level windows rather than hidden structural assumptions.

## Checker And Evidence

- Checker id: `v3_017_slew_rate_limiter`
- Runner mapping: `CHECKS["v3_017_slew_rate_limiter"] = check_vbm1_slew_rate_limiter`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
