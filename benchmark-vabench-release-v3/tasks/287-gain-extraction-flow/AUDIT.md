# Measurement Instrumentation Audit: Task 287 Gain Extraction Flow

## Gate 1

- Label: `l2_measurement_ready`.
- Function boundary: composed measurement flow connecting clocked stimulus,
  repeatable dither, fixed-gain amplification, and a transient Spectre testbench
  for gain extraction.
- Counting note: valid Measurement L2 row. It is not a Core Circuit L2 row.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: public prompt defines the composed artifacts, interfaces,
  public testbench parameters, saved observables, and flow-level behavior.
- Modeling repair: support copies remove debug `$strobe` output, use explicit
  transition rise/fall on clocked source outputs, and use event-updated dither
  target smoothing.
- Checker alignment: checker measures public differential input/output
  separation and rejects flow variants that break gain extraction.

## Validation

- AHDL-style preflight: PASS with 0 diagnostics.
- EVAS reference/negative sweep: reference PASS; 5/5 negatives rejected.
- Spectre private-split reference audit: PASS.
