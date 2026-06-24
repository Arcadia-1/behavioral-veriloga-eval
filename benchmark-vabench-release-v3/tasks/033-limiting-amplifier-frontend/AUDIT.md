# Honest SOP Audit: Task 033 Limiting Amplifier Frontend

## Scope

Task boundary is one Verilog-A DUT, `limiting_amplifier_frontend.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A limiting amplifier frontend is a useful RF/AFE behavioral macro.
- Reasonable task: pass. The public prompt fixes small-signal gain, output limiting, polarity, metric output, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden samples check small-signal gain and limited low/high output behavior. Five concrete negatives cover missing gain, weak limits, wrong polarity/scale, stuck output, and missing metric.
- Fair evaluation: pass for EVAS. The checker uses public input/output windows and tolerant level requirements.

## Checker And Evidence

- Checker id: `v3_033_limiting_amplifier_frontend`
- Runner mapping: `CHECKS["v3_033_limiting_amplifier_frontend"] = check_limiting_amplifier_frontend`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
