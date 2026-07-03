# Two-Gate SOP Audit: Task 109 Sample Hold Droop Front End

## Gate 1 Counting

- Label: `independent_l1_ready`
- Function boundary: compact sampling front-end component with aperture-delayed
  sampling, bounded droop, valid pulse, and coarse decision output.
- Independence note: this is more than a plain sample-and-hold because it
  combines aperture scheduling, droop memory, a completion pulse, and a coarse
  voltage-coded decision. It remains a single DUT component, so it is L1 rather
  than an L2 flow as written.

## Gate 2 Modeling

- Status: `cadence_modeling_ready`
- Public prompt now removes old testbench-companion and hidden-evaluator text.
- `CHECKS.yaml` now treats the task as a function-checked DUT, not as a
  testbench-generation row.
- Hidden stimulus now differs from the visible waveform while preserving the
  public aperture/droop/coarse/valid contract.

## Validation

- EVAS gold/negative: gold PASS; 5/5 concrete negatives rejected.
- EVAS preflight: visible and hidden decks PASS with zero diagnostics.
- Spectre hidden gold: PASS with zero simulator warnings.
