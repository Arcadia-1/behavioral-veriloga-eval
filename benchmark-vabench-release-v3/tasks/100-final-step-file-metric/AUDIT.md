# Measurement Instrumentation Audit: Task 100 Final Step File Metric

## Gate 1

- Label: `independent_l1_ready`.
- Function boundary: standalone measurement helper that counts reference
  crossings, exposes a normalized metric, and writes the final metric at
  `final_step`.
- Counting note: measurement/instrumentation L1 row, not a composed L2 flow by
  itself.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: old testbench-companion and provenance wording were removed.
- Metadata repair: duplicate `./final_step_file_metric_ref.va` target entry was
  removed; level is L1.
- Modeling repair: `transition()` is fed by the event-updated normalized metric,
  with the supply scaling outside the transition expression.
- Checker alignment: checker measures crossing count progression, metric
  levels, and final metric behavior.

## Validation

- AHDL-style preflight: PASS with 0 diagnostics.
- EVAS reference/negative sweep: reference PASS; 5/5 negatives rejected.
- Spectre private-split reference audit: PASS.
