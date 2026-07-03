# Measurement Instrumentation Audit: Task 102 Gain Estimator

## Gate 1

- Label: `independent_l1_ready`.
- Function boundary: standalone gain measurement helper that tracks differential
  input/output spans and reports a normalized gain metric with a validity flag.
- Counting note: measurement/instrumentation L1 row.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: old testbench-generation context and evaluator wording were
  removed.
- Metadata repair: duplicate `./gain_estimator.va` target entry was removed.
- Modeling repair: `transition()` is fed by event-updated normalized targets,
  with `V(VDD,VSS)` scaling outside the transition expression.
- Checker alignment: checker compares waveform gain, reported gain metric, and
  final validity.

## Validation

- AHDL-style preflight: PASS with 0 diagnostics.
- EVAS reference/negative sweep: reference PASS; 5/5 negatives rejected.
- Spectre private-split reference audit: PASS.
