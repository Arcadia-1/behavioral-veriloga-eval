# Honest SOP Audit: Task 016 Binary Weighted Voltage DAC

## Scope

Task boundary is one Verilog-A DUT, `simple_binary_voltage_dac_4b.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A 4-bit binary voltage DAC transfer model is a basic data-converter behavioral primitive.
- Reasonable task: pass. The prompt fixes the module name, bit order, reference endpoints, `code/15` transfer function, smoothing, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden stimulus exercises all 16 codes and checks code observability, monotonicity, zero-scale, full-scale, and bit weights. Five concrete negatives cover gain error, wrong bit weights, reversed bit order, endpoint offset, and MSB saturation.
- Fair evaluation: pass for EVAS. The hidden scoring behavior is exactly the public mathematical transfer function.

## Checker And Evidence

- Checker id: `v3_016_binary_weighted_voltage_dac`
- Runner mapping: `CHECKS["v3_016_binary_weighted_voltage_dac"] = check_simple_binary_dac_4b`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
