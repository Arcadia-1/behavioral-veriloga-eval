# Honest SOP Audit: Task 022 Bandgap Reference Macro Model

## Scope

Task boundary is one Verilog-A DUT, `bandgap_reference_macro_model.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A bandgap-reference macro model is a practical bias/reference/power-management behavioral block.
- Reasonable task: pass. The public prompt fixes startup gating, nominal reference behavior, line regulation expectation, brownout reset behavior, valid indication, and voltage-only constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks pre-start low output, nominal reference level, line regulation, brownout reset, and valid metric. Five concrete negatives cover missing output, wrong reference level, premature startup, poor regulation/brownout behavior, and missing valid signal.
- Fair evaluation: pass for EVAS. Hidden checks follow the public macro-model behavior and use tolerant voltage windows.

## Checker And Evidence

- Checker id: `v3_022_bandgap_reference_macro_model`
- Runner mapping: `CHECKS["v3_022_bandgap_reference_macro_model"] = check_bandgap_reference_macro_model`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
