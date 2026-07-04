# Measurement Instrumentation Audit: Task 083 Crossing Metric Writer

## Gate 1

- Label: `independent_l1_ready`.
- Function boundary: standalone measurement helper that records the first
  rising threshold crossing of `vin` to a text metric file and asserts `done`.
- Counting note: useful as a measurement/instrumentation L1 row, not a core
  analog circuit row.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: public prompt now names only the DUT artifact, interface,
  parameters, file I/O behavior, and output contract.
- Modeling contract: `filename`, `vth`, and `tr` are public parameters; the
  completion flag is event-latched and transition-smoothed.
- Checker alignment: the checker measures first-crossing file output and `done`
  behavior from public observables.

## Validation

- AHDL-style preflight: PASS with 0 diagnostics.
- EVAS reference/negative sweep: reference PASS; 5/5 negatives rejected.
- Spectre private-split reference audit: PASS.
