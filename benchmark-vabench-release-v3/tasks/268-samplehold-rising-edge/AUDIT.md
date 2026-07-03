# Two-Gate SOP Audit: Task 268 Source Samplehold Rising Edge

## Gate 1 Counting

- Label: `valid_variant_needs_counting_policy`
- Function boundary: rising-edge sample-and-hold with a 5 V control threshold
  and compact three-port source-style interface.
- Independence note: functionally this overlaps the ordinary sample-and-hold
  family represented by 026 and the cross-category 252 5 V sample-hold row.
  Keep it only if upstream wants a source-corpus/interface variant; otherwise
  it should not add another independent sample-and-hold count.

## Gate 2 Modeling

- Status: `cadence_modeling_ready`
- Public prompt now states the module interface, parameter defaults, rising-edge
  capture behavior, hold behavior, and voltage-only boundary.
- Hidden stimulus now differs from the visible waveform.
- Checker was generalized from fixed source-import sample points to
  event-derived rising-edge and hold-window checks.

## Validation

- EVAS gold/negative: gold PASS; 5/5 concrete negatives rejected.
- EVAS preflight: visible and hidden decks PASS with zero diagnostics.
- Visible smoke: PASS.
- Spectre hidden gold: PASS with zero simulator warnings.
