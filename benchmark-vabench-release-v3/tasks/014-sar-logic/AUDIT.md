# Honest SOP Audit: Task 014 SAR Logic

## Scope

Task boundary is one Verilog-A DUT, `sar_logic_4b.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A 4-bit SAR decision sequencer is a common data-converter behavioral primitive.
- Reasonable task: pass. The public prompt fixes the module name, port order, voltage-domain logic convention, rising-edge SAR sequencing, comparator-decision capture, DAC decision pins, `RDY`, and voltage-only implementation constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks the `RDY` low/high/low timing and final DAC decision code. Five concrete negatives cover wrong bit capture, wrong ready timing, bit-order/decision errors, missing ready, and wrong final code.
- Fair evaluation: pass for EVAS. Hidden checks are all stated in the public prompt; exact stimulus timing remains private.

## Checker And Evidence

- Checker id: `v3_014_sar_logic`
- Runner mapping: `CHECKS["v3_014_sar_logic"] = check_vbm1_sar_logic_4b`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
