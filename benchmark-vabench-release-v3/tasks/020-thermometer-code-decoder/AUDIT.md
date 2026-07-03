# Honest SOP Audit: Task 020 Thermometer Code Decoder

## Scope

Task boundary is one Verilog-A DUT, `thermometer_decoder_guarded.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Private validation materials include the reference solution, validation decks, harness code, and negative variants. No `meta.json` is present.

## Four Standards

- Useful scenario: pass as a support utility. A guarded thermometer-code decoder is a common data-converter helper block, but this two-bit version is intentionally classified as utility/support rather than as a core analog-circuit benchmark task.
- Reasonable task: pass. The public prompt fixes the module artifact, decoder behavior, guarded invalid-code handling, voltage-domain outputs, and voltage-only implementation constraints.
- Complete tests: pass for EVAS. Hidden stimulus checks the expected guarded output sequence over valid and invalid thermometer patterns. Five concrete negatives cover off-by-one decoding, missing guarded behavior, reversed mapping, stuck outputs, and incomplete decode width.
- Fair evaluation: pass for EVAS. Hidden scoring follows the public guarded decoder contract; exact stimulus timing remains private.

## Checker And Evidence

- Checker id: `v3_020_thermometer_code_decoder`
- Runner mapping: `CHECKS["v3_020_thermometer_code_decoder"] = check_vbm1_thermometer_decoder_guarded`
- EVAS/Python-engine gold semantic validation: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Release Classification

This task remains useful and should not be dropped, but it is classified as
`testbench_utility_modules` / `support-formal-candidate` so it is not presented
as a representative core analog/mixed-signal circuit-function task.

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
