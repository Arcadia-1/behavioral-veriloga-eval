# Measurement Instrumentation Audit: Task 111 Clocked Sine Source

## Gate 1

- Label: `l2_support_component`.
- Function boundary: `vin_src.va` is a clocked, sample-held differential sine
  stimulus source used inside the gain-extraction measurement flow.
- Counting note: keep as support for the measurement-flow family, not as
  standalone L1 credit in its current evaluation shape.

## Gate 2

- Status: `cadence_modeling_ready` for the support-component claim.
- Prompt hygiene: public prompt names only `vin_src.va` as the reviewed support
  component and avoids private-hook wording.
- Metadata repair: release metadata now targets only `vin_src.va`; companion
  `lfsr.va`, `dither_adder.va`, and `gain_amp_fixed.va` remain support
  artifacts in task-local metadata.
- Modeling repair: support copies remove debug `$strobe` output, use explicit
  `transition()` rise/fall on `vin_src`, and use event-updated dither target
  smoothing.
- Checker alignment: current evaluation remains flow-level; it is sufficient
  for support-component admission, not for standalone promotion.

## Validation

- AHDL-style preflight: PASS with 0 diagnostics.
- EVAS reference/negative sweep: reference PASS; 5/5 negatives rejected.
- Spectre private-split reference audit: PASS.

## Residual Risk

Promote to independent L1 only if upstream adds a task-specific `vin_src.va`
checker, visible/private decks, and negatives.
