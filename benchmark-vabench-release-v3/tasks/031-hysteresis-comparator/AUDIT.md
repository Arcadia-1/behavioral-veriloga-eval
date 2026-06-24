# Honest SOP Audit: Task 031 Hysteresis Comparator

## Scope

Task boundary is one Verilog-A DUT, `cmp_hysteresis.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A hysteresis comparator is a common decision-circuit primitive for noisy analog thresholds.
- Reasonable task: pass. The public prompt fixes rising/falling threshold hysteresis, latched state behavior between thresholds, rail output levels, smoothing, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden stimulus crosses both thresholds and checks rise/fall transition windows plus held state through the hysteresis region. Five concrete negatives cover missing hysteresis, wrong thresholds, inverted polarity, stuck output, and missing hold behavior.
- Fair evaluation: pass for EVAS. The checker scores public `vin`/`out` threshold windows and does not require hidden implementation structure.

## Checker And Evidence

- Checker id: `v3_031_hysteresis_comparator`
- Runner mapping: `CHECKS["v3_031_hysteresis_comparator"] = check_cmp_hysteresis`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
