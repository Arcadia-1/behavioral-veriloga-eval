# Two-Gate SOP Audit: Task 080 Acquisition Limited Sample And Hold

## Gate 1 Counting

- Label: `independent_l1_ready`
- Function boundary: finite-acquisition track/hold behavior with a public
  tracking monitor.
- Independence note: this is not an ideal edge sampler. The output moves toward
  `vin` over a tracking window and freezes at the last acquired value on the
  falling sample edge.

## Gate 2 Modeling

- Status: `cadence_modeling_ready`
- Public prompt now removes migration/history text and states the DUT interface,
  parameter defaults, acquisition update behavior, reset behavior, and metric
  semantics.
- Hidden stimulus now differs from the visible waveform.
- Checker was generalized from fixed time samples to event-derived acquisition
  and hold windows.

## Validation

- EVAS gold/negative: gold PASS; 5/5 concrete negatives rejected.
- EVAS preflight: visible and hidden decks PASS with zero diagnostics.
- Spectre hidden gold: PASS with zero simulator warnings.
