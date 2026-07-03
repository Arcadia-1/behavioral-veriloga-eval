# Two-Gate SOP Audit: Task 044 Sample And Hold With Droop Leakage

## Gate 1 Counting

- Label: `independent_l1_ready`
- Function boundary: sample-and-hold analog memory with reset and droop/leakage.
- Independence note: droop/leakage memory is a distinct behavior from the
  canonical ideal sample-and-hold because the held state decays between sample
  events and reset clears the memory.

## Gate 2 Modeling

- Status: `cadence_modeling_ready`
- Public prompt now exposes the DUT interface, reset/sample behavior, leakage
  update contract, parameter defaults, and voltage-only modeling boundary.
- Checker measures sampled-level capture, droop over hold windows, reset clear,
  and post-reset recovery.

## Validation

- EVAS gold/negative: gold PASS; 5/5 concrete negatives rejected.
- EVAS preflight: visible and hidden decks PASS with zero diagnostics.
- Spectre hidden gold: PASS with zero simulator warnings.
