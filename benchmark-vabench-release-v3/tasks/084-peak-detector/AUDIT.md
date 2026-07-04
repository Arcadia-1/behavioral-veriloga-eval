# Measurement Instrumentation Audit: Task 084 Peak Detector

## Gate 1

- Label: `independent_l1_ready`.
- Function boundary: standalone resettable peak detector that samples `vin`,
  retains the maximum value, clears on reset, and drives `vout`.
- Counting note: useful as a measurement/helper L1 row.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: release-wrapper and evaluator-boundary wording were removed.
- Modeling contract: the 500 ps sampling timer, reset threshold, and output
  transition are public behavior, not checker-only detail.
- Checker alignment: visible and private cases check hold, reset clear, and
  update to a larger later peak.

## Validation

- AHDL-style preflight: PASS with 0 diagnostics.
- EVAS reference/negative sweep: reference PASS; 5/5 negatives rejected.
- Spectre private-split reference audit: PASS.
