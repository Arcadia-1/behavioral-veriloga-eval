# Honest SOP Audit: Task 043 RF Mixer Downconverter Macro

## Scope

Task boundary is one Verilog-A DUT, `rf_mixer_downconverter_macro.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. An RF downconverter macro is a practical RF/AFE behavioral block.
- Reasonable task: pass. The public prompt fixes LO polarity control, conversion gain, baseband output bounding, and voltage-domain behavior.
- Complete tests: pass for EVAS. Hidden samples check LO sign control, conversion-gain visibility, and bounded baseband output. Five concrete negatives cover missing mixing sign, wrong gain, unbounded output, stuck output, and missing metric/baseband behavior.
- Fair evaluation: pass for EVAS. The checker uses public waveform observables and behavior specified in the prompt.

## Checker And Evidence

- Checker id: `v3_043_rf_mixer_downconverter_macro`
- Runner mapping: `CHECKS["v3_043_rf_mixer_downconverter_macro"] = check_rf_mixer_downconverter_macro`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
