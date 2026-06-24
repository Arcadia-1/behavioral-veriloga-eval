# Honest SOP Audit: Task 042 PTAT CTAT Reference Generator

## Scope

Task boundary is one Verilog-A DUT, `ptat_ctat_reference_generator.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. PTAT/CTAT compensation is a standard bias/reference behavioral-modeling scenario.
- Reasonable task: pass. The public prompt fixes temperature-coded behavior, monotonic PTAT metric, bounded reference output, and compensation flatness.
- Complete tests: pass for EVAS. Hidden samples check cold/mid/hot reference windows and PTAT monotonicity. Five concrete negatives cover non-monotonic PTAT, uncompensated reference drift, bad output range, reset/clock mistakes, and stuck outputs.
- Fair evaluation: pass for EVAS. The checker uses public voltage observables and stated temperature-sweep behavior.

## Checker And Evidence

- Checker id: `v3_042_ptat_ctat_reference_generator`
- Runner mapping: `CHECKS["v3_042_ptat_ctat_reference_generator"] = check_ptat_ctat_reference_generator`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
