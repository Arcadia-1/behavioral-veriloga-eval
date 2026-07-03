# Two-Gate SOP Audit: Task 094 Comparator Offset Search

## Scope

Task 094 is retained as an L2 measurement/characterization flow artifact. The
target Verilog-A file is `comparator_offset_search_ref.va`; it observes a
comparator input sweep, records the first positive decision crossing, and
reports an estimated input-referred offset through analog output pins.

The row is not a second standalone comparator-decision L1 task. Its value is
the measurement behavior: detecting a crossing, latching the trip point, and
holding a valid offset estimate for downstream flow checks.

## Gate 1: Admission And Counting

- Admission label: `l2_measurement_ready`.
- Counting decision: human review confirmed that task 094 may be retained as
  an L2 measurement-flow benchmark, separate from ordinary comparator DUT rows.
- Function boundary: reusable transient offset-search/readout block, not
  checker implementation logic or a private testbench side channel.
- Validation alignment: the public outputs expose crossing detection, valid
  indication, and stable captured offset behavior.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the retained L2 measurement
  row after prompt repair and current EVAS/Spectre validation.
- Prompt hygiene: the prompt now states the public module, ports, parameters,
  crossing behavior, retained metric, and modeling constraints without
  old repair-history or validation-internal wording.
- Gold quality: the gold model uses voltage-domain threshold/crossing style
  behavior and rail-derived output levels; it does not require current-domain,
  AC/noise, or file/report side effects.
- Negative strength: current negative variants exercise behavioral failures of
  the measurement output contract: stub output, shifted threshold, wrong event
  edge, missing valid latch, and scaled offset metric.

## Evidence

- Current branch prompt review updated the public instruction to the mandatory
  vaBench v3 heading shape without changing the gold behavior.
- EVAS reference/negative evidence: reference PASS; 5/5 concrete negatives
  rejected behaviorally.
- AHDL-like preflight: private-split solution decks PASS with 0 diagnostics.
- Spectre private-split reference: PASS; observed trip average 0.4750 V and
  offset average 0.0050 V on the ramp.
- Spectre private-split negatives: 5/5 `NEGATIVE_REJECTED`; the rejected
  failure modes are stub output, shifted threshold, wrong event edge, missing
  valid latch, and scaled offset metric.
- Fresh evidence is required after any future gold/checker edits.

## Human Confirmation

The reviewer confirmed this row should not be rejected merely because it is a
support/measurement component. It is useful when labeled as an L2 measurement
flow and kept distinct from counted L1 comparator DUT coverage.
