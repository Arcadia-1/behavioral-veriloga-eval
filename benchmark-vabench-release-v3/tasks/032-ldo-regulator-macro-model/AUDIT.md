# Honest SOP Audit: Task 032 LDO Regulator Macro Model

## Scope

Task boundary is one Verilog-A DUT, `ldo_regulator_macro_model.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. An LDO regulator macro model is a practical bias/reference/power-management behavioral block.
- Reasonable task: pass. The public prompt fixes light-load regulation, load-step droop, recovery behavior, metric output, voltage-domain outputs, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks light-load level, heavy-load droop, recovery, and metric windows. Five concrete negatives cover missing droop, wrong regulation level, no recovery, and bad metric behavior.
- Fair evaluation: pass for EVAS. The checker scores public voltage/metric behavior and does not require internal loop structure.

## Checker And Evidence

- Checker id: `v3_032_ldo_regulator_macro_model`
- Runner mapping: `CHECKS["v3_032_ldo_regulator_macro_model"] = check_ldo_regulator_macro_model`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
