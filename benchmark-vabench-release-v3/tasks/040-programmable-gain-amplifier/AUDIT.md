# Honest SOP Audit: Task 040 Programmable Gain Amplifier

## Scope

Task boundary is one Verilog-A DUT, `programmable_gain_amplifier.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A clocked programmable-gain amplifier is a practical baseband signal-conditioning block.
- Reasonable task: pass. The public prompt fixes gain selection, sampled gain updates, common-mode preservation, rail limiting, reset behavior, and metric output.
- Complete tests: pass for EVAS. Hidden samples check gain steps, hold behavior, common mode, clipping, and reset. Five concrete negatives cover wrong gain map, no sample/hold behavior, lost common mode, missing clipping, and reset mistakes.
- Fair evaluation: pass for EVAS. The checker is based on public input/output voltages and state behavior.

## Checker And Evidence

- Checker id: `v3_040_programmable_gain_amplifier`
- Runner mapping: `CHECKS["v3_040_programmable_gain_amplifier"] = check_programmable_gain_amplifier`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
