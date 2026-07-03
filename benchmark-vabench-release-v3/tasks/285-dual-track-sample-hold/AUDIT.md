# Two-Gate SOP Audit: Task 285 Dual Track Sample Hold

## Gate 1 Counting

- Label: `independent_l1_ready`
- Function boundary: dual complementary track/hold sample-and-hold.
- Rewrite decision: this row was a hard duplicate of the aperture-delay row
  081. It has been rewritten into a distinct dual-stage sampling-memory cell
  backed by Cadence training material that describes simple sample-and-hold and
  complementary track/hold implementations.
- Independence note: unlike 081, this row is not a point aperture sampler. The
  low clock phase tracks the input stage, the high clock phase transfers the
  retained input-stage value to the output stage, and falling edges freeze the
  output.

## Gate 2 Modeling

- Status: `cadence_modeling_ready`
- Public prompt defines the new artifact `dual_track_sample_hold.va`, interface,
  parameter defaults, two-stage phase behavior, clamp behavior, and voltage-only
  modeling boundary.
- `CHECKS.yaml`, `TASKS.json`, visible/hidden decks, checker mapping, gold, and
  negatives now agree on the rewritten task identity.
- Checker uses the public `tick`, `alpha_in`, and `alpha_out` contract to build
  a waveform reference model, plus phase-monitor and hold-window checks.

## Validation

- EVAS gold/negative: gold PASS; 5/5 concrete negatives rejected.
- EVAS preflight: visible and hidden decks PASS with zero diagnostics.
- Spectre hidden gold: PASS with zero simulator warnings.
