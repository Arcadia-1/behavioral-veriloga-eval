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
- Checker alignment: the checker samples the public outputs for crossing
  detection, valid indication, and stable captured offset behavior.

## Gate 2: Cadence Modeling Quality

- Modeling status: `cadence_modeling_ready` for the retained L2 measurement
  row after prompt repair and current EVAS/Spectre validation.
- Prompt hygiene: the prompt now states the public module, ports, parameters,
  crossing behavior, retained metric, and modeling constraints without
  migration-history or hidden-evaluator wording.
- Gold quality: the gold model uses voltage-domain threshold/crossing style
  behavior and rail-derived output levels; it does not require current-domain,
  AC/noise, or file/report side effects.
- Negative strength: current negative evidence exercises behavioral failures
  of the measurement output contract; additional hand-authored negatives can
  further strengthen the final release surface.

## Evidence

- EVAS hidden gold: PASS; the checker reports the expected 0.475 V trip point
  and 5 mV offset estimate on the repaired hidden deck.
- EVAS negatives: 1/1 behavioral rejection after normalizing the
  `negative_variants/manifest.json` schema.
- Spectre hidden gold: PASS with no task-level warnings or errors in the
  result JSON.
- Spectre negatives: 1/1 `NEGATIVE_REJECTED` on the hidden deck.

## Human Confirmation

The reviewer confirmed this row should not be rejected merely because it is a
support/measurement component. It is useful when labeled as an L2 measurement
flow and kept distinct from counted L1 comparator DUT coverage.
