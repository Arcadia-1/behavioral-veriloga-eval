# Honest SOP Audit: Task 037 PA Compression Macro

## Scope

Task boundary is one Verilog-A DUT, `pa_compression_macro.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A PA compression macro is a practical RF transmitter behavioral block.
- Reasonable task: pass. The public prompt fixes small-signal gain, low/high compression limits, metric output, and voltage-domain constraints.
- Complete tests: pass for EVAS. Hidden samples check gain and compressed output limits. Five concrete negatives cover missing gain, wrong compression metric, wrong scale/polarity, stuck output, and missing limit behavior.
- Fair evaluation: pass for EVAS. The checker uses public voltage transfer and metric behavior.

## Checker And Evidence

- Checker id: `v3_037_pa_compression_macro`
- Runner mapping: `CHECKS["v3_037_pa_compression_macro"] = check_pa_compression_macro`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
