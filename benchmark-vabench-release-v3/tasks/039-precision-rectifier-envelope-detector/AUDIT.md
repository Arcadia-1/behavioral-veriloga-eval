# Honest SOP Audit: Task 039 Precision Rectifier Envelope Detector

## Scope

Task boundary is one Verilog-A DUT, `precision_rectifier_envelope_detector.va`, plus EVAS/Spectre-compatible `.scs` testbenches. Agent-visible materials are limited to `instruction.md`, `starter/`, and `test_visible/`. Evaluator-only materials are `solution/`, `test_hidden/`, `test_harness/`, and `negative_variants/`. No `meta.json` is present.

## Four Standards

- Useful scenario: pass. A precision rectifier/envelope detector is a common analog front-end and measurement macro.
- Reasonable task: pass. The public prompt fixes full-wave rectification around common mode, envelope hold/decay, reset behavior, and metric output.
- Complete tests: pass for EVAS. Hidden samples check rectification polarity, envelope peak hold, decay behavior, and memory metric. Five concrete negatives cover half-wave-only behavior, missing envelope hold, wrong common-mode handling, reset mistakes, and stuck outputs.
- Fair evaluation: pass for EVAS. The checker uses public waveform columns and behavioral targets described in the prompt.

## Checker And Evidence

- Checker id: `v3_039_precision_rectifier_envelope_detector`
- Runner mapping: `CHECKS["v3_039_precision_rectifier_envelope_detector"] = check_precision_rectifier_envelope_detector`
- EVAS/Python-engine hidden gold smoke: `PASS`
- Concrete negative recertification: 5/5 expected failures, all `FAIL_SIM_CORRECTNESS` with simulator `returncode=0`
- Visible compile/sim smoke: `COMPILE_SIM_OK`

## Remaining Risk

Spectre/Spectre-AX correlation has not been run from this working tree; use EVAS-only wording until that evidence exists.
