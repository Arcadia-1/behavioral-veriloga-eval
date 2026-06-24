# Honest SOP Audit: Task 025 Clocked ADC Quantizer

## Scope

Task boundary is one Verilog-A DUT, `flash_adc_3b.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A clocked 3-bit ADC quantizer is a common data-converter behavioral primitive.
- Reasonable task: pass. The public prompt fixes the clocked sampling behavior, 3-bit output code, voltage-domain logic levels, monotonic quantization, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden stimulus exercises all eight quantizer codes and checks monotonic code progression. Five concrete negatives cover missing codes, wrong thresholds, reversed/nonmonotonic behavior, and collapsed output coding.
- Fair evaluation: pass for EVAS. Hidden checks enforce the public clocked quantizer transfer behavior without hidden implementation requirements.

## Checker And Evidence

- Checker id: `v3_025_clocked_adc_quantizer`
- Runner mapping: `CHECKS["v3_025_clocked_adc_quantizer"] = check_flash_adc_3b`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
