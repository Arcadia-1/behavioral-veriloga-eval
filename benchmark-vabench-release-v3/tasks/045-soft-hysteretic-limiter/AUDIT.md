# Honest SOP Audit: Task 045 Soft Hysteretic Limiter

## Scope

Task boundary is one Verilog-A DUT, `soft_hysteretic_limiter.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A soft limiter with hysteresis is a practical baseband conditioning macro.
- Reasonable task: pass. The public prompt fixes upper/lower limiting, memory behavior, transition smoothing, and metric output.
- Complete tests: pass for EVAS. Hidden samples check limiting levels, hysteretic memory, and metric span. Five concrete negatives cover hard clipping, missing memory, wrong limits, stuck outputs, and metric mistakes.
- Fair evaluation: pass for EVAS. The checker uses public voltage observables and stated limiter behavior.

## Checker And Evidence

- Checker id: `v3_045_soft_hysteretic_limiter`
- Runner mapping: `CHECKS["v3_045_soft_hysteretic_limiter"] = check_release_soft_hysteretic_limiter`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been rerun from this working tree; use EVAS-only wording unless fresh dual-simulator evidence is attached.
